#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import time
import datetime
from crawlers import SinaCrawler
from stock import Macd, Analysis
from util import fileUtil

dataDir = "./data/"
patchDir = dataDir + 'patchs/'
rawDir = dataDir + 'raw/'
macdDir = dataDir + 'macd/'
recDir = dataDir + 'rec/'
stockFile = 'stockCode.txt'

dateFormat = '%Y%m%d'
today = time.strftime(dateFormat,time.localtime(time.time()))

def getDaysBetween(begin, end):
    beginDate = datetime.strptime(begin, dateFormat)
    endDate = datetime.strptime(end, dateFormat)
    return (endDate - beginDate).days

def format(data):
    arr = ['day', 'close', 'open', 'high', 'low', 'volume']
    for str in arr:
        data = data.replace(str, '"'+str+'"')
    return data

def prepare():
   fileUtil.mkdirs(dataDir, patchDir, rawDir, macdDir, recDir)

def getStockCodes():
    return fileUtil.readFile(dataDir + stockFile)
        
def downloadRaw():
    print 'Begin updating all data...'
    for code in getStockCodes().split('\n'):
        print 'Cralwer stock:', code
        try:
            sinaCrawler = SinaCrawler.SinaCrawler(code)
            rawData = sinaCrawler.getJson()
            jsonData = format(rawData)
            rawFileName = code+'_raw.txt'
            print 'Saving raw data to file:', rawFileName
            fileUtil.writeFile(rawDir + rawFileName, jsonData)
        except Exception, e:
            print str(e)

def calcMacd():
    print 'Begin calc macd...'
    for fi in fileUtil.list(rawDir):
        try:
            print 'Calc the file:', fi
            macd = Macd.Macd(str(fileUtil.readFile(rawDir + fi)))
            macdData = json.dumps(macd.calc())
            macdFileName = fi.split('_')[0] + '_macd_' + today + '.txt'
            print 'Saving macd to file:', macdFileName
            fileUtil.writeFile(macdDir + macdFileName, macdData)
        except Exception, e:
            print str(e)

def updateAll():
    downloadRaw()
    calcMacd()
    print 'Updated raw and macd data to date ', today

def toBuyOrSell(days, reverse=True):
    print 'Begin to recommend candidates...'
    ana = Analysis.Analysis(days, reverse)
    candidates = ana.anaDir(macdDir)
    print 'Candidates:', candidates
    anaFileName = 'buy_' if reverse else 'sell_'
    anaFileName = '%s%s_%s.txt' % (anaFileName, today, days)
    print 'Saving candidates to file:', anaFileName
    fileUtil.writeFile(recDir + anaFileName, json.dumps(candidates))

if __name__ == '__main__':
    prepare()
    if len(sys.argv) == 3:
        if 'update' == sys.argv[1]:
            if 'all' == sys.argv[2].lower():
                updateAll()
            elif 'raw' == sys.argv[2].lower():
                downloadRaw()
            elif 'macd' == sys.argv[2].lower():
                calcMacd()
            else:
                pass
        elif 'buy' == sys.argv[1]:
            days = int(sys.argv[2])
            toBuyOrSell(days)
        elif 'sell' == sys.argv[1]:
            days = int(sys.argv[2])
            toBuyOrSell(days, False)
        else:
            print 'Please see readme.txt for usage.'
    else:
        print 'Please see readme.txt for usage.'
