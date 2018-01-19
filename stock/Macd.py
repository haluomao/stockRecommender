#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
import json

def format(data):
    arr = ['day', 'close', 'open', 'high', 'low', 'volume']
    for str in arr:
        data = data.replace(str, '"'+str+'"')
    return data

def sortDictValues(adict): 
    keys = adict.keys() 
    keys.sort() 
    return [adict[key] for key in keys] 

def sortDict(di):
    return [(k,di[k]) for k in sorted(di.keys())] 

class Macd(object):

    # data:'[{ day:'2018-01-02', close:'38.01'  }]'
    def __init__(self, str):
        self.data = json.loads(str)

    def calc(self, s=12, l=26, m=9):
        res = {}
        #DIF:EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);
        ema12 = self.ema(self.data, s)
        ema26 = self.ema(self.data, l)
        dif = {}
        for key in ema26:
            item = {}
            item['day'] = ema26[key]['day']
            item['close'] = ema12[key]['close'] - ema26[key]['close']
            dif[key] = item
            r = {}
            r['diff'] = item['close']
            res[item['day']] = r
        # DEA:EMA(DIF,MID);
        # MACD:(DIF-DEA)*2,COLORSTICK; 
        dea = self.ema(sortDictValues(dif), m)
        for key in dea:
            res[key]['dea'] = dea[key]['close']
            res[key]['macd'] = 2*(res[key]['diff']-res[key]['dea'])
        return sortDict(res)

    # ema1 = 2/(N+1)*close + (N-1)/(N+1)*ema0
    def ema(self, arr, scale):
        res = {}
        ema=[]
        alpha = 2.0/(scale+1)
        for i in range(len(arr)):
            item = {}
            item['scale'] = scale
            item['day'] = arr[i]['day']
            if i == 0:
                item['close'] = float(arr[i]['close'])
            else:
                item['close'] = alpha * float(arr[i]['close']) + (1-alpha) * ema[-1]
            ema.append(item['close'])
            res[item['day']] = item
        return res

def demo3(fileDir, destDir):
    if not os.path.exists(destDir):
        os.mkdir(destDir)
    if os.path.exists(fileDir):
        count = 0
        for fi in os.listdir(fileDir):
            count += 1
            print '[',count,']Calc file:', fi
            fileObj = open(os.path.join(fileDir,fi))
            text = fileObj.read()
            fileObj.close()
            try:
                macd = Macd(str(text))
                outText = json.dumps(macd.calc())
            except Exception, e:
                print str(e)
                print 'some wrong'
                continue
            outFileObj = open(os.path.join(destDir, 'macd_'+fi), 'w')
            outFileObj.write(outText)
            outFileObj.close()

def demo2(file_path='data.txt'):
    file_object = open(file_path)
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    macd = Macd(str(all_the_text))
    res = macd.calc()
    print json.dumps(res)

def demo1():
    arr = '''[{day:"2017-11-07 10:30:00",close:"1"},{day:"2017-11-08 10:30:00",close:"2"},
        {day:"2017-11-09 10:30:00",close:"3"},{day:"2017-11-10 10:30:00",close:"4"},
        {day:"2017-11-11 10:30:00",close:"5"},{day:"2017-11-12 10:30:00",close:"6"},
        {day:"2017-11-13 10:30:00",close:"7"},{day:"2017-11-14 10:30:00",close:"8"}]'''   
    data = json.loads(format(arr))
    macd = Macd(format(arr))
    print macd.ema(data, 5)
    print macd.calc()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        demo1()
    elif len(sys.argv)==2:
        demo2(sys.argv[1])
    else:
        demo3(sys.argv[1], sys.argv[2])
