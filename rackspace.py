#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pyrax
import pyrax.exceptions as exc
import time


creds_file = os.path.expanduser(".rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cs_ord = pyrax.connect_to_cloudservers(region="ORD")
cs_dfw = pyrax.connect_to_cloudservers(region="DFW")
dfw_servers = cs_dfw.servers.list()
ord_servers = cs_ord.servers.list()
all_servers = dfw_servers + ord_servers

print "Cloud Servers:"
for server in all_servers:
    time.sleep(5)
    print "Name:", server.name
    print "  ID:", server.id
    print "  Status:", server.status
    print "  Networks:", server.networks

print "Cloud DNS"
dns = pyrax.cloud_dns

PAGE_SIZE = 10
count = 0

def print_domains(domains):
    for domain in domains:
        time.sleep(5)
        print "Domain:", domain.name
        print "  email:", domain.emailAddress
        print "  created:", domain.created


domains = dns.list(limit=PAGE_SIZE)
count += len(domains)
print_domains(domains)

# Loop until all domains are printed
while True:
    try:
        domains = dns.list_next_page()
        time.sleep(5)
        count += len(domains)
    except exc.NoMoreResults:
        break
    print_domains(domains)

print "There were a total of %s domain(s)." % count


print "Cloud Load Balancers"

clb = pyrax.cloud_loadbalancers
for lb in clb.list():
    time.sleep(5)
    print "Name:", lb.name
    print "ID:", lb.id
    print "Status:", lb.status
    print "Nodes:"
    for item in lb.nodes:
        print item.id
        print item.address
    print "Virtual IPs:"
    for item in lb.virtual_ips:
        print item.address
    print "Algorithm:", lb.algorithm
    print "Protocol:", lb.protocol
