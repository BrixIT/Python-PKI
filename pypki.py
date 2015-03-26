#!/usr/bin/env python3
__author__ = 'Martijn Braam <martijn@brixit.nl>'
import argparse
import sys, os
from subprocess import call
from certinfo import CertInfo
import openssl
from tabulate import tabulate
from openssldbrow import OpenSSLDbRow


class PyPKI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Simple management tool for your own public key infrastructure",
        )
        parser.add_argument('command', choices=["init", "list", "csr", "sign-csr"], help="Command to run")
        args = parser.parse_args(sys.argv[1:2])
        command = args.command.replace("-", "_")
        getattr(self, command)()

    @staticmethod
    def init():
        print("Checking openssl is installed")
        if call(["openssl", "version"]) != 0:
            print("No valid openssl found")
            exit(1)

        print("\nThe first step is to create a root certificate for your CA. Please enter the CA information below.")

        ca_cert = CertInfo()
        ca_cert.c = input("[C]  Enter the country (ISO3166 2 letter country code)\n> ")
        ca_cert.st = input("[ST] Enter the state or province\n> ")
        ca_cert.l = input("[L]  Enter the locality (city)\n> ")
        ca_cert.o = input("[O] Enter the organisation name\n> ")
        ca_cert.ou = input("[OU] Enter the organizational unit (typically certificate type or brand)\n> ")
        ca_cert.cn = input("[CN] Enter the common name\n> ")

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

    @staticmethod
    def list():
        table = [
            ["Common name", "Organisation", "State", "Expiration date", "Serial"]
        ]
        with open("index.txt", "r") as index:
            for row in index.readlines():
                parsed = OpenSSLDbRow()
                parsed.parse(row)
                table.append([parsed.certinfo.cn, parsed.certinfo.o, parsed.state, parsed.expiration_date, parsed.serial])

        print(tabulate(table, tablefmt="psql", headers="firstrow"))

    @staticmethod
    def csr():
        csr_info = CertInfo()
        csr_info.c = input("[C]   Enter the country (ISO3166 2 letter country code)\n> ")
        csr_info.st = input("[ST]  Enter the state or province\n> ")
        csr_info.l = input("[L]   Enter the locality (city)\n> ")
        csr_info.o = input("[O]  Enter the organisation name\n> ")
        csr_info.ou = input("[OU]  Enter the organizational unit (typically certificate type or brand)\n> ")
        csr_info.cn = input("[CN]  Enter the common name\n> ")
        csr_info.san = input("[SAN] Enter the alternative names, separated by commas\n> ")
        print("\nIs the following information correct?\n")
        print(csr_info.get_table())
        input("Press enter to continue")

        key_file = "private/{}.key.pem".format(csr_info.cn)
        csr_file = "certs/{}.csr.pem".format(csr_info.cn)
        openssl.generate_private_key(key_file, encrypt=False)
        openssl.generate_csr(csr_file, key_file, csr_info)
        print("\nYour CSR has been generated in {} with the private key in {}".format(csr_file, key_file))

    @staticmethod
    def sign_csr():
        parser = argparse.ArgumentParser()
        parser.add_argument('cn', help="Common name of CSR to sign")
        args = parser.parse_args(sys.argv[2:])
        csr_file = "certs/{}.csr.pem".format(args.cn)
        cert_file = "certs/{}.cert.pem".format(args.cn)
        print("Signing {}. You will be asked for the password of your CA root certificate".format(csr_file))
        openssl.sign_csr(csr_file, cert_file)
        print("The signed certificate is {}".format(cert_file))

if __name__ == "__main__":
    PyPKI()