#!/usr/bin/python
# -*- coding: utf-8 -*-

# See http://pycurl.io/
import pycurl

import os
import sys
import argparse

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

buffer = BytesIO()

parser = argparse.ArgumentParser(description='Check Page Speed')
parser.add_argument('-u', '--url', type=str, help='Full URL for page to check.', required=True)

args = parser.parse_args()

c = pycurl.Curl()

if os.name == 'nt':
    c.setopt(c.SSL_VERIFYPEER, False);

c.setopt(c.URL, args.url)
c.setopt(c.WRITEDATA, buffer)

c.setopt(c.TIMEOUT, 60)
c.setopt(c.VERBOSE, False)

c.setopt(c.HEADER, True);
c.setopt(c.ENCODING, "gzip");
c.setopt(c.FOLLOWLOCATION, False);
c.setopt(c.USERAGENT, "Page Speed Checker v1.0");

c.perform()

print('RESPONSE_CODE: %d' % c.getinfo(c.RESPONSE_CODE))
print('SIZE_DOWNLOAD: %d bytes.' % c.getinfo(c.SIZE_DOWNLOAD))
print('SPEED_DOWNLOAD: %d bytes/second.' % c.getinfo(c.SPEED_DOWNLOAD))

print('NAMELOOKUP_TIME: %f seconds.' % c.getinfo(c.NAMELOOKUP_TIME))
print('CONNECT_TIME: %f seconds.' % c.getinfo(c.CONNECT_TIME))
print('APPCONNECT_TIME: %f seconds.' % c.getinfo(c.APPCONNECT_TIME))
print('PRETRANSFER_TIME: %f seconds.' % c.getinfo(c.PRETRANSFER_TIME))
print('STARTTRANSFER_TIME: %f seconds.' % c.getinfo(c.STARTTRANSFER_TIME))
print('TOTAL_TIME: %f seconds.' % c.getinfo(c.TOTAL_TIME))

# getinfo must be called before close.
c.close()

