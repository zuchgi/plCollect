#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 连接池
import redis
import devInfo

redis_server = devInfo.get_redis()
# 拿到一个redis的连接池
pool = redis.ConnectionPool(host=redis_server['host'],
                            port=redis_server['port'],
                            password=redis_server['password'],
                            max_connections=50)

# 从池子中拿一个链接
conn = redis.Redis(connection_pool=pool, decode_responses=True)


def save(name, data, ttl):
    conn.set(name, str(data), ex=ttl)


def read(name):
    conn.get(name)
