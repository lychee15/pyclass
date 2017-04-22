#!/bin/bash
# -*-coding=utf-8-*-
import re
import sys
import os


class MakeModel(object):
    def __init__(self):
        self._host = 'localhost'
        self._port = 3306
        self._user = 'root'
        self._passwd = '8532936'
        self._db = 'demo_web'
        self._clzss = '学习'
        pass

    def make_model(self):
        try:
            conn = MySQLdb.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd, db=self._db,
                                   charset='utf8')
            cur = conn.cursor()
            result = cur.execute('SELECT label,keyword,newword FROM model WHERE clzss = {0}'.format(self._clzss))
            if result != 0:
                for id, label in cur.fetchmany(result):
                    cur.execute('UPDATE model SET keyword="{0}" WHERE id={1}'.format(self.craw(label), id))
            cur.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print Exception, ":", e
        pass

    pass


if __name__ == '__main__':
    pass
