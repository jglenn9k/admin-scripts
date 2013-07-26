#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import time
import pyrax

import paramiko
import base64


# Hard Code this. Might want to have drop down...
template = "f6e27c7a-bfcb-4328-8d9c-6d1f71024827"

parser = argparse.ArgumentParser(description='Create new Rackspace Cloud Server')
parser.add_argument('-n', '--name', type=str, help='Server Name', required=True)
parser.add_argument('-s', '--size', type=int, default=2, help='Server Size', required=True)
parser.add_argument('-c', '--client', type=str, help='Client Name', required=True)
parser.add_argument('-j', '--jobnumber', type=int, help='Job Number', required=True)

args = parser.parse_args()

servername = args.name
flavor = args.size
client = str(args.client)
jobnumber = str(args.jobnumber)



meta = {"client": client,
        "jobnumber": jobnumber,
       }

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.settings.set('identity_type', 'rackspace')
pyrax.settings.set('region', 'ORD')
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

server = cs.servers.create(servername, template, flavor, meta=meta)
print "Name: ", server.name
print "ID: ", server.id
print "Status: ", server.status
print "Admin Password: ", server.adminPass
print "Data: ", server.metadata


while server.status != "ACTIVE":
    if server.status == "BUILD":
        time.sleep(60)
        server = cs.servers.get(server.id)
        print "Status: %s" % server.status
        print "%d%%" % server.progress
    else:
        print "Serious problem..."
        print "Build is in status %s" % server.status
        ssy.exit(1)

print "Server looks active..."
print server.status

ipaddress = server.networks['public'][-1]
print "IP Address %s" % ipaddress

time.sleep(60)

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ipaddress, username='root')

    stdin, stdout, stderr = client.exec_command('uptime')
    print stdout.read()
    stdin, stdout, stderr = client.exec_command('hostname')
    print stdout.read()
finally:
    client.close()


