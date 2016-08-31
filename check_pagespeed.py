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
parser.add_argument('-w', '--warn', type=str, help='Total time to result in warning status in seconds.', required=True)
parser.add_argument('-c', '--crit', type=str, help='Total time to result in critical status in seconds.', required=True)


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

if c.getinfo(c.TOTAL_TIME) > args.warn:
    exittext = 'WARNING'
    exitcode = 1
elif c.getinfo(c.TOTAL_TIME) > args.crit:
    exittext = 'CRITICAL'
    exitcode = 2
else:
    exittext = 'OK'
    exitcode = 0

print('%s | dns=%fs;;;0.000 connect=%fs;;;0.000 appconnect=%fs;;;0.000 pretransfer=%fs;;;0.000 start=%fs;;;0.000 total=%fs;;;0.000' % (exittext, c.getinfo(c.NAMELOOKUP_TIME), c.getinfo(c.CONNECT_TIME), c.getinfo(c.APPCONNECT_TIME), c.getinfo(c.PRETRANSFER_TIME), c.getinfo(c.STARTTRANSFER_TIME), c.getinfo(c.TOTAL_TIME)))

# getinfo must be called before close.
c.close()

