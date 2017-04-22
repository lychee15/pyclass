#!/bin/bash
# -*-coding=utf-8-*-
import re
import sys
import os
import MySQLdb
from util.schemas import *

reload(sys)
sys.setdefaultencoding('utf-8')


class MakeModel(object):
    def __init__(self):
        self._clzss = u'新闻'
        self._modelfile = sys.path[0] + '/model/' + self._clzss + '.txt'
        self._host = xinrui['host']
        self._port = xinrui['port']
        self._user = xinrui['user']
        self._passwd = xinrui['passwd']
        self._db = 'demo_web'

    def make_model(self):
        try:
            result = file(self._modelfile, 'w+')
            keyword_set = self.get_keyword()
            if keyword_set != 0:
                for label, keyword, newword in keyword_set:
                    words = set(filter(lambda s: s and s.strip(), (str(keyword) + ',' + str(newword)).replace('None', '').split(',')))
                    for word in words:
                        result.write(label + ',' + word + '\n')
            result.close()
        except Exception, e:
            result.close()
            os.remove(self._modelfile)
            print Exception, ":", e

    def get_keyword(self):
        try:
            conn = MySQLdb.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd, db=self._db, charset='utf8')
            cur = conn.cursor()
            result_set = cur.fetchmany(cur.execute(
                'SELECT '
                'label,keyword,newword '
                'FROM '
                'demo_web.model '
                'WHERE '
                'clzss = "{0}" '
                'AND '
                '('
                'keyword IS NOT NULL AND keyword != "" '
                'OR '
                'newword IS NOT NULL AND newword != ""'
                ')'.format(self._clzss)
            ))
            conn.commit()
            return result_set
        except Exception, e:
            print Exception, ":", e
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    bayes = MakeModel()
    bayes.make_model()
