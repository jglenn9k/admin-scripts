#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import math
import argparse

# https://code.google.com/p/pysphere/
from pysphere import VIServer, VIProperty

# From http://stackoverflow.com/a/14822210/2001268
def convertSize(size):
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(math.fabs(size),1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if (s > 0):
       return '%s%s' % (s,size_name[i])
   else:
       return '0B'


parser = argparse.ArgumentParser(description='Check for WMware datastore space')
parser.add_argument('-H', '--host', type=str, help='vSphere Host', required=True)
parser.add_argument('-u', '--user', type=str, help='Username', required=True)
parser.add_argument('-p', '--password', type=str, help='Password', required=True)
parser.add_argument('-w', '--warn', type=int, help='Warn percent left', required=False, default=20)
parser.add_argument('-c', '--critical', type=int, help='Critical percent left', required=False, default=10)

args = parser.parse_args()

server = VIServer()
server.connect(args.host, args.user, args.password)

serviceoutput = "UNKNOWN Error"
perfdata = ""
actualexitflag = 0
actualserviceoutput = "OK all storage ok"

for ds_mor, name in server.get_datastores().items():
    exitflag = 3
    props = VIProperty(server, ds_mor)
    datastorename = name
    if datastorename == 'VMArchives': # Ignores a datastore. This one is always full...
        continue
#    print "----------------------------------------" 
#    print "Datastore %s" % datastorename
#    print "capacity %d" % props.summary.capacity
#    print "freeSpace %d" % props.summary.freeSpace
    if hasattr(props.summary, "uncommitted"):
#        print "uncommitted %d" % props.summary.uncommitted
        usedspace = (props.summary.capacity - props.summary.freeSpace) + props.summary.uncommitted
        freespace = props.summary.freeSpace - props.summary.uncommitted
    else:
        usedspace = props.summary.capacity - props.summary.freeSpace
        freespace = props.summary.freeSpace
    warnsize = props.summary.capacity * (1 - args.warn / 100)
    critsize = props.summary.capacity * (1 - args.critical / 100)
    maxspace = props.summary.capacity
    while exitflag >= 3:
        if usedspace >= critsize:
            exitflag = 2
#            print "CRITICAL: %d > %d" % (usedspace, critsize)
            serviceoutput = "CRITICAL " + datastorename + " has " + convertSize(usedspace) + " provisioned. Alerts at " + convertSize(critsize) + ". Datastore maxsize is " + convertSize(maxspace) + "|"
        elif usedspace >= warnsize:
            exitflag = 1
#            print "WARNING: %d > %d" % (usedspace, warnsize)
            serviceoutput = "WARN " + datastorename + " has " + convertSize(usedspace) + " provisioned. Alerts at " + convertSize(warnsize) + ". Datastore maxsize is " + convertSize(maxspace) + "|"
        else:
            exitflag = 0
#            print "OK: %d" % (usedspace)
            serviceoutput = "OK " + datastorename + " has " + convertSize(usedspace) + " provisioned. Alerts at " + convertSize(warnsize) + ". Datastore maxsize is " + convertSize(maxspace) + "|"
    if exitflag >= 1:
        actualexitflag = exitflag
        actualserviceoutput = serviceoutput
    perfdata += " '"+ datastorename +"'="
    perfdata += "%dB;" % usedspace
    perfdata += "%d;%d;0;%d" % (warnsize, critsize, maxspace)
print actualserviceoutput,
print perfdata
server.disconnect()
sys.exit(actualexitflag)

