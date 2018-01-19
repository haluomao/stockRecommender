#!/usr/bin/python
# coding=UTF-8

import os
import time
import sys
import logging
import json
from crawlers import BaseCrawler
from util import fileUtil

class SinaCrawler(object):

    # Example: http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz002095&scale=60&ma=no&datalen=1023
    def __init__(self, symbol, scale=240, datalen=365,  baseUrl='http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'):
        self.baseUrl = baseUrl
        self.symbol = 'sz'+symbol if symbol.startswith('00') else 'sh'+symbol
        self.scale = scale
        self.ma = 'no'
        self.datalen = datalen
        self.url = '%s?symbol=%s&scale=%s&ma=%s&datalen=%s' % (self.baseUrl, self.symbol, self.scale, self.ma, self.datalen)

    def getJson(self):
        logging.info('getJson', self.url)
        crawler = BaseCrawler.BaseCrawler(self.url)
        return crawler.getPage()

    def parseJson(self, jsonData):
        pass


if __name__ == '__main__':
    stockCodes = fileUtil.readFile(sys.argv[1]).split('\n')
    dir = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if not os.path.exists(dir):
        os.mkdir(dir)
    for code in stockCodes:
        print 'Crawlering code:', code
        sinaCrawler = SinaCrawler(code)
        fileName = code+'_market_365.txt'
        fileUtil.writeFile(dir + '/' + fileName, sinaCrawler.getJson())

