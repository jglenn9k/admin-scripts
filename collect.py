#!/usr/bin/python
# -*- coding: utf-8 -*-

# Get Web Server config info
# Works on Windows Server 2003
# Works on Windows Server 2008
# Works on RHEL/CentOS 5
# Works on RHEL/CentOS 6

# Ourput in csv
# Output should be easy to change for a database or excel or something


import os
import sys
import platform
import subprocess
import socket
import time

hostname = socket.gethostname()

now = time.time()
thirtydays_ago = now - 60*60*24*30

filename = hostname + ".txt"
file = open(filename,'w')

file.write("Domain Name,IP Address,Document Root,Config,Log File,Status,Time Stamp" + os.linesep)


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
        ip = None
    return ip

def get_config_value(file,item):
    include = a.get("/files" + file + "/VirtualHost/*[self::directive='Include']/arg")
    values = a.match("/files" + file + "/VirtualHost/*[self::directive='" + item + "']/arg")
    info = []
    if values:
        for value in values:
            info.append(a.get(value))
        return info
    else:
        try:
            values = a.match("/files" + include + "/*[self::directive='" + item + "']/arg")
            for value in values:
                info.append(a.get(value))
            return info
        except:
            info = None
            return info

if platform.system() == "Windows":
    import win32com.client
    hostname = hostname + ".vml.com"
    webserver = win32com.client.GetObject("IIS://localhost/W3SVC")
    for webservice in webserver:
        if webservice.Class == "IIsWebServer":
            status = state2desc(webservice.ServerState)
            logfile = webservice.LogFileDirectory + "\W3SVC" + webservice.Name
            domainname = webservice.ServerBindings[0]
            domainname = domainname.split(":")
            serveralias = str(domainname[-1])
            print domainname
            domainname = str(domainname[2])
            ipaddress = get_ip_for_host(str(domainname))
            config = webservice.ServerComment
            website = win32com.client.GetObject(webservice.adsPath + "/Root")
            documentroot = website.Path
            file.write("('%s','%s','%s','%s','%s','%s','%d');" % (domainname,ipaddress,documentroot,config,logfile,status,now) + os.linesep)
    file.close()

if platform.system() == "Linux":
    import augeas
    # Use apache2ctl for Debian/Ubuntu
    webserver = subprocess.Popen("apachectl -S 2>&1 | grep namevhost | awk '{print $5}' | sed 's/(//g' | sed 's/:.*)//g' | sort -u | grep -v 0", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    configs = webserver.stdout.readlines()

    for config in configs:
        config = config.strip()
        a = augeas.Augeas()
        a.set("/augeas/load/Httpd/incl[last()+1]", config)
        a.load()
        include = a.get("/files" + config + "/VirtualHost/*[self::directive='Include']/arg")
        a.set("/augeas/load/Httpd/incl[last()+1]", include)
        a.load()
        domainname = get_config_value(config,"ServerName")
        if domainname:
            domainname = domainname[0]
            ipaddress = get_ip_for_host(domainname)
        else:
            ipaddress = None
        serveraliases = get_config_value(config,"ServerAlias")
        documentroot = get_config_value(config,"DocumentRoot")
        if documentroot:
            documentroot = documentroot[0]
        logfiles = get_config_value(config,"CustomLog")
        if logfiles:
            # Need to fix this path some how...
            logfile = "/etc/httpd/" + logfiles[0]
        else:
            logfile = None
        try:
            fileage = os.path.getmtime(logfile)
            if fileage > thirtydays_ago:
                status = "Yes
            else:
                status = "No"
        except:
            status = "No"
        file.write("('%s','%s','%s','%s','%s','%s','%d');" % (domainname,ipaddress,documentroot,config,logfile,status,now) + os.linesep)

    file.close()