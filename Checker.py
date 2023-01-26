# Checker
# DOBOT_2
# Final Code
# Last edition 9/7/1019
# Last editor Hossein


from dobot_helper import *
from position import *
import requests
from msvcrt import *
import random


com_port = "COM9"

connect(com_port)
dType.SetQueuedCmdClear(api)
dType.SetQueuedCmdStartExec(api)
dType.SetHOMEParams(api, 40, -225, 40, -50)
dType.SetQueuedCmdStopExec(api)
dType.SetQueuedCmdClear(api)


def miss():
    x = random.random()
    if x > 0.3:
        return False
    else:
        return True


def get_color_number():
    r = requests.get('http://127.0.0.1:5000/get_color')
    color_holder_json = r.json()
    color_holder = [int(color_holder_json['RED']),
                    int(color_holder_json['GREEN']),
                    int(color_holder_json['BLUE'])]
    return color_holder


def increase_color_number(color):
    requests.get('http://127.0.0.1:5000/color_plus', params={'color': color})


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


current_pos = get_current_position()
if get_current_position().z > 40:
    position_to_go_home = current_pos
else:
    position_to_go_home = current_pos.clone().sum_z(50 - current_pos.z)

move(position_to_go_home)
goto_home()


r_head = -50
box_size = 35
cube_size = 27

infrared_sensor_position = Position(137, 200, 20, r_head)
color_sensor_position = Position(123, 136.5, 12, r_head)
color_RGB_position = [Position(19, -207, -30, r_head), Position(19, -243, -30, r_head),
                      Position(21, -278, -30, r_head)]
first_position = infrared_sensor_position.clone().change_x(201).clone().change_z(cube_size+5).clone().sum_y(10)
grab_position = first_position.clone().sum(Position(3, -64, -17, 0))
color_stop_position = color_sensor_position.clone().sum_z(cube_size)
wait_position = Position(130, -160, 35, r_head)
init_color_sensor()
init_pick_check_sensor()
init_middle_sensor()

jump(first_position)

set_status(dobot_number="DOBOT_2", status="READY_TO_GRAB")

mode = "5G"
delay_time = 2000
on_change = 0

wait_position_offset = 6.5
color_stop_position_offset = 6.5
predicted_time_offset = 3

wait_position_offset_4G = 8.5
color_stop_position_offset_4G = 8.5


