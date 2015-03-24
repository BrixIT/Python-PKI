__author__ = 'Martijn Braam <martijn@brixit.nl>'
from tabulate import tabulate


class CertInfo:
    cn = ""
    c = ""
    l = ""
    st = ""
    o = ""
    ou = ""

    def get_table(self):
        table = [
            ["Common name", self.cn],
            ["Organisation", self.o],
            ["Organizational unit", self.ou],
            ["Locality", self.l],
            ["State / Province", self.st],
            ["Country", self.c]
        ]
        return tabulate(table, tablefmt="psql")

    def get_dn(self):
        return "/C={}/ST={}/L={}/OU={}/O={}/CN={}".format(self.c, self.st, self.l, self.ou, self.o, self.cn)

    def __str__(self):
        return self.get_dn()

    def __repr__(self):
        return "<CertInfo {}>".format(self.get_dn())