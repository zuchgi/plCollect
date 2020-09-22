#!/usr/bin/python
# -*- coding: UTF-8 -*-

import modbus_tk.defines as cst
import logging
from threading import Timer
import struct
import cache
import db


class BaseDevice(object):

    def __init__(self, name, update_period, address, client):
        self.name = name
        self.update_period = update_period
        self.is_online = False
        self.Flow = [0, 0]
        self.sumFlow = [0, 0]
        self.CA = [0, 0]
        self.sumCA = [0, 0]
        self.address = address
        self.client = client

    def update(self):
        buf = []
        # 创建 空list
        for i in range(32):
            buf.append(0)
        if True:
            self.is_online = True
            try:
                # 读取数据
                rsp_ = self.client.execute(self.address, cst.READ_HOLDING_REGISTERS, 150, 16)
                # 将读取的tuple 转换为 list 每元素2bytes
                temp_list = list(tuple(rsp_))
                # 拆解2 bytes的list为1 byte的list
                for i in range(8):
                    buf[i * 4 + 1] = temp_list[i*2+1].to_bytes(2, 'little')[0]
                    buf[i * 4 + 0] = temp_list[i*2+1].to_bytes(2, 'little')[1]
                    buf[i * 4 + 3] = temp_list[i*2].to_bytes(2, 'little')[0]
                    buf[i * 4 + 2] = temp_list[i*2].to_bytes(2, 'little')[1]
                # 将byte list转换为bytes
                temp_bytes = bytes(buf)
                # bytes 转换为 flaot

                self.Flow[0] = struct.unpack_from('>f', temp_bytes, 0)[0]
                self.sumFlow[0] = struct.unpack_from('>f', temp_bytes, 4)[0]
                self.CA[0] = struct.unpack_from('>f', temp_bytes, 8)[0]
                self.sumCA[0] = struct.unpack_from('>f', temp_bytes, 12)[0]

                self.Flow[1] = struct.unpack_from('>f', temp_bytes, 16)[0]
                self.sumFlow[1] = struct.unpack_from('>f', temp_bytes, 20)[0]
                self.CA[1] = struct.unpack_from('>f', temp_bytes, 24)[0]
                self.sumCA[1] = struct.unpack_from('>f', temp_bytes, 28)[0]
                logging.info("Flow" + str(self.Flow))
                logging.info("sumFlow" + str(self.sumFlow))
                logging.info("CA" + str(self.CA))
                logging.info("sumCA" + str(self.sumCA))

                cache.save("cat:%s:Flow0" % self.name, self.Flow[0], None)
                cache.save("cat:%s:Flow1" % self.name, self.Flow[1], None)
                cache.save("cat:%s:sumFlow0" % self.name, self.sumFlow[0], None)
                cache.save("cat:%s:sumFlow1" % self.name, self.sumFlow[1], None)
                cache.save("cat:%s:CA0" % self.name, self.CA[0], None)
                cache.save("cat:%s:CA1" % self.name, self.CA[1], None)
                cache.save("cat:%s:sumCA0" % self.name, self.sumCA[0], None)
                cache.save("cat:%s:sumCA1" % self.name, self.sumCA[1], None)
                if self.Flow[0] > 0:
                    db.write_db(self.name, self.sumFlow[0], self.sumCA[0])
            except:
                logging.error('dev : %s read reg error' % self.name)
        t = Timer(self.update_period, self.update)
        t.start()

    def reconnect(self):
        if not self.client.is_socket_open():
            self.is_online = False
            self.client.connect()
            logging.info('Connecting to %s' % self.name)
        t = Timer(self.reconnect_period, self.reconnect)
        t.start()
