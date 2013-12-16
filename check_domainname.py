#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
# https://pypi.python.org/pypi/pythonwhois
import pythonwhois
import datetime

parser = argparse.ArgumentParser(description='Icinga check for Domain Name expiration')
parser.add_argument('-D', '--domain', type=str, help='Domain Name', required=True)
parser.add_argument('-w', '--warning', type=int, help='Days to result in warning status', default=30)
parser.add_argument('-c', '--critical', type=int, help='Days to result in critical status', default=7)

args = parser.parse_args()
domain_name = args.domain
warn = args.warning
crit = args.critical

whois_info = pythonwhois.get_whois(domain_name,normalized=True)

now = datetime.datetime.now()

try:
    expdate = whois_info['expiration_date'][0]
except KeyError:
    print "UNKNOWN - No information for %s." % domain_name
    sys.exit(3)

if expires < (now + datetime.timedelta(days=crit)):
    print "CRITICAL - %s expires on: %s. Email %s to renew." % (domain_name,expdate,str(whois_info['contacts']['admin']['email']))
    sys.exit(2)
elif expires < (now + datetime.timedelta(days=warn)):
    print "WARNING - %s expires on: %s. Email %s to renew." % (domain_name,expdate,str(whois_info['contacts']['admin']['email']))
    sys.exit(1)
else:
    print "OK - %s expires on: %s." % (domain_name,expdate)
    sys.exit(0)

