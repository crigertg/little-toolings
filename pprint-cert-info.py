#!/usr/bin/env python

import ssl
import socket
import pprint
import sys


def print_help():
    print('usage: pprint-cert-info.py <host>')
    print('example: pprint-cert-info.py heise.de')


def print_help_and_exit(exitcode: int):
    print_help()
    exit(exitcode)


# 2 because sys.argv contains scriptname as first arg
if len(sys.argv) == 2:
    hostname = sys.argv[1]
elif len(sys.argv) > 2:
    print('Too many arguments, only 1 expected.')
    print_help_and_exit(21)
else:
    print('Missing Host as first argument.')
    print_help_and_exit(23)

ssl_context = ssl.create_default_context()
with ssl_context.wrap_socket(socket.socket(), server_hostname=hostname) as s:
    s.connect((hostname, 443))
    cert = s.getpeercert()

# these are the keys we want to print from the element
print_elements = [
  'subject',
  'issuer',
  'notBefore',
  'notAfter',
  'subjectAltName'
]

print = {key: value for (key, value) in cert.items() if key in print_elements}

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(print)
