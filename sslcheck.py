#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import socket
import json
import ssl
import pprint
from backports.ssl_match_hostname import match_hostname, CertificateError

parser = argparse.ArgumentParser(description='SSL Certificate Report')

parser.add_argument('-H', '--hostname', type=str, help='Host Name', required=True)

args = parser.parse_args()


hostname = args.hostname


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv3, cert_reqs=ssl.CERT_REQUIRED, ca_certs='/etc/pki/tls/cert.pem')

try:
    ssl_sock.connect((hostname, 443))
except ssl.SSLError:
    print hostname + ": Port 443 not open"
    sys.exit(1)

try:
    match_hostname(ssl_sock.getpeercert(), hostname)
except ValueError:
    print hostname + ": Certificate not valid"
    sys.exit(1)

ciphertype = ssl_sock.cipher()[1]
bitsize = int(ssl_sock.cipher()[2]) * 8

data = ssl_sock.getpeercert()['subject']
expires = ssl_sock.getpeercert()['notAfter']

print hostname
print ciphertype
print bitsize
print pprint.pformat(ssl_sock.getpeercert())



#country = data[0][0][1]
#state = data[1][0][1]
#city = data[2][0][1]
#organization = data[3][0][1]
#commonname = data[5][0][1]


#print "%s, %s, %s, %s, %s" % (hostname, bitsize, ciphertype, commonname, expires)



from M2Crypto import SSL, RSA

SSL.Connection.clientPostConnectionCheck = None
ctx = SSL.Context()
conn = SSL.Connection(ctx)
conn.connect((hostname, 443))
cert = conn.get_peer_cert()

print cert.get_issuer().as_text()

print cert.get_subject().as_text()

def size(self):
    """
    Return the size of the key in bytes.
    """
    return m2.pkey_size(self.pkey)
print cert.get_pubkey().size()*8

