#########################################################################################
# interface.make
#	Global Makefile Interface
#----------------------------------------------------------------------------------------
# Note: Using this interface as a Makefile won't work!
# It's only purpose is to be included in another Makefile setting the needed
# variables properly. The following variables are expected to be set:
#
#	srcFiles   => The list of source files.
#
#	objFiles   => The list of object files. It might be set via:
#	               e.g.: objFiles = $(srcFiles:.c=.o)
#
#	subFolders => The list of subfolders containing further source files.
#
#	output     => This names the output of the linker. For the project's root folder
#	              it may be the name of the executable.
#	              For any subfolder it is expected to name a _relocatable_ linked
#	              library being thrown out:
#	               e.g.: ../subfoldersName.lib
#	              For this, don't miss to add LNKopt_reloc to LNKFLAGS!
#
#	extLib     => The list of external libraries being linked.
#
#	CFLAGS  	  => May be used to set switches and compiler flags to affect module
#	              compilation. This is probably set by your make environment.
#	              Note: this variable is propagated to all subcalls of make.
#
#	LNKFLAGS   => The flags to be set for the linking process. Unlike CFLAGS, this
#	              variable won't be propatated to any subcall of make!
#
#	CC_INCLUDE => The include paths for searching included files during compilation.
#	              When specifying this, be aware to use variables instead of the flags.
#	              With this in mind, you can keep your Makefile compiler independent.
#	               e.g.: CC_INCLUDE = $(CCopt_incP) ./somePath $(CCopt_incP) ./anotherOne
#
# Try to get a proper Makefile by configuring the project folder.
#----------------------------------------------------------------------------------------
#
# Author:	Josef Scheuer
# Date:		10 Aug 2005
# Rev:		$Id: interface.make,v 1.1 2005/10/17 16:48:09 josch Exp $
#----------------------------------------------------------------------------------------
# Log:		$Log: interface.make,v $
# Log:		Revision 1.1  2005/10/17 16:48:09  josch
# Log:		*** empty log message ***
# Log:		
# Log:		Revision 1.1.1.1  2005/09/25 22:05:03  josch
# Log:		MakeIt makefile interface & configure
# Log:		
# Log:		Revision 1.2  2005/08/15 22:07:22  josch
# Log:		Moving phony subfolder target downwards as it is _not_ the default target.
# Log:		
#----------------------------------------------------------------------------------------
#

##
# Compiler and Linker Options & Flags
#------------------------------------------------
CC					= g++
CCopt_incP		= -I
CCopt_ppo		= -E
CCopt_cpl		= -c
CCopt_deps		= -M
CCopt_opt		= -O3
CCopt_dbg		= -ggdb -D DEBUG
CCopt_dbgF		= $(CCopt_dbg) -Wall

LNK				= ld
LNKopt_lnkP		= -L
LNKopt_reloc	= -r
LNKopt_out		= -o


##
# Make Settings
#------------------------------------------------
Mk_deps	= depend.make
Mk_tmp	= *.o *.lib
Mk_opt	= 

##
# Make Targets
#------------------------------------------------
#
default: $(output)
	@echo $(INDENT)$(output) is up-to-date!

$(output): $(objFiles) $(subFolders:=.lib)
	@echo $(INDENT)[linking ...]
	$(LNK) $(LNKFLAGS) $(objFiles) $(subFolders:=.lib) $(extLib) $(LNKopt_out) $(output)
	@echo $(INDENT)[done.]

$(subFolders:=.lib): $(subFolders)


rebuild:
	@$(MAKE) $(Mk_opt) clean
	@$(MAKE) "CFLAGS=$(CFLAGS)" depend $(Mk_opt)
	@$(MAKE) "CFLAGS=$(CFLAGS)" $(Mk_target) $(Mk_opt)

debug:
	@$(MAKE) "CFLAGS=$(CFLAGS) $(CCopt_dbg)" $(Mk_target) $(Mk_opt)
	
debugFull:
	@$(MAKE) "CFLAGS=$(CFLAGS) $(CCopt_dbgF)" $(Mk_target) $(Mk_opt)

optimize:
	@$(MAKE) "CFLAGS=$(CFLAGS) $(CCopt_opt)" $(Mk_target) $(Mk_opt)
	

##
# Special Targets
#------------------------------------------------
#
depend:
	@echo $(INDENT)[building dependencies ...]
	@	$(MAKE) "CFLAGS=$(CFLAGS)" "INDENT=$(INDENT)" "Mk_target=depend" __doDepend $(Mk_opt)
	@echo $(INDENT)[done.]

__doDepend: $(subFolders)
	$(CC) $(CFLAGS) $(CC_INCLUDE) $(CCopt_deps) $(srcFiles) > $(Mk_deps)

clean:
	@echo $(INDENT)[making clean ...]
	@rm -f $(Mk_tmp)
	@$(MAKE) "CFLAGS=$(CFLAGS)" "INDENT=$(INDENT)" "Mk_target=clean" __doClean $(Mk_opt)
	@echo $(INDENT)[done.]

__doClean: $(subFolders)

# Recursive run through subfolders
.PHONY: $(subFolders)
$(subFolders):
	@echo $(INDENT)[entering $@]
	@	cd $@ && $(MAKE) "CFLAGS=$(CFLAGS)" "INDENT=$(INDENT)\ \ " $(Mk_opt) $(Mk_target) && cd ..
	@echo $(INDENT)[leaving $@]


##
# Conversion Rules
#------------------------------------------------
# known suffixes
.SUFFIXES:
.SUFFIXES: .o .c .cpp
#
.c.o:
	$(CC) $(CFLAGS) $(CC_INCLUDE) $(CCopt_cpl) $<

.cpp.o:
	$(CC) $(CFLAGS) $(CC_INCLUDE) $(CCopt_cpl) $<


# include file dependencies
include $(Mk_deps)

