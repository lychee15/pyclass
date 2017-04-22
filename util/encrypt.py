#!/bin/bash
# -*-coding=utf-8-*-
import hashlib
import types
import sys
import hmac

reload(sys)
sys.setdefaultencoding('utf-8')

HMA_CMD5 = "qwertyuiopasdfghjklzxcvbnm"


def hmacmd5(str):
    '''
    hmacmd5加密字符串
    :param str:
    :return:
    '''
    if type(str) is types.StringType:
        return hmac.new(HMA_CMD5, str, hashlib.md5).hexdigest()
    else:
        return ''


if __name__ == '__main__':
    print hmacmd5('新闻')
