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

# Use a buffer just to discard it.
buffer = BytesIO()

parser = argparse.ArgumentParser(description='Check Page Speed')
parser.add_argument('-u', '--url', type=str, help='Full URL for page to check.', required=True)
parser.add_argument('-w', '--warn', type=float, help='Total time to result in warning status in seconds.', required=False, default=15)
parser.add_argument('-c', '--crit', type=float, help='Total time to result in critical status in seconds.', required=False, default=30)
parser.add_argument('-t', '--timeout', type=int, help='Time out in seconds.', required=False, default=60)

args = parser.parse_args()

c = pycurl.Curl()

# Junk to allow testing on Windows. Don't use this on Windows.
if os.name == 'nt':
    c.setopt(c.SSL_VERIFYPEER, False);

c.setopt(c.URL, args.url)
# 
c.setopt(c.WRITEFUNCTION, buffer.write)
c.setopt(c.TIMEOUT, args.timeout)
c.setopt(c.VERBOSE, False)
c.setopt(c.HEADER, True);
c.setopt(c.ENCODING, "gzip");
c.setopt(c.USERAGENT, "Page Speed Checker v1.0");
# TODO: Make this optional.
c.setopt(c.FOLLOWLOCATION, False);

try:
    c.perform()
except:
    print('UNKNOWN Error')
    exitcode = 3
    c.close()
    sys.exit(exitcode)
exitcode = 0
if exitcode == 0:
    if c.getinfo(c.TOTAL_TIME) > args.crit:
        exittext = 'CRITICAL'
        exitcode = 2
    elif c.getinfo(c.TOTAL_TIME) > args.warn:
        exittext = 'WARNING'
        exitcode = 1
    else:
        exittext = 'OK'
        exitcode = 0
print('%s - Response Code: %d - Page Size: %d bytes - Speed: %d bytes/second | dns=%fs;;;0.000 connect=%fs;;;0.000 appconnect=%fs;;;0.000 pretransfer=%fs;;;0.000 start=%fs;;;0.000 total=%fs;%f;%f;0.000' % (exittext, c.getinfo(c.RESPONSE_CODE), c.getinfo(c.SIZE_DOWNLOAD), c.getinfo(c.SPEED_DOWNLOAD), c.getinfo(c.NAMELOOKUP_TIME), c.getinfo(c.CONNECT_TIME), c.getinfo(c.APPCONNECT_TIME), c.getinfo(c.PRETRANSFER_TIME), c.getinfo(c.STARTTRANSFER_TIME), c.getinfo(c.TOTAL_TIME), args.warn, args.crit))

c.close()
sys.exit(exitcode)
