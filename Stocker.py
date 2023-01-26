# Stocker
# DOBOT 4
# Final Code
# Last edition 9/7/1019
# Last editor Hossein

from dobot_helper import *
from position import *
import requests
from msvcrt import *

com_port = "COM20"

connect(com_port)
dType.SetQueuedCmdClear(api)
dType.SetQueuedCmdStartExec(api)
dType.SetHOMEParams(api, 207, 0, 70, -65)
dType.SetQueuedCmdStopExec(api)
dType.SetQueuedCmdClear(api)

goto_home()

r_head = -65
stock_position = [Position(63, -171.5, -15, r_head), Position(-25, -171.5, -15, r_head),
                  Position(63, -214, -15, r_head), Position(-25, -214, -15, r_head)]
release_position = Position(207, 215, 47, r_head)
first_position = Position(207, 0, 70, r_head)
stock_number = 0


def pick(stock_num):
    grabber_open()
    wait_ms(400)
    pump_release()
    move(stock_position[stock_num].clone().sum_z(50))
    move(stock_position[stock_num])
    grabber_close()
    wait_ms(400)
    move(stock_position[stock_num].clone().sum_z(70))
    move(release_position.clone().change_y(stock_position[stock_num].y).clone().sum_z(40))
    move(release_position.clone().sum_z(40))
    move(release_position)
    grabber_open()
    wait_ms(400)
    pump_release()
    wait_ms(200)
    move(release_position.clone().sum_z(40))


def get_status(dobot_number):
    r = requests.get('http://127.0.0.1:5000/status', params={'name': dobot_number, 'status': "NO_CHANGE"}).json()
    return r


def set_is_in_place(place_status):
    requests.get('http://127.0.0.1:5000/double_stock', params={'is_in_place': place_status, 'get_or_set': "SET"})


def is_in_place():
    r = requests.get('http://127.0.0.1:5000/double_stock', params={'is_in_place': "-1", 'get_or_set': "GET"}).json()
    return r


on_change = 1

while True:
    move(first_position)

    while True:
        if is_in_place() == "1":
            continue
        break
    start_conveyor()
    wait_ms(500)
    stop_conveyor()
    pick(stock_number)
    on_change = 0
    stock_number = stock_number + 1
    set_is_in_place("1")

