# Assembler
# DOBOT_3
# Final Code
# Last edition 9/7/1019
# Last editor Hossein

from dobot_helper import *
from position import *
import requests
from msvcrt import *

com_port = "COM19"

connect(com_port)
dType.SetQueuedCmdClear(api)
dType.SetQueuedCmdStartExec(api)
dType.SetHOMEParams(api, 150, 5.5, 20, -20)
dType.SetQueuedCmdStopExec(api)
dType.SetQueuedCmdClear(api)


def get_color_number():
    r = requests.get('http://127.0.0.1:5000/get_color')
    color_holder_json = r.json()
    color_holder = [int(color_holder_json['RED']),
                    int(color_holder_json['GREEN']),
                    int(color_holder_json['BLUE'])]
    return color_holder


def decrease_color_number(color):
    requests.get('http://127.0.0.1:5000/color_minus', params={'color': color})


def get_status(dobot_number):
    r = requests.get('http://127.0.0.1:5000/status', params={'name': dobot_number, 'status': "NO_CHANGE"}).json()
    return r


def set_status(dobot_number, status):
    requests.get('http://127.0.0.1:5000/status', params={'name': dobot_number, 'status': status})


def get_stock_status():
    r = requests.get('http://127.0.0.1:5000/stock_status', params={'status': "NO_CHANGE"}).json()
    return r


def set_stock_status(status):
    requests.get('http://127.0.0.1:5000/stock_status', params={'status': status})


def is_in_place():
    r = requests.get('http://127.0.0.1:5000/double_stock', params={'is_in_place': "-1", 'get_or_set': "GET"}).json()
    return r


def set_is_in_place(place_status):
    requests.get('http://127.0.0.1:5000/double_stock', params={'is_in_place': place_status, 'get_or_set': "SET"})


def set_finish_time_occupancy(start_time, offset):
    finish_time = str(start_time + offset)
    requests.get('http://127.0.0.1:5000/time', params={'finish_time': finish_time})


def get_finish_time_occupancy():
    r = requests.get('http://127.0.0.1:5000/time', params={'finish_time': "-1"}).json()
    return float(r)


def get_current_time():
    return time.time()


def print_status():
    requests.get('http://127.0.0.1:5000/print_status')


def get_admin_command():
    if kbhit():
        return getch()
    return "NO_COMMAND"


# current_pos = get_current_position()
# if get_current_position().z > 40:
#     position_to_go_home = current_pos
# else:
#     position_to_go_home = current_pos.clone().sum_z(50 - current_pos.z)

# move(position_to_go_home)
goto_home()

r_head = -20
box_size = 35
cube_size = 24
delay_time = 1500

color_RGB_position = [Position(24, 252, -39, r_head), Position(24, 214, -39, r_head),
                      Position(24, 175, -39, r_head)]
rail_position = Position(136, 5.5, -8, r_head)  # Somewhere fix to locate
release_position = Position(186.5, -88, 33, r_head)

first_position = Position(180, 50, 37, r_head)

set_status(dobot_number="DOBOT_3", status="HOLD")

mode = "5G"

on_change = 0
offset = 6.5


while True:
    command = get_admin_command()
    if command == "q":
        mode = "5G"
        print "MODE 5G Selected"
    elif command == "w":
        print "MODE 4G Selected"
        mode = "4G"
    if mode == "5G":
        move(first_position)
        color_number_holder = get_color_number()
        if color_number_holder[0] > 1:
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[0].clone().sum_x(- box_size * (get_color_number()[0] - 1)))
            pump_grab()
            decrease_color_number("RED")
            if is_in_place() == "0":
                jump(first_position)
            while True:
                if is_in_place() == "0":
                    continue
                break
            jump(release_position)
            pump_release()
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[0].clone().sum_x(- box_size * (get_color_number()[0] - 1)))
            pump_grab()
            decrease_color_number("RED")
            jump(release_position.clone().sum_x(42))
            pump_release()
            move(release_position.clone().sum_z(30).clone().sum_x(42))
            set_is_in_place("0")
            move(first_position)
        if color_number_holder[1] > 1:
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[1].clone().sum_x(- box_size * (get_color_number()[1] - 1)))
            pump_grab()
            decrease_color_number("GREEN")
            if is_in_place() == "0":
                jump(first_position)
            while True:
                if is_in_place() == "0":
                    continue
                break
            jump(release_position.clone())
            pump_release()
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[1].clone().sum_x(- box_size * (get_color_number()[1] - 1)))
            pump_grab()
            decrease_color_number("GREEN")
            jump(release_position.clone().sum_x(42))
            pump_release()
            move(release_position.clone().sum_z(30).clone().sum_x(42))
            set_is_in_place("0")
            move(first_position)
        if color_number_holder[2] > 1:
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[2].clone().sum_x(- box_size * (get_color_number()[2] - 1)))
            pump_grab()
            decrease_color_number("BLUE")
            if is_in_place() == "0":
                jump(first_position)
            while True:
                if is_in_place() == "0":
                    continue
                break
            jump(release_position)
            pump_release()
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[2].clone().sum_x(- box_size * (get_color_number()[2] - 1)))
            pump_grab()
            decrease_color_number("BLUE")
            jump(release_position.clone().sum_x(42))
            pump_release()
            move(release_position.clone().sum_z(30).clone().sum_x(42))
            set_is_in_place("0")
            move(first_position)
    elif mode == "4G":
        move(first_position)
        color_number_holder = get_color_number()
        if color_number_holder[0] > 1:
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[0].clone().sum_x(- box_size * (get_color_number()[0] - 1)))
            pump_grab()
            decrease_color_number("RED")
            if is_in_place() == "0":
                jump(first_position)
            while True:
                if is_in_place() == "0":
                    continue
                break
            jump(release_position)
            pump_release()
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[0].clone().sum_x(- box_size * (get_color_number()[0] - 1)))
            pump_grab()
            decrease_color_number("RED")
            jump(release_position.clone().sum_x(42))
            pump_release()
            move(release_position.clone().sum_z(30).clone().sum_x(42))
            set_is_in_place("0")
            move(first_position)
        if color_number_holder[1] > 1:
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[1].clone().sum_x(- box_size * (get_color_number()[1] - 1)))
            pump_grab()
            decrease_color_number("GREEN")
            if is_in_place() == "0":
                jump(first_position)
            while True:
                if is_in_place() == "0":
                    continue
                break
            jump(release_position.clone())
            pump_release()
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[1].clone().sum_x(- box_size * (get_color_number()[1] - 1)))
            pump_grab()
            decrease_color_number("GREEN")
            jump(release_position.clone().sum_x(42))
            pump_release()
            move(release_position.clone().sum_z(30).clone().sum_x(42))
            set_is_in_place("0")
            move(first_position)
        if color_number_holder[2] > 1:
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[2].clone().sum_x(- box_size * (get_color_number()[2] - 1)))
            pump_grab()
            decrease_color_number("BLUE")
            if is_in_place() == "0":
                jump(first_position)
            while True:
                if is_in_place() == "0":
                    continue
                break
            jump(release_position)
            pump_release()
            while True:
                if get_current_time() < get_finish_time_occupancy():
                    continue
                break
            set_finish_time_occupancy(start_time=time.time(), offset=offset)
            jump(color_RGB_position[2].clone().sum_x(- box_size * (get_color_number()[2] - 1)))
            pump_grab()
            decrease_color_number("BLUE")
            jump(release_position.clone().sum_x(42))
            pump_release()
            move(release_position.clone().sum_z(30).clone().sum_x(42))
            set_is_in_place("0")
            move(first_position)

# SERVER ADDED
