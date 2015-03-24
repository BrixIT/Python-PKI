#!/usr/bin/env python3
__author__ = 'Martijn Braam <martijn@brixit.nl>'
import argparse
import sys, os
from subprocess import call
from certinfo import CertInfo
import openssl


class PyPKI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Simple management tool for your own public key infrastructure",
        )
        parser.add_argument('command', choices=["init", "list"], help="Command to run")
        args = parser.parse_args(sys.argv[1:2])
        getattr(self, args.command)()

    @staticmethod
    def init():
        print("Checking openssl is installed")
        if call(["openssl", "version"]) != 0:
            print("No valid openssl found")
            exit(1)

        print("\nThe first step is to create a root certificate for your CA. Please enter the CA information below.")

        ca_cert = CertInfo()
        ca_cert.c = input("[C]  Enter the country (ISO3166 2 letter country code)\n>")
        ca_cert.st = input("[ST] Enter the state or province\n>")
        ca_cert.l = input("[L]  Enter the locality (city)\n>")
        ca_cert.o = input("[O] Enter the organisation name\n>")
        ca_cert.ou = input("[OU] Enter the organizational unit (typically certificate type or brand)\n>")
        ca_cert.cn = input("[CN] Enter the common name\n>")

        print("\nIs the following information correct?\n")
        print(ca_cert.get_table())

        print("Creating openssl.cnf...")
        openssl.generate_config("openssl.cnf")

        print("Creating directory structure...")
        os.mkdir("certs")
        os.mkdir("private")
        os.chmod("private", 0o700)
        os.mkdir("newcerts")
        os.mkdir("crl")
        open("index.txt", "w").close()
        with open("serial", "w") as serial_file:
            serial_file.write("1000")
        print("\nGenerating private key... you wil be asked to enter a password for your private key. "
              "This password will be asked for every cert you generate.")
        openssl.generate_private_key("private/ca.key.pem")
        os.chmod("private/ca.key.pem", 0o400)
        print("\nGenerating the root certificate. Enter the password you've created above when asked.")
        openssl.generate_root_cert("certs/ca.cert.pem", "private/ca.key.pem", ca_cert)
        os.chmod("certs/ca.cert.pem", 0o444)
        print("\nCA setup complete")

if __name__ == "__main__":
    PyPKI()