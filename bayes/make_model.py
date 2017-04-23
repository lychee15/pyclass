#!/bin/bash
# -*-coding=utf-8-*-
import re
import sys
import os
import MySQLdb
from util.schemas import *
from util.encrypt import *

reload(sys)
sys.setdefaultencoding('utf-8')


class MakeModel(object):
    def __init__(self, clazz):
        self._clzss = clazz
        self._modelfile = sys.path[0] + '/model/' + Encrypt.hmacmd5(self._clzss) + '.txt'
        self._host = xinrui['host']
        self._port = xinrui['port']
        self._user = xinrui['user']
        self._passwd = xinrui['passwd']
        self._db = xinrui['db']

    def make_model(self):
        try:
            result = file(self._modelfile, 'w+')
            keyword_set = self.get_keyword()
            for label, keyword, newword in keyword_set:
                words = set(filter(lambda s: s and s.strip(), (str(keyword) + ',' + str(newword)).replace('None', '').split(',')))
                for word in words:
                    result.write(label + ' ' + word + '\n')
            result.close()
        except Exception, e:
            result.close()
            os.remove(self._modelfile)
            print Exception, ":", e
            exit(0)

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
            cur.close()
            conn.commit()
            conn.close()
            return result_set
        except Exception, e:
            print Exception, ":", e
            exit(0)


if __name__ == '__main__':
    bayes = MakeModel('新闻')
    bayes.make_model()
