#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

# 获取用户设置
setting = json.load(open("D:/project/plCollect/config.json", encoding='utf-8'))


def get_dev():
    return setting['dev']


def get_redis():
    return setting['redis']


def get_db():
    return setting['db']


def is_debug():
    return setting['isDebug']


def get_time():
    return setting['time']
