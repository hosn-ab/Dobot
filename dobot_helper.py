import DobotDllType as dType
import time
from position import Position

api = dType.load()


def connect(com_port):
    #time.sleep(15)
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    state = dType.ConnectDobot(api, com_port, 115200)[0]
    print("Connect status:", CON_STR[state])

    if state == dType.DobotConnect.DobotConnect_NoError:
        dType.SetQueuedCmdClear(api)
        return True
    return False


def disconnect():
    dType.DisconnectDobot(api)


def start_conveyor():
    dType.SetQueuedCmdStartExec(api)
    dType.SetEMotorEx(api, 0, 1, 283 * 50)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def stop_conveyor():
    dType.SetQueuedCmdStartExec(api)
    dType.SetEMotorEx(api, 0, 0, 0)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def led_on():
    dType.SetQueuedCmdStartExec(api)
    dType.SetIODOEx(api, 18, 0)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def led_off():
    dType.SetQueuedCmdStartExec(api)
    dType.SetIODOEx(api, 18, 1)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def init_middle_sensor():
    dType.SetQueuedCmdStartExec(api)
    dType.SetIOMultiplexingEx(api, 18, 3)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def init_color_sensor():
    dType.SetQueuedCmdStartExec(api)
    dType.SetColorSensor(api, 1, 1)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def init_pick_check_sensor():
    dType.SetQueuedCmdStartExec(api)
    dType.SetIOMultiplexingEx(api, 20, 3)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def get_color_data():
    return dType.GetColorSensor(api)


def is_picked():
    return dType.GetIODI(api, 20)[0] == 0


def is_passed():
    return dType.GetIODI(api, 18)[0] == 0


def pump_grab():
    dType.SetQueuedCmdStartExec(api)
    dType.SetEndEffectorSuctionCupEx(api, 1, 1)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def pump_release():
    dType.SetQueuedCmdStartExec(api)
    dType.SetEndEffectorSuctionCupEx(api, 1, 0)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def grabber_close():
    dType.SetQueuedCmdStartExec(api)
    dType.SetEndEffectorGripperEx(api, 1, 1)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def grabber_open():
    dType.SetQueuedCmdStartExec(api)
    dType.SetEndEffectorGripperEx(api, 1, 0)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def start_queue():
    dType.SetQueuedCmdStartExec(api)


def clear_queue():
    dType.SetQueuedCmdClear(api)


def stop_queue():
    dType.SetQueuedCmdStopExec(api)


def wait_ms(t_ms):
    time.sleep(t_ms / 1000.0)


def move(p):
    dType.SetQueuedCmdStartExec(api)
    dType.SetPTPCmdEx(api, 1, p.x, p.y, p.z, p.r)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def jump(p):
    dType.SetQueuedCmdStartExec(api)
    dType.SetPTPCmdEx(api, 0, p.x, p.y, p.z, p.r)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def get_current_position():
    p = dType.GetPose(api)
    return Position(p[0], p[1], p[2], p[3])


def goto_home():
    dType.SetQueuedCmdClear(api)
    dType.SetQueuedCmdStartExec(api)
    dType.SetHOMECmdEx(api, 0)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)


def init_picker():
    current_pos = get_current_position()
    if get_current_position().z > 40:
        position_to_go_home = current_pos
    else:
        position_to_go_home = current_pos.clone().sum_z(50 - current_pos.z)

    move(position_to_go_home)

    goto_home()
    pass


def init_color_detector():
    goto_home()
    start_queue()
    init_color_sensor()
    init_middle_sensor()
    init_pick_check_sensor()
    stop_queue()
    clear_queue()
