# -*- coding:utf-8 -*-
# !/usr/bin/python3
import pymysql
import devInfo
import time
import logging
mysql_server = devInfo.get_db()


def mysql_quary(sql):
    db = pymysql.connect(mysql_server['host'],
                         mysql_server['user'],
                         mysql_server['password'],
                         mysql_server['db_name'])
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # logging.error("%s",e)
        db.rollback()
    db.close()


def write_db(tb_name, sumFlowPA, sumFlowCA):
    sql_str = "INSERT INTO %s (date,sumFlowPA,sumFlowCA) VALUES (\"%s\",%f,%f)" \
              % (tb_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), sumFlowPA, sumFlowCA)
    mysql_quary(sql_str)
