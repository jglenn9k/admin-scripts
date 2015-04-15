#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import pyrax
import pyrax.exceptions as exc

parser = argparse.ArgumentParser(description='Export Rackspace Cloud Domain records')
parser.add_argument('-D', '--domain', type=str, help='Domain Name', required=True)

args = parser.parse_args()

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.settings.set('identity_type', 'rackspace')
pyrax.settings.set('region', 'ORD')
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns
dns.set_timeout(30)
file = args.domain + '.zonefile.txt'
exp = dns.export_domain(args.domain)
f = open(file, 'w')
f.write(exp)
f.close()

