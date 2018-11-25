
makeIt
======

.. contents::

About
-----

makeIt is another approach to simplify the creation of GNU Make-based makefiles.
It contains a collection of modular make definitions and functions that could be included in project makefiles.
These, mostly very generic, definitions try to handle the typical build steps and can be customized by setting variables or passing arguments.
The goal of makeIt is reducing your makefile to the absolute minimum by including these definitions and redefine the default settings if needed by your own variables.

makeIt contains and uses the really nice GNU Make Standard Library of John Graham-Cumming (http://gmsl.sourceforge.net/)

Usage
-----

After cloning makeIt to some directory the easiest is to set an environment variable (e.g. MAKEIT_DIR) to this directory.
This environment variable can than be used in your project makefiles to include the definitions you need, e.g. for a C/C++ project::

  > cd my_project
  > cat makefile
  include $(MAKEIT_DIR)/mk.c++

Actually this is already suitable for building an easy C/C++-project by calling::

  > make built

To customize your *makefile* you should consult the built-in help page (the default target)::

  > make help
  
  == KNOWN CONFIGURATIONS == 
  debug      shortcut target for building with debug options. Equivalent to: "make built CFG=debug"
  release    shortcut target for building with optimization and without debug options. Equivalent to: "make built CFG=release"
                
  == OTHER TARGETS ==        
  built      target for starting build process
  clean      clear build directory [.work/debug.64.gcc.exe] by removing object files
  cpp,*      preprocess file to stdout. Directories have to be separated by \\, e.g. make cpp,src\\main.cpp
  dist-*     meta target for starting make on distribution configurations: {64-}{{release-}{exe,shared,static}}
  echo,*     evaluate value of make variable 
  eval,*     evaluate a make variable by calling with argument, e.g. make eval._mkFunc,arg. Separate directories by \\.
  grep,*     grep pattern in source files: make grep,PATTERN[,GREP-OPTS]; default: GREP-OPTS: -iw
  help       print overview over supported parameters and targets
  log        show the logged command output via less
  rescan     trigger rescan of source files and recreation of build dependencies
  value,*    show value of make variable
  vartab,*   print overview over known variables with given prefix, e.g. make vartab,mk_
                
  == CURRENT PARAMETERS ==   
  ARCH             default       architecture id: {64,32}                                      64
  BUILD_DIR        default       working directory for building object files.                  .work/debug.64.gcc.exe
  BUILD_MODE       default       mode for building object files: {exe,shared,static}           exe
  CC               file          used c/c++ compiler: {gcc}                                    gcc
  CC_CFLAGS        default       c/c++ compile flags, applied to any file                      -ggdb
  CC_FLAGS         default       flags, applied to any c/c++ compile and link command          -m64
  CC_INCLUDE_DIRS  default       c/c++ include directories                                     
  CC_LFLAGS        default       c/c++ link flags                                              -Wl,-rpath,$ORIGIN
  CC_LIBRARIES     default       list of c/c++ linked libraries                                
  CC_LIBRARY_DIRS  default       list of library directories (c/c++-link only!)                
  CC_LINK_OTHER    default       list of other c/c++ link input files                          
  CC_PP_DEFINES    default       list of c-preprocessor defines                                
  CFG              default       current build configuration: {debug,release}                  debug
  LOG              default       switch to enable/disable logging: {on,off}                    on
  LOG_FILE         default       file for logging build messages.                              .work/debug.64.gcc.exe/_log.txt
  OUT_DIR          default       output directory for effective output file(s)                 .work/debug.64.gcc.exe
  OUT_FILE         default       path and file name of the final result                        .work/debug.64.gcc.exe/outname.debug.64.gcc
  OUT_FILE_NAME    default       the file name of the final result                             outname.debug.64.gcc
  OUT_NAME         default       the base name of the final result                             outname.debug.64.gcc
  OUT_TYPE         file          type of built binary: {exe,shared,static}                     exe
  OUT_UMASK        default       the umask to set for the final output file                    
  SUBPACKAGES      default       directory list of project prerequisites                       
  TAG              default       string for tagging build directory.                           debug.64.gcc


- The first column of section CURRENT PARAMETERS lists the most important variables that can be configured in your *makefile* or by command line argument.
- The second column specifies the origin of the current variable setting.
- The third column gives a short description of these variables and, for some of them, a list of supported values.
- The last column reports the currently effective settings.

Before changing the *makefile* the effect of certain settings can easily be tested on the command line::

  > make OUT_TYPE=shared CFG=release

... what gives an updated overview page and the effective settings at the last column of *CURRENT PARAMETERS*.
To start building with these settings, don't forget to provide the target *built*::

  > make OUT_TYPE=shared CFG=release built


Useful hints
------------

The variable names listed in the first column of *CURRENT PARAMETERS* are the variables you use for setting your values.
From variables specified by your *makefile* and command line arguments makeIt derives the effective settings and lists them in the last column.
These effective settings can be queried by the internally defined counterpart of the variables, prefixed by **mk_**.

To get the effective content of a certain variable you can use one of the targets **echo,** or **eval,**.
The following example shows the difference between the variables and their **mk_**-counterparts::

  > make -s eval,mk_OUT_FILE   #< gives the derived setting. Note that the flag -s suppresses info messages!
  outname.debug.64.gcc
  > make -s eval,OUT_FILE      #< gives the content of OUT_FILE
  
  > make -s eval,OUT_FILE OUT_FILE=file.out
  file.out


Example
-------

A simple *makefile* for building a simple c++ program::

  > ls -R
  .:
  class.cpp  include  main.cpp  makefile

  ./include:
  class.hpp
  >
  > cat makefile
  CC_INCLUDE_DIRS := include
  include $(MAKEIT_DIR)/mk.c++


TODO
----

makeIt works quite well for C/C++ and Fortran projects.
However, there are many things that can be improved:

- improve documentation, give more examples
- there's always the need for cleaning up ;-)
- adding support for other languages
- ...


Copyright and License Information
---------------------------------

Copyright (c) 2018 Josef Scheuer.
All rights reserved.

See the file "LICENSE" for information on the terms &
conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.

