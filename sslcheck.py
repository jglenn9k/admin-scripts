#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import socket
import ssl
from backports.ssl_match_hostname import match_hostname, CertificateError

parser = argparse.ArgumentParser(description='SSL Certificate Report')
parser.add_argument('-H', '--hostname', type=str, help='Host Name', required=True)

args = parser.parse_args()
hostname = args.hostname
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv3, cert_reqs=ssl.CERT_REQUIRED, ca_certs='/etc/pki/tls/cert.pem')

try:
    ssl_sock.connect((hostname, 443))
except ssl.SSLError, socket.error:
    print hostname + ": Port 443 not open"
    sys.exit(1)

try:
    match_hostname(ssl_sock.getpeercert(), hostname)
except ValueError, :
    print hostname + ": Certificate not valid"
    sys.exit(1)

ciphertype = ssl_sock.cipher()[1]
expires = ssl_sock.getpeercert()['notAfter']

from M2Crypto import SSL, RSA

SSL.Connection.clientPostConnectionCheck = None
ctx = SSL.Context()
conn = SSL.Connection(ctx)
conn.connect((hostname, 443))
cert = conn.get_peer_cert()

certinfo = cert.get_subject().as_text()

def size(self):
    """
    Return the size of the key in bytes.
    """
    return m2.pkey_size(self.pkey)

certsize = cert.get_pubkey().size()*8

print "'%s', '%s', '%s', '%s', '%s'" % (hostname, ciphertype, certsize, certinfo, expires)
sock.close()
conn.close()