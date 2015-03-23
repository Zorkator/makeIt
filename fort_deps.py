
"""Usage: fort_deps [((-o|-a) <outfile>)] [--fpp=<cmd>] [--objdir=<dir>] <file>...

Generate Fortran dependencies.
The result is output to stdout or given output file.

Options:
	-o              overwrite given output file
	-a              append to given output file
	--fpp=<cmd>     preprocess each file by given command string <cmd>.
	                Within <cmd> the placeholder {f} is replaced by the name of the file to preprocess.
	--objdir=<dir>  replace directory of input files by given string <dir>.
"""

import docopt, re, sys, shlex
from os.path    import splitext as _splitext, split as _splitpath, join as _joinpath
from subprocess import Popen as _Popen, PIPE as _PIPE

class DepsCrawler(object):

	_scanMod = re.compile( r'^\s*module\s+(\w+)\s*(?:!.*|)$', re.IGNORECASE ).match
	_scanUse = re.compile( r'^\s*use\s+(\w+)',                re.IGNORECASE ).match

	@staticmethod
	def _getStream( fileName, fpp ):
		if fpp: return _Popen( shlex.split( fpp.format( f=fileName ) ), stdout=_PIPE ).stdout
		else  : return open( fileName, 'r' )


	def __init__( self, **kwArgs ):
		self._objDir = kwArgs['--objdir']
		if   self._objDir is None: self._setObjDir = lambda f: f
		elif self._objDir        : self._setObjDir = lambda f: _joinpath( self._objDir, _splitpath(f)[-1] )
		else                     : self._setObjDir = lambda f: _splitpath(f)[-1]

		self._fileTab, self._modTab = dict(), dict()
		for fileName in kwArgs['<file>']:
			try  : self.scanFile( fileName, kwArgs['--fpp'] )
			except IOError as e:
				print "%s skipped: %s" % (fileName, e)


	def scanFile( self, fileName, fpp ):
		with self._getStream( fileName, fpp ) as stream:
			uses = self._fileTab.setdefault( fileName, set() )
			for line in stream.readlines():
				use = self._scanUse( line )
				if use:
					uses.add( use.groups()[0].lower() )
				else:
					mod = self._scanMod( line )
					if mod:
						self._modTab[ mod.groups()[0].lower() ] = fileName


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

