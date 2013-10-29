#!/usr/bin/python

import sys
import whois
import argparse
import datetime
import time

parser = argparse.ArgumentParser(description='Icinga check for Domain Name expiration')
parser.add_argument('-D', '--domain', type=str, help='Domain Name', required=True)
parser.add_argument('-w', '--warning', type=int, help='Days to result in warning status', default=30)
parser.add_argument('-c', '--critical', type=int, help='Days to result in critical status', default=7)

args = parser.parse_args()
domain_name = args.domain
warn = args.warning
crit = args.critical

whois_info = whois.whois(domain_name)

# There has got to be a better way to do this...
now = datetime.datetime.now()
now = str(now)
now = now[:-7]

current_time = time.mktime(datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple())

expires = time.mktime(datetime.datetime.strptime(whois_info.expiration_date, "%Y-%m-%d %H:%M:%S").timetuple())

if expires < (current_time + (86400 * crit)):
    print "CRITICAL - Domain Expires on: " + whois_info.expiration_date
    sys.exit(2)

elif expires < (current_time + (86400 * warn)):
    print "WARNING - Domain Expires on: " + whois_info.expiration_date
    sys.exit(1)
else:
    print "OK - Domain Expires on: " + whois_info.expiration_date
    sys.exit(0)
