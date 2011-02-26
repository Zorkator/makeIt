####
# compiler & tools
##
CC       = gcc
CPPC     = g++
LINK     = g++
AR       = ar

mk_CC              = $(CC)
mk_CPPC            = $(CPPC)
mk_CXX_FLAGS       = $(_CXX_FLAGS) $(CXX_FLAGS) -DREVISION_ID="$(mk_REVISION_ID)" -DREVISION_DATE="$(mk_REVISION_DATE)"
mk_C_FLAGS         = $(_C_FLAGS) $(C_FLAGS) $(C_FLAGS_$(_CONF)) $(mk_CXX_FLAGS) $(mk_TARGET_FLAGS)
mk_CPP_FLAGS       = $(_CPP_FLAGS) $(CPP_FLAGS) $(CPP_FLAGS_$(_CONF)) $(mk_CXX_FLAGS) $(mk_TARGET_FLAGS)

mk_C_SOURCE      = $(C_SOURCE)
mk_C_OBJECTS     = $(mk_C_SOURCE:%.c=$(_CONF)/%.o)
mk_CPP_SOURCE    = $(CPP_SOURCE) $(MOC_SOURCE) $(mk_MOC_CPP_GEN) $(mk_UIC_CPP_GEN)
mk_CPP_OBJECTS   = $(mk_CPP_SOURCE:%.cpp=$(_CONF)/%.o)
#-- c files --
$(_CFG)/%.o : %.c
	$(CC) $(mk_INCLUDE_PATHLIST) $(mk_C_FLAGS) -c $< -o $@

#-- c++ files --
$(_CFG)/%.o : %.cpp
	$(CPPC) $(mk_INCLUDE_PATHLIST) $(mk_CPP_FLAGS) -c $< -o $@

