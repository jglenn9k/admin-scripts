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

now = datetime.datetime.now()

try:
    whois_info = pythonwhois.get_whois(args.domain,normalized=True)
except pythonwhois.shared.WhoisException:
    print "UNKNOWN - No root WHOIS server found for %s." % domain_name
    sys.exit(3)

try:
    expdate = whois_info['expiration_date'][0]
except KeyError:
    print "UNKNOWN - No information for %s." % args.domain
    sys.exit(3)

if expdate < (now + datetime.timedelta(days=args.critical)):
    print "CRITICAL - %s expires on: %s. Email %s to renew." % (args.domain,expdate,str(whois_info['contacts']['admin']['email']))
    sys.exit(2)
elif expdate < (now + datetime.timedelta(days=args.warning)):
    print "WARNING - %s expires on: %s. Email %s to renew." % (args.domain,expdate,str(whois_info['contacts']['admin']['email']))
    sys.exit(1)
else:
    print "OK - %s expires on: %s." % (args.domain,expdate)
    sys.exit(0)

