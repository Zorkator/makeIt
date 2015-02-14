
TARGET_doc = Some project for\\n testing make files
SOURCE_FILES         = $(call any_source) $(call any_source_in,sub)
#IGNORE_FILES.32     = func1.f90
#IGNORE_FILES.64     = func2.f90
#IGNORE_FILES.%      = testinger.f90
#IGNORE_FILES.static = testinger.for
#SUB_DIRS = sub

FC_PP_DEFINES     =
FC_INCLUDE_DIRS   =
FC_FLAGS          =
FC_CFLAGS         = 
FC_CFLAGS.debug   = $(fc_g)
FC_CFLAGS.release = $(fc_O3)

func1.shared = -DBLA=1
func2.% = -DBLUB=1


FC_LIBRARY_DIRS   = 
FC_LIBRARIES      = 
FC_LFLAGS         =
FC_LINK_INPUT     =

MAKEIT_DIR = ../
include $(MAKEIT_DIR)/mk.compilation
include $(MAKEIT_DIR)/mk.fortran
sinclude $(mk_DEPS)

