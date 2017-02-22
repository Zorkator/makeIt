#!/usr/bin/env python
"""Usage:
  fort_deps [-v...] [options] [FILE...]
  fort_deps (-h | --help)

Generate Fortran module dependencies. All given files are scanned for
definitions and uses of modules. For module definitions fort_deps detects any
legal fortran module start line _and_ preprocessor includes, matching the form:
    #include "[<path>]<module_name>.fmod" The result is written in make syntax
    to stdout or any given output file.

Options:
  -h --help                     show this help screen.
  -i LISTFILE, --in LISTFILE    read list of (whitespace separated) input files from
                                textfile LISTFILE. Use '-' for reading from stdin.
  -o OUTFILE, --out OUTFILE     write output to file instead of dumping it to stdout.
  -a --append                   append to given output file
  -p CMD, --fpp CMD             preprocess each file by given command string CMD.
                                Within CMD the placeholder {f} is replaced by the name of
                                the file to preprocess.
  -d DIR, --objdir DIR          replace directory of input files by given string DIR.
  -j JOBS, --jobs JOBS          number of threads for processing files [default: 1].
  -v                            set verbosity of printed messages. Increase level by
                                repeating the option.
"""

from os.path              import splitext as _splitext, split as _splitpath, join as _joinpath
from subprocess           import Popen as _Popen, PIPE as _PIPE
from multiprocessing.pool import ThreadPool
import docopt, re, sys, logging

logging.basicConfig()

class DepsCrawler(object):

  _scanMod   = re.compile( r'^\s*module\s+(\w+)\s*(?:!.*|)$',          re.IGNORECASE ).match
  _scanInc   = re.compile( r'^#\s*include\s*["\'].*?(\w+)\.fmod["\']', re.IGNORECASE ).match
  _scanUse   = re.compile( r'^\s*use\s+(\w+)',                         re.IGNORECASE ).match
  _tryCodecs = ['latin-1', 'utf-8']

  @staticmethod
  def _getStream( fileName, fpp, codec ):
    import shlex, codecs
    if fpp: return _Popen( shlex.split( fpp.format( f=fileName ) ), stdout=_PIPE ).stdout
    else  : return codecs.open( fileName, 'r', codec )


  def __init__( self, **kwArgs ):
    self._log = logging.getLogger( self.__class__.__name__ )
    self._log.setLevel( logging.WARNING - kwArgs['-v'] * 10 )
    self._log.debug( kwArgs )

    self._objDir = kwArgs['--objdir']
    if   self._objDir is None: self._setObjDir = lambda f: f
    elif self._objDir        : self._setObjDir = lambda f: _joinpath( self._objDir, _splitpath(f)[-1] )
    else                     : self._setObjDir = lambda f: _splitpath(f)[-1]

    fileList, fileSet = kwArgs['--in'], set( kwArgs['FILE'] )
    if fileList:
      with (fileList == '-' and sys.stdin) or open( fileList ) as listFile:
        fileSet |= set( ' '.join( listFile.readlines() ).split() )

    self._fpp = kwArgs['--fpp']
    self._fileTab, self._modTab = dict(), dict()
    ThreadPool( processes=int(kwArgs['--jobs']) ).map( self.scanFile, fileSet )
    self._log.info( ' Module definitions:\n\t' +
                    '\n\t'.join( map( ': '.join, self._modTab.items() ) ) )


  def scanFile( self, fileName ):
    try:
      self._log.info( "scanning " + fileName )
      uses = self._fileTab.setdefault( fileName, set() )
      for line in self._readFile( fileName ):
        use = self._scanUse( line )
        if use:
          uses.add( use.groups()[0].lower() )
        else:
          mod = self._scanMod( line ) or self._scanInc( line )
          if mod:
            self._modTab[ mod.groups()[0].lower() ] = fileName
    except IOError as e:
      self._log.error( "{0} skipped: {1}".format( fileName, e ) )


  def _readFile( self, fileName ):
    for codec in self._tryCodecs:
      try:
        with self._getStream( fileName, self._fpp, codec ) as stream:
          return stream.readlines()
      except UnicodeError:
        self._log.warning( "failed at decoding {0} by codec {1}".format( fileName, codec ) )
    else:
      raise UnicodeDecodeError( "unable to decode {0}".format( fileName ) )


  def _obj( self, fileName ):
    return self._setObjDir( _splitext( fileName )[0] + '.o' )


  def __iter__( self ):
    for f, uses in self._fileTab.items():
      modFiles = set( map( self._modTab.get, uses ) ) - set([f])
      yield self._obj(f) + ': ' + ' '.join( map( self._obj, filter( None, modFiles ) ) )



if __name__ == "__main__":
  opts = docopt.docopt( __doc__ )

  try             : out = open( opts['--out'], 'wa'[opts['--append']] )
  except TypeError: out = sys.stdout

  deps = DepsCrawler( **opts )
  out.write( '\n'.join( deps ) + '\n' )

