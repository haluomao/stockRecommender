#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import re

def format(txt):
    return txt.split('_')[0]

class Analysis(object):

    def __init__(self, days, reverse):
        self.days = days
        self.reverse = reverse

    def ana(self, macds):
        begin = macds[-self.days-1][1]
        end = macds[-1][1]
        begin_more = macds[-self.days-1-2][1]['macd']
        return (begin['macd'] * end['macd'])<=0 and (
                   (self.reverse and end['macd'] >= 0 and begin_more<0) or
                   (not self.reverse and end['macd'] <= 0 and begin_more>0))
          
    def anaDir(self, fileDir):
        res = []
        for fi in os.listdir(fileDir):
            fileObj = open(os.path.join(fileDir,fi))
            text = fileObj.read()
            fileObj.close()
            try:
                if self.ana(json.loads(text)):
                    res.append(format(fi))
            except Exception, e:
                print e.message
        return res

if __name__ == '__main__':
    fileDir = sys.argv[1]
    days = 3 if len(sys.argv) < 3 else int(sys.argv[2])
    ana = Analysis(days, False)
    ana.anaDir(fileDir)
