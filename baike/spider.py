#!/bin/bash
# -*-coding=utf-8-*-
'''
    根据关键词爬取百度百科
    http://baike.baidu.com/search/word?word=  # 得到url的方法
'''
import urllib
import urllib2
from bs4 import BeautifulSoup
import jieba.analyse
import re
import MySQLdb
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


class Spider(object):
    def __init__(self):
        self._url = 'http://baike.baidu.com/search/word?word='  # 爬取链接
        self._encoding = 'utf-8'
        self._pattern = re.compile("[/.,/#@$%^& ]")
        self._topK = 30  # 关键词个数
        self._stopwords = sys.path[0] + '/stopwords.txt'  # 停用词位置
        self._host = 'localhost'
        self._port = 3306
        self._user = 'root'
        self._passwd = '8532936'
        self._db = 'demo_web'

    def craw(self, keyword):
        url = self.get_url(keyword)
        return self.passer(url, self.download(url))

    def get_url(self, keyword):
        return self._url + keyword

    def download(self, url):
        return urllib2.urlopen(url).read()

    def passer(self, url, html_count):
        soup = BeautifulSoup(html_count, 'html.parser', from_encoding=self._encoding)
        return self.get_content(soup)

    def get_content(self, soup):
        content = []
        summarys = soup.find_all('div', attrs={'class': 'para'})
        for summary in summarys:
            content.append(summary.getText())
        result = re.sub(self._pattern, '', ''.join(content))
        return self.get_keyword(result)

    def get_keyword(self, content):
        keys = jieba.analyse.extract_tags(content, topK=self._topK)
        stopwords = self.load_stop_words()
        keywords = ','.join(set(keys) - set(stopwords))
        return keywords

    def load_stop_words(self):
        stop_words = [line.strip().decode(self._encoding) for line in open(self._stopwords).readlines()]
        return stop_words

    def update(self):
        try:
            conn = MySQLdb.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd, db=self._db,
                                   charset='utf8')
            cur = conn.cursor()
            result = cur.execute('SELECT id,label FROM model WHERE keyword IS NULL OR keyword = ""')
            if result != 0:
                for id, label in cur.fetchmany(result):
                    cur.execute('UPDATE model SET keyword="{0}" WHERE id={1}'.format(self.craw(label), id))
            cur.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print Exception, ":", e


if __name__ == '__main__':
    spider = Spider()
    spider.update()