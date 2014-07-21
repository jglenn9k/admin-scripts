#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://pysvn.tigris.org/
import pysvn
# http://code.google.com/p/argparse/
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Deploy from local SVN to remote SVN')
parser.add_argument('--remoteurl', type=str, help='remote SVN URL', required=True)
parser.add_argument('--localurl', type=str, help='local SVN URL', required=True)

args = parser.parse_args()

remotepath = args.remoteurl.rsplit('/',1)
localpath = args.localurl.rsplit('/',1)

localclient = pysvn.Client()
localclient.callback_get_login = locallogin
remoteclient = pysvn.Client()
remoteclient.callback_get_login = remotelogin

if not os.path.exists(localpath[1] + '/htdocs'):
    localclient.checkout(args.localurl, localpath[1])
if not os.path.exists(remotepath[1] + '/docroot'):
    remoteclient.checkout(args.remoteurl + '/trunk', remotepath[1])

localclient.switch(localpath[1],args.localurl)

os.system('rsync -a --delete ' + localpath[1] + '/htdocs/ ' + remotepath[1] + '/docroot --exclude=*.svn*')
sys.stdout.flush()

changes = remoteclient.status(remotepath[1])
print 'files to be added:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.added]
print 'files to be removed:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.deleted]
print 'files that have changed:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.modified]
print 'files with merge conflicts:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.conflicted]
print 'unversioned files:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.unversioned]
print 'missing files:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.missing]
sys.stdout.flush()

for file in [f.path for f in changes if f.text_status == pysvn.wc_status_kind.added]:
    remoteclient.add(file)
for file in [f.path for f in changes if f.text_status == pysvn.wc_status_kind.deleted]:
    remoteclient.remove(file)
for file in [f.path for f in changes if f.text_status == pysvn.wc_status_kind.unversioned]:
    remoteclient.add(file)
for file in [f.path for f in changes if f.text_status == pysvn.wc_status_kind.missing]:
    remoteclient.remove(file)
changes = remoteclient.status(remotepath[1])
print 'files to be added:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.added]
print 'files to be removed:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.deleted]
print 'files that have changed:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.modified]
print 'files with merge conflicts:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.conflicted]
print 'unversioned files:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.unversioned]
print 'missing files:'
print [f.path for f in changes if f.text_status == pysvn.wc_status_kind.missing]
sys.stdout.flush()

remoteclient.checkin([remotepath[1]], 'Updating from SVN.')
sys.stdout.flush()
