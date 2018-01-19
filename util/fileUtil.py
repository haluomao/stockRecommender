#!/usr/bin/python
# coding=UTF-8

import os

def readFile(file_path):
    file_object = open(file_path)
    try:
        return file_object.read( )
    finally:
        file_object.close( )

def writeFile(file_path, content):
    file_object = open(file_path, 'w')
    file_object.write(content)
    file_object.close()

def mkdir(file_dir):
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

def mkdirs(*file_dirs):
    for file_dir in file_dirs:
        mkdir(file_dir)

def list(file_dir):
    return os.listdir(file_dir)
