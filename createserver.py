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
# CentOS 6.4
template = "25a5f2e8-f522-4fe0-b0e0-dbaa62405c25"

parser = argparse.ArgumentParser(description='Create new Rackspace Cloud Server')
parser.add_argument('-n', '--name', type=str, help='Server Name', required=True)
parser.add_argument('-s', '--size', type=int, default=2, help='Server Size', required=True)

args = parser.parse_args()

servername = args.name
flavor = args.size


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.settings.set('identity_type', 'rackspace')
pyrax.settings.set('region', 'DFW')
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
        time.sleep(60)
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

time.sleep(60)

commands = [
'rpm -ivh http://mirror.rackspace.com/epel/6/x86_64/epel-release-6-8.noarch.rpm',
'rpm -ivh http://mirror.rackspace.com/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm',
'rpm -ivh http://yum.puppetlabs.com/el/6/products/x86_64/puppetlabs-release-6-7.noarch.rpm',
'yum -y install vim-enchanced puppet mlocate man file',

]


try:
    client = paramiko.SSHClient()
#    client.load_system_host_keys()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ipaddress, username='root', password=rootpassword)
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        print stdout.read()

finally:
    client.close()


