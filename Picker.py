# Picker
# DOBOT_1
# Final Code
# Last edition 9/7/1019
# Last editor Hossein

import requests

from dobot_helper import *
from position import *
from msvcrt import *

MODE_INIT = "init"
MODE_READY = "ready"
MODE_POSITIONING = "positioning"
MODE_RUNNING = "running"

NO_COMMAND = "nothing"
EXIT_COMMAND = "^"
START_COMMAND = "s"
RESET_COMMAND = "r"
SERVER_RESET_COMMAND = "z"
CONNECT_COMMAND = "c"
POSITIONING_COMMAND = "p"
SET_STOCK_POS_COMMAND = "1"
SET_RELEASE_POS_COMMAND = "2"
HOME_COMMAND = "h"

com_port = "COM10"

box_number = 0

delayTime = 3000

release_gap = 6
r_head = -50

box_size = Position(29, 29, 25, 0)

stock_first_position = Position(111, 183.5, 10, r_head)
release_position = Position(200, -22, 24, r_head)


def server_reset():
    requests.get('http://127.0.0.1:5000/reset')


def get_status(dobot_number):
    r = requests.get('http://127.0.0.1:5000/status', params={'name': dobot_number, 'status': "NO_CHANGE"}).json()
    return r


def set_status(dobot_number, status):
    requests.get('http://127.0.0.1:5000/status', params={'name': dobot_number, 'status': status})


def get_admin_command():
    if kbhit():
        return getch()
    return NO_COMMAND


def init_routine(command):
    if command == NO_COMMAND:
        pass
    elif command == CONNECT_COMMAND:
        if connect(com_port):
            print "connected to picker!"
            dType.SetQueuedCmdClear(api)
            dType.SetQueuedCmdStartExec(api)
            dType.SetHOMEParams(api, 180, 0, 40, -78)  # Home Parameters ..............................................
            dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdClear(api)
            init_picker()
            print "picker ready!!!"
            return MODE_READY
        else:
            print "cannot connect to picker!"
    else:
        print "cannot execute " + command + " command in " + MODE_INIT + " mode!"
    return MODE_INIT


def ready_routine(command):
    global box_number
    if command == NO_COMMAND:
        pass
    elif command == HOME_COMMAND:
        print "going home!"
        goto_home()
        print "at home!"
    elif command == CONNECT_COMMAND:
        disconnect()
        print "disconnected from picker!"
        return MODE_INIT
    elif command == RESET_COMMAND:
        box_number = 0
        print "picker reset"
    elif command == SERVER_RESET_COMMAND:
        server_reset()
        print "server has been reset"
    elif command == POSITIONING_COMMAND:
        print "separator positioning started!"
        return MODE_POSITIONING
    elif command == START_COMMAND:
        start_conveyor()
        print "picker resumed!"
        return MODE_RUNNING
    else:
        print "cannot execute " + command + " command in " + MODE_READY + " mode!"
    return MODE_READY


def positioning_routine(command):
    global stock_first_position
    global release_position

    if command == NO_COMMAND:
        pass
    elif command == POSITIONING_COMMAND:
        print "separator positioning finished!"
        return MODE_READY
    elif command == SET_STOCK_POS_COMMAND:
        stock_first_position = get_current_position().change_r(r_head)
        print "stock first position set to " + str(stock_first_position)
    elif command == SET_RELEASE_POS_COMMAND:
        release_position = get_current_position().change_r(r_head).sum_z(box_size.z + release_gap)
        print "release position set to " + str(release_position)
    else:
        print "cannot execute " + command + " command in " + MODE_POSITIONING + " mode!"
    return MODE_POSITIONING


def running_routine(command):
    global box_number
    if command == NO_COMMAND:
        if get_status("DOBOT_2") == "IN_STOCK":
            wait_ms(3800)
        elif get_status("DOBOT_2") == "READY_TO_GRAB":
            pass
        else:
            return MODE_RUNNING
        pick(box_number)
        box_number += 1
        if box_number == 27:
            print "picker stock finished"
            stop_conveyor()
            return MODE_READY
    elif command == START_COMMAND:
        stop_conveyor()
        print "picker paused!"
        return MODE_READY
    else:
        print "cannot execute " + command + " command in " + MODE_RUNNING + " mode!"
    return MODE_RUNNING


def pick(box_num):
    start_time = time.time()
    x = (int((box_num % 9) / 3))
    y = ((box_num % 9) % 3)
    z = (int(box_num / 9))
    print "picking " + str(x) + " , " + str(y) + " , " + str(z)
    box_position = stock_first_position.clone().sum(box_size.clone().multiply(-x, y, -z))
    box_above_position = box_position.clone().change_z(release_position.z)

    jump(box_position)
    pump_grab()
    move(box_above_position)
    move(release_position)
    pump_release()
    wait_ms(delayTime)

    print("--- %s seconds ---" % (time.time() - start_time))


def main():
    mode = MODE_INIT
    while True:
        command = get_admin_command()
        if command == EXIT_COMMAND:
            break
        if mode == MODE_INIT:
            mode = init_routine(command)
        elif mode == MODE_READY:
            mode = ready_routine(command)
        elif mode == MODE_POSITIONING:
            mode = positioning_routine(command)
        elif mode == MODE_RUNNING:
            mode = running_routine(command)


def exit_handler():
    pump_release()
    disconnect()


if __name__ == "__main__":
    try:
        main()
    finally:
        exit_handler()

# SERVER ADDED..............................
