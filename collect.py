#!/usr/bin/python
# -*- coding: utf-8 -*-

# Get the Web Server config info
# Works on Windows Server 2003
# Works on RHEL 5
# Should also work on Windows Server 2008
# Should also work on RHEL 6

# Output should be easy to change for a database or excel or something


import os
import platform
import subprocess
import re
import socket
import time

hostname = socket.gethostname()
now = time.time()
thirtydays_ago = now - 60*60*24*30


def state2desc(n):
    if n == 1:
        return "Starting"
    elif n == 2:
        return "Started"
    elif n == 3:
        return "Stopping"
    elif n == 4:
        return "Stopped"
    elif n == 5:
        return "Pausing"
    elif n == 6:
        return "Paused"
    elif n == 7:
        return "Continuing"
    else:
        return "Unknown"

def get_ip_for_host(host):
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        ip = "NULL"
    return ip

if platform.system() == "Windows":
    import win32com.client
    webserver = win32com.client.GetObject("IIS://localhost/W3SVC")
    for webservice in webserver:
        if webservice.Class == "IIsWebServer":
            status = state2desc(webservice.ServerState)
            logfiles = webservice.LogFileDirectory + "\W3SVC" + webservice.Name
            domainname = webservice.ServerBindings[0]
            domainname = domainname.split(":")
            domainname = str(domainname[2])
            ip = get_ip_for_host(str(domainname))
            config = webservice.ServerComment
            website = win32com.client.GetObject(webservice.adsPath + "/Root")
            documentroot = website.Path
            print "Server: %s Domain Name: %s IP: %s Document Root: %s Config: %s Log Files: %s Status: %s" % (hostname,domainname,ip,documentroot,config,logfiles,status)

if platform.system() == "Linux":
    webserver = subprocess.Popen("apachectl -S 2>&1 | grep namevhost | awk '{print $5}' | sed 's/(//g' | sed 's/:.*)//g' | sort -u ",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    config = webserver.stdout.readlines()
    for site in config:
        config = site.strip()
        for line in open(site.strip()):
            if re.match("ServerName",line.strip()):
                domainname = line.strip().split()[1]
                ip = get_ip_for_host(str(domainname))
            if re.match("CustomLog",line.strip()):
                logfiles = line.strip().split()[1]
                logfiles = "/etc/httpd/" + logfiles
                try:
                    fileage = os.path.getctime(logfiles)
                    if fileage < thirtydays_ago:
                        status = 1
                    else:
                        status = 0
                except OSError:
                    status = 1
            if re.match("DocumentRoot",line.strip()):
                documentroot = line.strip()
        print "Server: %s Domain Name: %s IP: %s Document Root: %s Config: %s Log Files: %s Status: %d" % (hostname,domainname,ip,documentroot,config,logfiles,status)
