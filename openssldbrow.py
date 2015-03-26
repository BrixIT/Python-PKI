__author__ = 'Martijn Braam <martijn@brixit.nl>'
from datetime import datetime
from certinfo import CertInfo


class OpenSSLDbRow:
    (VALID, REVOKED, EXPIRED) = ("Valid", "Revoked", "Expired")

    state = ""
    expiration_date = ""
    revokation_date = ""
    serial = ""
    filename = ""
    subject = ""
    certinfo = None

    def parse(self, row):
        fields = row.split("\t")
        if fields[0] == "V":
            self.state = OpenSSLDbRow.VALID
        elif fields[0] == "R":
            self.state = OpenSSLDbRow.REVOKED
        else:
            self.state = OpenSSLDbRow.EXPIRED

        self.expiration_date = datetime.strptime(fields[1][:-1], "%y%m%d%H%M%S")
        if fields[2] != "":
            self.revokation_date = datetime.strptime(fields[2][:-1], "%y%m%d%H%M%S")

        self.serial = fields[3]
        self.filename = fields[4]
        self.subject = fields[5]

        self.certinfo = CertInfo()
        self.certinfo.from_dn(self.subject)

    def __str__(self):
        return "{} (Serial: {}, valid til {})".format(self.subject, self.serial, self.expiration_date.isoformat())