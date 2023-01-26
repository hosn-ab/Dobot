# Final Code
# Last edition 9/7/1019
# Last editor Hossein

import json
import jsonpickle
from flask import Flask, request
from DataHandler import MiddleStockData, DobotsConditions, StockConditions, DoubleStockCondition, Alarm
import logging
import time

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

stock = MiddleStockData.getInstance()
condition = DobotsConditions.getInstance()
stock_condition = StockConditions.getInstance()
double_stock = DoubleStockCondition.getInstance()
alarm = Alarm.getInstance()


@app.route('/color_plus')
def color_plus():
    color = request.args.get("color")
    if color == "RED":
        count = stock.get_red_number()
        count = count + 1
        stock.set_red_number(count)
    if color == "GREEN":
        count = stock.get_green_number()
        count = count + 1
        stock.set_green_number(count)
    if color == "BLUE":
        count = stock.get_blue_number()
        count = count + 1
        stock.set_blue_number(count)
    return "1"


@app.route('/color_minus')
def color_minus():
    color = request.args.get("color")
    if color == "RED":
        count = stock.get_red_number()
        count = count - 1
        stock.set_red_number(count)
    if color == "GREEN":
        count = stock.get_green_number()
        count = count - 1
        stock.set_green_number(count)
    if color == "BLUE":
        count = stock.get_blue_number()
        count = count - 1
        stock.set_blue_number(count)
    return "1"


@app.route('/get_color')
def get_color():
    color_number = [stock.get_red_number(), stock.get_green_number(), stock.get_blue_number()]
    color_number_json = {'RED': str(color_number[0]),
                         'GREEN': str(color_number[1]),
                         'BLUE': str(color_number[2])}

    return json.dumps(color_number_json)


@app.route('/status')
def status():
    r = request.args
    current_status = r.get('status')
    dobot_number = r.get('name')
    if current_status == "NO_CHANGE":
        return json.dumps(condition.get_status(dobot_number))
    condition.set_status(dobot_number, current_status)
    return "1"


@app.route('/stock_status')
def stock_status():
    r = request.args
    current_status = r.get('status')
    if current_status == "NO_CHANGE":
        return json.dumps(stock_condition.get_status())
    stock_condition.set_status(current_status)
    return "1"


@app.route('/reset')
def server_reset():
    stock.set_red_number(0)
    stock.set_green_number(0)
    stock.set_blue_number(0)
    condition.set_status(dobot_number="DOBOT_1", status="HOLD")
    condition.set_status(dobot_number="DOBOT_2", status="READY_TO_GRAB")
    condition.set_status(dobot_number="DOBOT_3", status="HOLD")
    condition.set_status(dobot_number="DOBOT_4", status="HOLD")
    double_stock.set_is_in_place("0")
    return "1"


@app.route('/time')
def stock_time():
    r = request.args
    finish_time = r.get('finish_time')
    if finish_time == "-1":
        return json.dumps(str(stock_condition.get_finish_time_occupancy()))
    stock_condition.set_finish_time_occupancy(finish_time=float(finish_time))
    return "1"


@app.route('/double_stock')
def double_stock_condition():
    r = request.args
    get_or_set = r.get('get_or_set')
    place_status = r.get('is_in_place')
    if get_or_set == "GET":
        return json.dumps(double_stock.is_in_place())
    elif get_or_set == "SET":
        double_stock.set_is_in_place(place_status)
    return "1"


@app.route('/alarm')
def alarm_handler():
    r = request.args
    status = r.get('status')
    get_or_set = r.get('get_or_set')
    if get_or_set == "GET":
        return json.dumps(alarm.status)
    elif get_or_set == "SET":
        alarm.set_status(status)
    return "1"


@app.route('/Test')
def test():
    r = request.args
    name = r.get('name')
    kir = r.get('kir')
    if name == "hossein":
        print name
    if kir == "kos":
        print kir
    return "1"


@app.route('/print_status')
def print_status():
    print "Stock has " + str(stock.get_red_number()) + " Red Cubes \n" + str(stock.get_green_number()) + " Green Cubes \n" + str(stock.get_blue_number)() + " Blue Cubes"
    return "1"

if __name__ == '__main__':
    app.secret_key = "dobot"
    app.run()