while True:
    command = get_admin_command()
    if command == "q":
        mode = "5G"
        print "MODE 5G Selected"
    elif command == "w":
        mode = "4G"
        print "MODE 4G Selected"
    if mode == "5G":
        move(first_position)
        if is_passed():
            pump_grab()
            move(grab_position)
            set_status(dobot_number="DOBOT_2", status="READY_TO_PUT")
            move(color_stop_position)
            wait_ms(100)
            if is_picked():
                wait_ms(200)
                if get_color_data()[0] == 1:
                    if get_current_time() + predicted_time_offset < get_finish_time_occupancy():
                        move(wait_position)
                        while True:
                            if get_current_time() < get_finish_time_occupancy():
                                on_change = 1
                                continue
                            break
                    else:
                        set_finish_time_occupancy(start_time=time.time(), offset=color_stop_position_offset)
                    if on_change == 1:
                        set_finish_time_occupancy(start_time=time.time(), offset=wait_position_offset)
                        on_change = 0
                    set_status(dobot_number="DOBOT_2", status="IN_STOCK")
                    jump(color_RGB_position[0].clone().sum_x(-box_size * (get_color_number()[0])))
                    pump_release()
                    increase_color_number("RED")
                    jump(first_position)
                elif get_color_data()[1] == 1:
                    if get_current_time() + predicted_time_offset < get_finish_time_occupancy():
                        move(wait_position)
                        while True:
                            if get_current_time() < get_finish_time_occupancy():
                                on_change = 1
                                continue
                            break
                    else:
                        set_finish_time_occupancy(start_time=time.time(), offset=color_stop_position_offset)
                    if on_change == 1:
                        set_finish_time_occupancy(start_time=time.time(), offset=wait_position_offset)
                        on_change = 0
                    set_status(dobot_number="DOBOT_2", status="IN_STOCK")
                    jump(color_RGB_position[1].clone().sum_x(-box_size * (get_color_number()[1])))
                    pump_release()
                    increase_color_number("GREEN")
                    jump(first_position)
                elif get_color_data()[2] == 1:
                    if get_current_time() + predicted_time_offset < get_finish_time_occupancy():
                        move(wait_position)
                        while True:
                            if get_current_time() < get_finish_time_occupancy():
                                on_change = 1
                                continue
                            break
                    else:
                        set_finish_time_occupancy(start_time=time.time(), offset=color_stop_position_offset)
                    if on_change == 1:
                        set_finish_time_occupancy(start_time=time.time(), offset=wait_position_offset)
                        on_change = 0
                    set_status(dobot_number="DOBOT_2", status="IN_STOCK")
                    jump(color_RGB_position[2].clone().sum_x(-box_size * (get_color_number()[2])))
                    pump_release()
                    increase_color_number("BLUE")
                    jump(first_position)
            else:
                pump_release()
                set_status(dobot_number="DOBOT_2", status="READY_TO_GRAB")
    elif mode == "4G":
        move(first_position)
        if is_passed():
            pump_grab()
            if miss():
                wait_ms(300)
                move(grab_position.clone().sum_y(-20))
            else:
                move(grab_position)
            set_status(dobot_number="DOBOT_2", status="READY_TO_PUT")
            move(color_stop_position)
            wait_ms(100)
            if is_picked():
                wait_ms(200)
                if get_color_data()[0] == 1:
                    if get_current_time() + predicted_time_offset < get_finish_time_occupancy():
                        move(wait_position)
                        while True:
                            if get_current_time() < get_finish_time_occupancy():
                                on_change = 1
                                continue
                            break
                    else:
                        set_finish_time_occupancy(start_time=time.time(), offset=color_stop_position_offset_4G)
                    if on_change == 1:
                        set_finish_time_occupancy(start_time=time.time(), offset=wait_position_offset_4G)
                        on_change = 0
                    set_status(dobot_number="DOBOT_2", status="IN_STOCK")
                    jump(color_RGB_position[0].clone().sum_x(-box_size * (get_color_number()[0])))
                    pump_release()
                    increase_color_number("RED")
                    jump(first_position)
                elif get_color_data()[1] == 1:
                    if get_current_time() + predicted_time_offset < get_finish_time_occupancy():
                        move(wait_position)
                        while True:
                            if get_current_time() < get_finish_time_occupancy():
                                on_change = 1
                                continue
                            break
                    else:
                        set_finish_time_occupancy(start_time=time.time(), offset=color_stop_position_offset_4G)
                    if on_change == 1:
                        set_finish_time_occupancy(start_time=time.time(), offset=wait_position_offset_4G)
                        on_change = 0
                    set_status(dobot_number="DOBOT_2", status="IN_STOCK")
                    jump(color_RGB_position[1].clone().sum_x(-box_size * (get_color_number()[1])))
                    pump_release()
                    increase_color_number("GREEN")
                    jump(first_position)
                elif get_color_data()[2] == 1:
                    if get_current_time() + predicted_time_offset < get_finish_time_occupancy():
                        move(wait_position)
                        while True:
                            if get_current_time() < get_finish_time_occupancy():
                                on_change = 1
                                continue
                            break
                    else:
                        set_finish_time_occupancy(start_time=time.time(), offset=color_stop_position_offset_4G)
                    if on_change == 1:
                        set_finish_time_occupancy(start_time=time.time(), offset=wait_position_offset_4G)
                        on_change = 0
                    set_status(dobot_number="DOBOT_2", status="IN_STOCK")
                    jump(color_RGB_position[2].clone().sum_x(-box_size * (get_color_number()[2])))
                    pump_release()
                    increase_color_number("BLUE")
                    jump(first_position)
            else:
                pump_release()
                set_status(dobot_number="DOBOT_2", status="READY_TO_GRAB")

# SERVER ADDED..............................
