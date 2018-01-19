#!/usr/bin/python
# coding=UTF-8

import urllib
import urllib2
import re
import sys

# Base Crawler
class BaseCrawler:

    # Construct
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl;
    
    # Get the raw page.
    def getPage(self):
        try:
            url = self.baseUrl;
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'Failed to connect.', e.reason
                return None

if __name__ == '__main__':
    gpus = sys.argv[1]
    crawler = BaseCrawler(gpus)
    print crawler.getPage()
