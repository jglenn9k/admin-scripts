#!/usr/bin/python
# -*- coding: utf-8 -*-

# Good for batch checking SSL certificates. Output in .csv style.

import sys
import argparse
import socket
import ssl
# https://pypi.python.org/pypi/backports.ssl_match_hostname
from backports.ssl_match_hostname import match_hostname

def size(self):
    """
    Return the size of the key in bytes.
    """
    return SSL.pkey_size(self.pkey)

parser = argparse.ArgumentParser(description='SSL Certificate Report')
parser.add_argument('-H', '--hostname', type=str, help='Host Name', required=True)

args = parser.parse_args()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

ssl_sock = ssl.wrap_socket(sock,
                           ssl_version=ssl.PROTOCOL_SSLv3,
                           cert_reqs=ssl.CERT_REQUIRED,
                           ca_certs='/etc/pki/tls/cert.pem'
                           )

try:
    ssl_sock.connect((args.hostname, 443))
except ssl.SSLError, error:
    print args.hostname + ": Port 443 not open"
    sys.exit(1)

try:
    match_hostname(ssl_sock.getpeercert(), args.hostname)
except ValueError:
    print args.hostname + ": Certificate not valid"
    sys.exit(1)

ciphertype = ssl_sock.cipher()[1]
expires = ssl_sock.getpeercert()['notAfter']
from M2Crypto import SSL

SSL.Connection.clientPostConnectionCheck = None
ctx = SSL.Context()
conn = SSL.Connection(ctx)
conn.connect((args.hostname, 443))
cert = conn.get_peer_cert()

certinfo = cert.get_subject().as_text()

certsize = cert.get_pubkey().size() * 8

print '"%s", "%s", "%s", "%s", "%s"' % (args.hostname, ciphertype, certsize, certinfo, expires)

conn.shutdown(socket.SHUT_RDWR)
sock.shutdown(socket.SHUT_RDWR)
conn.close()
sock.close()
