

MSG_LIST := $(MSG_LIST) $(MSG_NULL)
MSG_NULL  = "no\ message"

#--
# Message print target
#
$(MSG_LIST):
	@echo $@

