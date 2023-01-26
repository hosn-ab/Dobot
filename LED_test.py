from dobot_helper import *
from position import *
import requests

com_port = "COM20"

connect(com_port)

# dType.SetQueuedCmdStartExec(api)
# dType.SetIOMultiplexingEx(api, 18, 1)
# dType.SetQueuedCmdStopExec(api)
# dType.SetQueuedCmdClear(api)
#
#
# print dType.GetIODO(api, 18)
#
#
# dType.SetQueuedCmdStartExec(api)
# dType.SetIOMultiplexingEx(api, 18, 3)
# dType.SetQueuedCmdStopExec(api)
# dType.SetQueuedCmdClear(api)

dType.SetQueuedCmdStartExec(api)
dType.SetIODOEx(api, 18, 1)
dType.SetQueuedCmdStopExec(api)
dType.SetQueuedCmdClear(api)