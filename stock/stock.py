#!/usr/bin/python
# -*-coding: utf-8-*-

import re
import sys

def readFile(file_path):
    file_object = open(file_path)
    try:
        return file_object.read( )
    finally:
        file_object.close( )

if __name__ == '__main__':
    if len(sys.argv) == 1:
        str='abcd(006531)(hello)'
        arr = re.findall(r'[^()]+', str)
        for item in arr:
            print item
    else:
        str = readFile(sys.argv[1])
        for item in re.findall(r'[^()]+', str):
            if item.startswith('00') or item.startswith('60'):
                print item

