
"""Usage: fort_deps [((-o|-a) <outfile>)] [--fpp=<cmd>] <file>...

Generate Fortran dependencies.
The result is output to stdout or given output file.

Options:
	-o            overwrite given output file
	-a            append to given output file
	--fpp=<cmd>   preprocess each file by given command <cmd>.
	              For complex commands use {} as a placeholder for the input file.
"""

import docopt, re, sys, os
from os.path import splitext

class DepsCrawler(object):

	_scanMod = re.compile( r'^\s*module\s+(\w+)\s*(?:!.*|)$', re.IGNORECASE ).match
	_scanUse = re.compile( r'^\s*use\s+(\w+)',                re.IGNORECASE ).match

	@staticmethod
	def _obj( fileName ):
		return splitext( fileName )[0] + '.o'


	def __init__( self, fpp, fileList ):
		self._fileTab, self._modTab = dict(), dict()
		for fileName in fileList:
			try  : self.scanFile( fileName, fpp )
			except IOError as e:
				print "%s skipped: %s" % (fileName, e)


	def scanFile( self, fileName, fpp ):
		with open( fileName ) as f:
			uses = self._fileTab.setdefault( fileName, set() )
			for mod in self.scanStream( f, uses ):
				self._modTab[mod] = fileName


	def scanStream( self, stream, uses ):
		mods = set()
		for line in stream.readlines():
			mod = self._scanMod( line )
			if mod:
				mods.add( mod.groups()[0] ); continue
			use = self._scanUse( line )
			if use:
				uses.add( use.groups()[0] ); continue
		return mods


	def __iter__( self ):
		for f, uses in self._fileTab.items():
			modFiles = set( map( self._modTab.get, uses ) ) - set([f])
			yield self._obj(f) + ': ' + ' '.join( map( self._obj, filter( None, modFiles ) ) )


	def __str__( self ):
		return '\n'.join( self )



if __name__ == "__main__":
	opts = docopt.docopt( __doc__ )
	print opts

	outfile = opts.get('<outfile>')
	if outfile: out = open( outfile, ('w', 'a')[opts.get('-a')] )
	else      : out = sys.stdout

	deps = DepsCrawler( opts.get('--fpp'), opts['<file>'] )
	out.write( str(deps) + '\n' )

