#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import devInfo
import iCounter
import serial
from modbus_tk import modbus_rtu

logging.basicConfig(level=logging.ERROR)

device = []

if __name__ == '__main__':

    # 获取设备list，从配置信息config.json
    _dev_array = devInfo.get_dev()
    # 设定串口从站
    client = modbus_rtu.RtuMaster(serial.Serial(port='COM3', baudrate=9600, bytesize=8, parity='N', xonxoff=0))
    client.set_timeout(5.0)
    client.set_verbose(True)
    for _dev in _dev_array:
        device.append(iCounter.BaseDevice(_dev['DeviceName'],
                                          devInfo.get_time()['telemetry'],
                                          _dev["modbus_slave_id"],
                                          client
                                          ),
                      )
        logging.info("dev : %s installed !" % str(_dev['DeviceName']))
        device[-1].update()
        # device[-1].reconnect()
