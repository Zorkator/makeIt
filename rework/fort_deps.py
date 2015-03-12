
"""Usage: fort_deps [--output=<outfile>] <file>...

Generate Fortran dependencies.
The result is output to stdout or given output file.

Options:
	--output=<outfile>		the output file

"""

import docopt, re
from extensions import Dict

class DepsCrawler(object):

	_mod = re.compile( r'^\s*module\s+(\w+)\s*(?:!.*|)$', re.IGNORECASE ).match
	_use = re.compile( r'^\s*use\s+(\w+)',                re.IGNORECASE ).match

	@staticmethod
	def _cmp( a, b ):
		if not a[1][1].isdisjoint( b[1][0] ): return 1
		if not b[1][1].isdisjoint( a[1][0] ): return -1
		return 0


	def __init__( self, **kwArgs ):
		self._fileTab = Dict()
		for fileName in kwArgs['<file>']:
			self.scanFile( fileName )
		

	def __iter__( self ):
		fileList = self._fileTab.items()
		fileList.sort( self._cmp )
		for f in fileList:
			yield f


	def __str__( self ):
		return '\n'.join( map( str, self ) )


	def scanFile( self, fileName ):
			fileInfo = self._fileTab.setdefault( fileName, [] )
			if not fileInfo:
				fileInfo.extend( (set(),set()) ) #< ([<modSet>], [<useSet>])
				with open( fileName ) as f:
					for line in f.readlines():
						mod = self._mod( line )
						if mod: fileInfo[0].add( mod.groups()[0] )
						else:
							use = self._use( line )
							if use: fileInfo[1].add( use.groups()[0] )





if __name__ == "__main__":
	print DepsCrawler( **docopt.docopt( __doc__ ) )

