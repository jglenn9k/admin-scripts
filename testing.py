#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import time
import pyrax


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.settings.set('identity_type', 'rackspace')
pyrax.settings.set('region', 'ORD')
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

servers = cs.servers.list()
for server in servers:
    print " -", server.id, server.name