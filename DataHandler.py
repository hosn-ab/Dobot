import threading

lock = threading.Lock()


class MiddleStockData:
    __instance = None
    RGB_count = [0, 0, 0]

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MiddleStockData.__instance == None:
            MiddleStockData()
        return MiddleStockData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MiddleStockData.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MiddleStockData.__instance = self

    def get_red_number(self):
        lock.acquire()
        count = self.RGB_count[0]
        lock.release()
        return count

    def get_green_number(self):
        lock.acquire()
        count = self.RGB_count[1]
        lock.release()
        return count

    def get_blue_number(self):
        lock.acquire()
        count = self.RGB_count[2]
        lock.release()
        return count

    def set_red_number(self, count):
        lock.acquire()
        self.RGB_count[0] = count
        lock.release()

    def set_green_number(self, count):
        lock.acquire()
        self.RGB_count[1] = count
        lock.release()

    def set_blue_number(self, count):
        lock.acquire()
        self.RGB_count[2] = count
        lock.release()


class DobotsConditions:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DobotsConditions.__instance == None:
            DobotsConditions()
        return DobotsConditions.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DobotsConditions.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DobotsConditions.__instance = self

    status_json = {'DOBOT_1': "HOLD",
                   'DOBOT_2': "READY_TO_GRAB",
                   'DOBOT_3': "HOLD",
                   'DOBOT_4': "HOLD"}

    def set_status(self, dobot_number, status):
        lock.acquire()
        self.status_json[dobot_number] = status
        lock.release()

    def get_status(self, dobot_number):
        return self.status_json[dobot_number]


class StockConditions:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if StockConditions.__instance == None:
            StockConditions()
        return StockConditions.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if StockConditions.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            StockConditions.__instance = self

    current_status = "FREE"
    start_occupancy = 0
    finish_occupancy = 0

    def set_status(self, current_status):
        lock.acquire()
        self.current_status = current_status
        lock.release()

    def get_status(self):
        return self.current_status

    def get_finish_time_occupancy(self):
        return self.finish_occupancy

    def set_finish_time_occupancy(self, finish_time):
        lock.acquire()
        self.finish_occupancy = finish_time
        lock.release()


class DoubleStockCondition:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DoubleStockCondition.__instance == None:
            DoubleStockCondition()
        return DoubleStockCondition.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DoubleStockCondition.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DoubleStockCondition.__instance = self

    place_status = "0"

    def is_in_place(self):
        return self.place_status

    def set_is_in_place(self, place_status):
        lock.acquire()
        self.place_status = place_status
        lock.release()


class Alarm:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Alarm.__instance == None:
            Alarm()
        return Alarm.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Alarm.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Alarm.__instance = self

    status = "OFF"

    def set_status(self, status):
        lock.acquire()
        self.status = status
        lock.release()
