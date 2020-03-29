
ifndef __mk_cpp_included
__mk_cpp_included := true

include $(dir $(lastword $(MAKEFILE_LIST)))mk.compilation

mk_PARAMETERS    += CC CC_PP_DEFINES CC_INCLUDE_DIRS CC_FLAGS CC_CFLAGS CC_LFLAGS CC_LIBRARY_DIRS CC_LIBRARIES CC_LINK_OTHER
mk_OPT_CLASSES   += CC
mk_TARGET_list   += cpp,*
mk_FILE_TYPES    += $(__cc_file_types)
mk_OUTPUT_DIRS   +=
mk_CLEARED_FILES += $(mk_BUILD_DIR)/*.o

mk_CC_list       += gcc
mk_ARCH_list     += 64 32
cmd_CC_version    = $(shell $(fc) $(fc_version) 2>&1 | sed -ne 's/\([0-9]\+\.[0-9.]\+\)/\1/p')
cmd_depends      += cmd_CC_depends

# $(cmd_LINK,OUT_FILE,OBJECTS)
define cmd_LINK
	$(call cc_cmd_link.$(mk_OUT_TYPE),$1,$2)
endef

# $(cmd_CC_depends,DEPS_FILE,SOURCE_LIST)
define cmd_CC_depends
	$(eval ___cc_src := $(call mk_file_list,filter,$(__cc_file_types),$2))
	$(if $(___cc_src),\
		$(call mk_xargs,g++ $(__cc_include_dirs) $(__cc_pp_defines) -MM >> $1,$(___cc_src)) \
		sed -i 's|^\(.*\.o:\)|$(mk_BUILD_DIR)/\1|' $1)
endef

#-- user parameters --

CC_doc              ?= used c/c++ compiler: $(call mk_opt_set,CC)
CC                   = $(firstword $(mk_CC_list))#< override default on most systems: cc
mk_CC                = $(call mk_get,CC)

CC_PP_DEFINES_doc   ?= list of c-preprocessor defines
mk_CC_PP_DEFINES     = $(call mk_get,CC_PP_DEFINES)

CC_INCLUDE_DIRS_doc ?= c/c++ include directories
mk_CC_INCLUDE_DIRS   = $(call mk_get,CC_INCLUDE_DIRS)

CC_FLAGS_doc        ?= flags, applied to any c/c++ compile and link command
CC_FLAGS.%          ?= $(cc_m)$(mk_ARCH)
CC_FLAGS.shared     ?= $(cc_pic)
mk_CC_FLAGS          = $(call mk_get,CC_FLAGS)

CC_CFLAGS_doc       ?= c/c++ compile flags, applied to any file
CC_CFLAGS.debug     ?= $(cc_g)
CC_CFLAGS.release   ?= $(cc_O3)
mk_CC_CFLAGS         = $(call mk_get,CC_CFLAGS)

CC_LFLAGS_doc       ?= c/c++ link flags
CC_LFLAGS.exe       ?= $(cl_rpath)'$$ORIGIN'
CC_LFLAGS.shared    ?= $(cl_rpath)'$$ORIGIN' $(cl_no_undef) $(cl_soname)$(mk_OUT_FILE_NAME)$(mk_MAYOR)
mk_CC_LFLAGS         = $(call mk_get,CC_LFLAGS)

CC_LIBRARY_DIRS_doc ?= list of library directories (c/c++-link only!)
mk_CC_LIBRARY_DIRS   = $(call mk_get,CC_LIBRARY_DIRS)

CC_LIBRARIES_doc    ?= list of c/c++ linked libraries
mk_CC_LIBRARIES      = $(call mk_get,CC_LIBRARIES)

CC_LINK_OTHER_doc   ?= list of other c/c++ link input files
mk_CC_LINK_OTHER     = $(call mk_get,CC_LINK_OTHER)

#-- exposed compiler switches --

cc              = $(__cc_$(mk_CC))#              < compiler call
cc_version      = $(__cc_version_$(mk_CC))#      < compiler version string
cc_c            = $(__cc_c_$(mk_CC))#            < compile only (no linking)
cc_g            = $(__cc_g_$(mk_CC))#            < compile with debug info
cc_O0           = $(__cc_O0_$(mk_CC))#           < optimization level O0
cc_O1           = $(__cc_O1_$(mk_CC))#           < optimization level O1
cc_O2           = $(__cc_O2_$(mk_CC))#           < optimization level O2
cc_O3           = $(__cc_O3_$(mk_CC))#           < optimization level O3
cc_o            = $(__cc_o_$(mk_CC))#            < output file
cc_m            = $(__cc_m_$(mk_CC))#            < architecture
cc_omp          = $(__cc_omp_$(mk_CC))#          < enable OpenMP extensions
cc_fpe          = $(call __cc_fpe_$(mk_CC),$1)#  < set fpe-trap mode: $(call fc_fpe,{0,1,3})
#                                                     0: traps invalid, div_by_zero, underflow, overflow, inexact, NANs
#                                                     1: traps invalid, div_by_zero, underflow, overflow, inexact
#                                                     3: no traps
cc_pp_old       = $(__cc_pp_old_$(mk_CC))#       < enable traditional mode of c preprocessor
cc_E            = $(__cc_E_$(mk_CC))#            < preprocess only
cc_D            = $(__cc_D_$(mk_CC))#            < define preprocessor symbol
cc_I            = $(__cc_I_$(mk_CC))#            < include directory
cc_L            = $(__cc_L_$(mk_CC))#            < link directory
cc_l            = $(__cc_l_$(mk_CC))#            < link library
cc_pic          = $(__cc_pic_$(mk_CC))#          < generate position independent code (pic) for shared libraries
cc_threads      = $(__cc_threads_$(mk_CC))#      < enable threading support
cc_c++11        = $(__cc_c++11_$(mk_CC))#        < enable C++11 support
#
cl          = $(__cl_$(mk_CC))#                  < linker call
cl_soname   = $(__cl_soname_$(mk_CC))#           < set soname
cl_static   = $(__cl_static_$(mk_CC))#           < force static linking
cl_rpath    = $(__cl_rpath_$(mk_CC))#            < burn library path
cl_no_undef = $(__cl_no_undef_$(mk_CC))#         < force error reports for unresolved symbols
cl_arch_on  = $(__cl_arch_on_$(mk_CC))#          < force linker to include whole archives
cl_arch_off = $(__cl_arch_off_$(mk_CC))#         < disable including whole archives
cl_archives = $(cl_arch_on) $1 $(cl_arch_off)#   < option frame for linking whole archives


#-- targets --

cpp,*_doc = preprocess file to stdout. Directories have to be separated by \\\\, e.g. make cpp,src\\\\main.cpp
cpp,%:
	$(mk_MAKE) --quiet $(subst \,/,$*)
	$(call __cc_cmd_cpp,$(subst \,/,$*))


#-- define compiler switches --

__cc_gcc          := g++
__cc_version_gcc  := --version
__cc_c_gcc        := -c
__cc_g_gcc        := -ggdb
__cc_O0_gcc       := -O0
__cc_O1_gcc       := -O1
__cc_O2_gcc       := -O2
__cc_O3_gcc       := -O3
__cc_o_gcc        := -o
__cc_m_gcc        := -m
__cc_omp_gcc      := -fopenmp
__cc_fpe_0_gcc    := -ftrapping-math -fsignaling-nans
__cc_fpe_1_gcc    := -ftrapping-math
__cc_fpe_3_gcc    :=
__cc_fpe_gcc       = $(__fc_fpe_$1_gcc)
__cc_pp_old_gcc   := -traditional-cpp
__cc_E_gcc        := -E
__cc_D_gcc        := -D
__cc_I_gcc        := -I
__cc_L_gcc        := -L
__cc_l_gcc        := -l
__cc_pic_gcc      := -shared -fPIC
__cc_threads_gcc  := -pthread
__cc_c++11_gcc    := -std=c++11
#
__cl_gcc          := g++
__cl_soname_gcc   := -Wl,-soname,
__cl_static_gcc   := -Wl,-static
__cl_rpath_gcc    := -Wl,-rpath,
__cl_no_undef_gcc := -Wl,--no-undefined
__cl_arch_on_gcc  := -Wl,--whole-archive
__cl_arch_off_gcc := -Wl,--no-whole-archive

#-- derive private flaglists --

__cc_file_types     := c cpp c++

__cc_pp_defines      = $(mk_CC_PP_DEFINES:%=$(cc_D)%)
__cc_include_dirs    = $(patsubst %,$(cc_I)%,$(mk_CC_INCLUDE_DIRS))

__cc_cflags__        = $(mk_CC_FLAGS) $(mk_CC_CFLAGS) $(call mk_get,$(basename $1))
__cc_cflags          = $(__cc_include_dirs) $(__cc_pp_defines) $(call __cc_cflags__,$1)
__cc_cflags_of       = $(call __cc_cflags,$1) $(call mk_fileType_opts,$1)

__cc_cmd_cpp         = $(cc) $(cc_E) $(call __cc_cflags_of,$(notdir $1)) $1
__cc_cmd_compile     = $(cc) $(cc_c) $(call __cc_cflags_of,$(notdir $<)) $< $(cc_o) $@

__cc_library_dirs    = $(call uniq,$(patsubst %,$(cc_L)%,$(mk_BUILD_DIR) $(mk_CC_LIBRARY_DIRS)))
__cc_libraries       = $(patsubst %,$(cc_l)%,$(mk_CC_LIBRARIES))
__cc_lflags          = $(mk_CC_LFLAGS) $(mk_CC_FLAGS) $(__cc_library_dirs)
__cc_object_archive  = $(mk_BUILD_DIR)/.mk.objects.a


define cc_cmd_link.exe
	$(call mk_create_archive,$(__cc_object_archive),$2)
	$(call mk_logged_cmd,$(cc) $(cc_o) $(mk_OUT_FILE) $(__cc_lflags) $(mk_OBJECT_ARCHIVE) $(__cc_libraries) $(mk_CC_LINK_OTHER))
	$(call mk_collect_so,$(mk_CC_LIBRARY_DIRS),$(mk_CC_LIBRARIES))
endef

define cc_cmd_link.shared
	$(call mk_create_archive,$(__cc_object_archive),$2)
	$(call mk_logged_cmd,$(cc) $(cc_o) $(mk_OUT_FILE) $(__cc_lflags) $(call cl_archives,$(mk_OBJECT_ARCHIVE)) $(__cc_libraries) $(mk_CC_LINK_OTHER))
	$(call mk_symlink_so,$(mk_OUT_FILE))
	$(call mk_collect_so,$(mk_CC_LIBRARY_DIRS),$(mk_CC_LIBRARIES))
endef

define cc_cmd_link.static
	$(call mk_create_archive,$1,$2,$(mk_BUILD_DIR),$(mk_CC_LIBRARIES))
	$(call mk_collect_so,$(mk_CC_LIBRARY_DIRS),$(mk_CC_LIBRARIES))
endef


$(mk_BUILD_DIR)/%.o: %.c
	@$(call mk_logged_cmd,$(__cc_cmd_compile))

$(mk_BUILD_DIR)/%.o: %.cpp
	@$(call mk_logged_cmd,$(__cc_cmd_compile))

endif # __mk_cpp_included

