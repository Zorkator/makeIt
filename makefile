
###
# makefile for creating initial project makefiles
# command:
# 	make -f <makeit.dir>/makefile makefile
#

_here       = $(abspath $(dir $(firstword $(MAKEFILE_LIST))))
_makefiles  = makefile Makefile
_makefilesP = $(patsubst %,\%/%,$(_makefiles))

$(_makefiles):
	$(call mk_makefile,$@)

$(_makefilesP):
	$(call mk_makefile,$@)

# $(call mk_makefile,PATH_MAKEFILE)
define mk_makefile
	$(eval ___name       := $(notdir $(mk_pwd)))
	$(eval mk_FILE_TYPES := $(__cc_file_types))
	$(eval _c_src_dirs   := $(dir $(call scan_files_in,.)))
	$(eval mk_FILE_TYPES := $(__fc_file_types))
	$(eval _f_src_dirs   := $(dir $(call scan_files_in,.)))
	$(eval ___src_dirs   := $(call uniq,$(sort $(_c_src_dirs) $(_f_src_dirs))))
	$(eval ___lang_types := $(if $(_c_src_dirs),c++,) $(if $(_f_src_dirs),fortran,))
	$(eval ___include    := $(foreach t,$(___lang_types),include $$$$(MAKEIT_DIR)/mk.$t\n))

	sed    -e 's#{MAKEIT_DIR}#$(_here)#g' < $(_here)/makefile.template > $1
	sed -i -e 's#{SOURCE_DIRS}#$(___src_dirs)#g'                         $1
	sed -i -e 's#{NAME}#$(___name)#g'                                    $1
	sed -i -e 's#{INCLUDE_TYPE}#$(___include)#g'                         $1
endef

include $(_here)/mk.fortran
include $(_here)/mk.c++

