#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import time
import pyrax
import pyrax.exceptions as exc

parser = argparse.ArgumentParser(description='Add Rackspace Cloud Domain records')
parser.add_argument('-D', '--domain', type=str, help='Domain Name', required=True)
parser.add_argument('-t', '--type', type=str, help='Record Type', required=True, default='A')
parser.add_argument('-r', '--record', type=str, help='Record Name', required=True)
parser.add_argument('-d', '--data', type=str, help='Record Data', required=True)
parser.add_argument('-p', '--priority', type=int, help='Mail Priority. Defaults to 10', required=False, default=10)

args = parser.parse_args()

domain_name = args.domain
recoredtype = args.type
record = args.record
data = args.data
priority = args.priority

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.settings.set('identity_type', 'rackspace')
pyrax.settings.set('region', 'ORD')
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns

if recoredtype == "MX":
    rec = {"type": recoredtype,
           "name": record,
           "data": data,
           "priority": priority,
          }

else:
    rec = {"type": recoredtype,
           "name": record,
           "data": data,
           "ttl": 3600
          }
try:
    dom = dns.find(name=domain_name)
    recs = dom.add_records([rec])
except exc.NotFound:
    dom = dns.create(name=domain_name, emailAddress="hostmaster@" + domain_name, ttl=3600)
    recs = dom.add_records([rec])

print recs


