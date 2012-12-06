#!/usr/bin/env python
# Must use Python 2.x
"""Import list of servers and services from Icinga and make pages for the Wiki.
It will overwrite existing pages."""

import json
import urllib2
# See http://sourceforge.net/apps/mediawiki/mwclient/index.php?title=Main_Page
import mwclient

# Edit these
wikiusername = "admin"
wikipassword = "admin123"
icingausername = "admin"
icingapassword = "admin123"
# Needs to be the location of your status.cgi
icingaurl = "https://icinga.example.com/cgi-bin/icinga/status.cgi"
# I'm assuming you use HTTPS. You really should.
wikihost = ('https','en.wikipedia.org')

# Config for the Wiki
# You might need to change the path, but this is the default.
site = mwclient.Site(wikihost, path='/w/')
site.login(wikiusername, wikipassword)

# This gets through the HTTP Basic Auth in Icinga
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, icingaurl+"?style=hostdetail&jsonoutput", icingausername, icingapassword)
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
# This is the list of hosts.
req = urllib2.Request(icingaurl+"?style=hostdetail&jsonoutput")
data = urllib2.urlopen(req)
json_data = data.read()
j = json.loads(json_data)

# Start a counter for looping through the json listing of hosts
x = int(0)

for i in j['status']['host_status']:
    hostname = j['status']['host_status'][x]['host']
    passman2 = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman2.add_password(None, icingaurl + "?host=" + hostname + "&jsonoutput", icingausername, icingapassword)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
    # This is the lists of services on each host.
    req2 = urllib2.Request(icingaurl + "?host=" + hostname + "&jsonoutput")
    data2 = urllib2.urlopen(req2)
    json_data2 = data2.read()
    j2 = json.loads(json_data2)
    # Start a counter for looping through the json listing of services on each host
    y = int(0)
    # Start building text for the Page.
    page = site.Pages[hostname]
    pagetext = "== Services ==\r\n\r\n"
    for i in j2['status']['service_status']:
        pagetext += "=== "+ j2['status']['service_status'][y]['service'] + " ===\r\n\r\n"
        y += 1
    pagetext += "[[Category:Icinga]]\r\n\r\n"
    # Save the pagetext.
    page.save(pagetext, summary='Creating new page')
    x += 1
print "Done"
