import requests

from dobot_helper import *
from position import *
from msvcrt import *

connect("COM10")
stop_conveyor()
# com_port = "COM3"
#
# release_gap = 6
# r_head = -50
#
# box_size = Position(29, 29, 25, 0)
#
# stock_first_position = Position(111, 183.5, 10, r_head)
# release_position = Position(200, -22, 24, r_head)
#
# connect(com_port)
# # goto_home()
# jump(stock_first_position)
# pump_grab()
# jump(release_position)
# pump_release()
# com_port = "COM9"
#
# connect(com_port)
#
# # dType.SetQueuedCmdClear(api)
# # dType.SetQueuedCmdStartExec(api)
# dType.SetHOMEParams(api, 40, -225, 40, -50)
# # dType.SetQueuedCmdStopExec(api)
# # dType.SetQueuedCmdClear(api)
# # goto_home()
# current_pos = get_current_position()
# if get_current_position().z > 40:
#     position_to_go_home = current_pos
# else:
#     position_to_go_home = current_pos.clone().sum_z(50 - current_pos.z)
#
# # move(position_to_go_home)
#
# # goto_home()
# r_head = -50
# box_size = 35
# cube_size = 27
#
# infrared_sensor_position = Position(137, 200, 20, r_head)
# color_sensor_position = Position(123, 136.5, 12, r_head)
# color_RGB_position = [Position(19, -207, -30, r_head), Position(19, -243, -30, r_head),
#                       Position(21, -278, -30, r_head)]
# first_position = infrared_sensor_position.clone().change_x(201).clone().change_z(cube_size+5).clone().sum_y(10)
# grab_position = first_position.clone().sum(Position(3, -64, -17, 0))
# color_stop_position = color_sensor_position.clone().sum_z(cube_size)
# wait_position = Position(130, -160, 35, r_head)
#
#
# # init_color_sensor()
# init_pick_check_sensor()
# while True:
#     print is_picked()
#
#
# # jump(color_stop_position)
# # move(wait_position)
# # move(grab_position)
# disconnect()
#
#
