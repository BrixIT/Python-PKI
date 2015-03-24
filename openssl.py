__author__ = 'Martijn Braam <martijn@brixit.nl>'
from subprocess import call
from opensslconfig import OpenSSLConfig
import os


def generate_config(fp):
    config = OpenSSLConfig()
    config["__global__"] = {"distinguished_name": "req_distinguished_name"}
    config["req_distinguished_name"] = {}
    config["v3_req"] = {}
    config["v3_ca"] = {
        "subjectKeyIdentifier": "hash",
        "authorityKeyIdentifier": "keyid:always,issuer",
        "basicConstraints": "CA:true",
        "keyUsage": "cRLSign, keyCertSign"
    }
    config["usr_cert"] = {
        "basicConstraints": "CA:false",
        "keyUsage": "nonRepudiation, digitalSignature, keyEncipherment",
        "nsComment": "OpenSSL Generated Certificate",
        "subjectKeyIdentifier": "hash",
        "authorityKeyIdentifier": "keyid,issuer"
    }
    config["ca"] = {
        "default_ca": "CA_default"
    }
    config["CA_default"] = {
        "dir": os.getcwd(),
        "certs": "$dir/certs",
        "crl_dir": "$dir/crl",
        "database": "$dir/index.txt",
        "new_certs_dir": "$dir/newcerts",
        "certificate": "$dir/certs/ca.cert.pem",
        "private_key": "$dir/private/ca.key.pem",
        "serial": "$dir/serial",
        "RANDFILE": "$dir/private/.rand",
        "x509_extensions": "usr_crt",
        "name_opt": "ca_default",
        "cert_opt": "ca_default",
        "default_days": "3650",
        "default_md": "rsa256"
    }
    config["req"] = {
        "default_bits": "4096",
        "distinguished_name": "req_distinguished_name",
        "attributes": "req_attributes",
        "x509_extensions": "v3_ca",
        "req_extensions": "v3_req",
        "string_mask": "utf8only"
    }
    config.write(fp)


def generate_private_key(path, size=4096):
    return call(["openssl", "genrsa", "-aes256", "-out", path, str(size)])


def generate_root_cert(path, keyfile, cert):
    return call(
        ["openssl", "req", "-new", "-x509",
         "-key", keyfile,
         "-extensions", "v3_ca",
         "-subj", cert.get_dn(),
         "-out", path])