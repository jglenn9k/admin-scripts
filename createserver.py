#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import time
# https://pypi.python.org/pypi/pyrax
import pyrax
# https://pypi.python.org/pypi/paramiko
import paramiko

# CentOS 6.5
template = "042395fc-728c-4763-86f9-9b0cacb00701"

parser = argparse.ArgumentParser(description='Create new Rackspace Cloud Server')
parser.add_argument('-n', '--name', type=str, help='Server Name', required=True)
parser.add_argument('-s', '--size', type=str, default='performance1-1', help='Server Size', required=True)

args = parser.parse_args()

servername = args.name
flavor = args.size

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.settings.set('identity_type', 'rackspace')
# DFW is the default
# pyrax.settings.set('region', 'DFW')
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

server = cs.servers.create(servername, template, flavor)
print "Name: ", server.name
print "ID: ", server.id
print "Status: ", server.status
print "Admin Password: ", server.adminPass

rootpassword = server.adminPass

while server.status != "ACTIVE":
    if server.status == "BUILD":
        time.sleep(15)
        server = cs.servers.get(server.id)
        print "Status: %s" % server.status
        print "%d%%" % server.progress
    else:
        print "Serious problem..."
        print "Build is in status %s" % server.status
        sys.exit(1)

print "Server looks active..."

ipaddress = server.accessIPv4
print "IP Address %s" % ipaddress

# Wait for SSH to start before trying to login
time.sleep(30)

commands = [
'rpm -ivh http://mirror.rackspace.com/epel/6/x86_64/epel-release-6-8.noarch.rpm',
'rpm -ivh http://mirror.rackspace.com/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm',
'rpm -ivh http://yum.puppetlabs.com/el/6/products/x86_64/puppetlabs-release-6-7.noarch.rpm',
'yum -y install vim-enhanced puppet mlocate man file',

]

try:
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ipaddress, username='root', password=rootpassword)
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        print stdout.read()

finally:
    client.close()

