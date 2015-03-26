# Python PKI management tool

This python tool is an interface around openssl to simplify management of your own SSL CA.

## Usage

```bash
$ ./pypki.py init # Create a new CA in the current directory
$ ./pypki.py csr # Create a CSR
$ ./pypki.py sign-csr <cn> # Sign a CSR with this CA key
$ ./pypki.py list # List all signed certs
+------------------------+----------------+---------+---------------------+----------+
| Common name            | Organisation   | State   | Expiration date     |   Serial |
|------------------------+----------------+---------+---------------------+----------|
| proxmox.demo.brixit.nl | Brixit         | Valid   | 2025-03-23 10:11:07 |     1000 |
+------------------------+----------------+---------+---------------------+----------+
```