#!/usr/bin/env python
"""Usage: fort_deps [((-a|-o) <outfile>)] [--verbose] [--fpp=<cmd>] [--objdir=<dir>] [--filelist=<listfile>] [<file>...]

Generate Fortran module dependencies.
All given files are scanned for definitions and uses of modules.
For module definitions fort_deps detects any legal fortran module start line _and_ preprocessor includes, matching the form:
#include "[<path>]<module_name>.fmod"
The result is written in make syntax to stdout or any given output file.

Options:
	-a                      append to given output file
	-o                      overwrite given output file
	--filelist=<listfile>   read list of (whitespace separated) input files from textfile <listfile>. Use '-' for reading from stdin.
	--fpp=<cmd>             preprocess each file by given command string <cmd>.
	                        Within <cmd> the placeholder {f} is replaced by the name of the file to preprocess.
	--objdir=<dir>          replace directory of input files by given string <dir>.
	--verbose               be verbose, print comment lines with process info.
"""

import docopt, re, sys, shlex
from os.path    import splitext as _splitext, split as _splitpath, join as _joinpath
from subprocess import Popen as _Popen, PIPE as _PIPE


class DepsCrawler(object):

	_scanMod = re.compile( r'^\s*module\s+(\w+)\s*(?:!.*|)$',          re.IGNORECASE ).match
	_scanInc = re.compile( r'^#\s*include\s*["\'].*?(\w+)\.fmod["\']', re.IGNORECASE ).match
	_scanUse = re.compile( r'^\s*use\s+(\w+)',                         re.IGNORECASE ).match

	@staticmethod
	def _getStream( fileName, fpp ):
		if fpp: return _Popen( shlex.split( fpp.format( f=fileName ) ), stdout=_PIPE ).stdout
		else  : return open( fileName, 'r' )


	def __init__( self, **kwArgs ):
		if kwArgs['--verbose']: self._log = lambda *msg: self._out( 1, *msg )
		else                  : self._log = lambda *msg: None

		self._objDir = kwArgs['--objdir']
		if   self._objDir is None: self._setObjDir = lambda f: f
		elif self._objDir        : self._setObjDir = lambda f: _joinpath( self._objDir, _splitpath(f)[-1] )
		else                     : self._setObjDir = lambda f: _splitpath(f)[-1]

		fileList, fileSet = kwArgs['--filelist'], set( kwArgs['<file>'] )
		if fileList:
			with (fileList == '-' and sys.stdin) or open( fileList ) as listFile:
				fileSet |= set( ' '.join( listFile.readlines() ).split() )

		self._log( "processed files:", *fileSet )
		self._fileTab, self._modTab = dict(), dict()
		for fileName in fileSet:
			try  : self.scanFile( fileName, kwArgs['--fpp'] )
			except IOError as e:
				self._out( 2, "WARNING: %s skipped: %s" % (fileName, e) )
		self._log( "\n", "module definitions:", *map( ': '.join, self._modTab.items() ) )


	def scanFile( self, fileName, fpp ):
		with self._getStream( fileName, fpp ) as stream:
			uses = self._fileTab.setdefault( fileName, set() )
			for line in stream.readlines():
				use = self._scanUse( line )
				if use:
					uses.add( use.groups()[0].lower() )
				else:
					mod = self._scanMod( line ) or self._scanInc( line )
					if mod:
						self._modTab[ mod.groups()[0].lower() ] = fileName


	def _out( self, ch, *msg ):
		(None, sys.stdout, sys.stderr)[ch].write( '# %s\n' % '\n# '.join( msg ) )


	def _obj( self, fileName ):
		return self._setObjDir( _splitext( fileName )[0] + '.o' )


	def __iter__( self ):
		for f, uses in self._fileTab.items():
			modFiles = set( map( self._modTab.get, uses ) ) - set([f])
			yield self._obj(f) + ': ' + ' '.join( map( self._obj, filter( None, modFiles ) ) )



if __name__ == "__main__":
	options = docopt.docopt( __doc__ )
	outfile = options.get('<outfile>')
	if outfile: out = open( outfile, ('w', 'a')[options.get('-a')] )
	else      : out = sys.stdout

	deps = DepsCrawler( **options )
	out.write( '\n'.join( deps ) + '\n' )

