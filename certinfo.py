__author__ = 'Martijn Braam <martijn@brixit.nl>'
from tabulate import tabulate


class CertInfo:
    cn = ""
    c = ""
    l = ""
    st = ""
    o = ""
    ou = ""
    san = ""

    def get_table(self):
        table = [
            ["Common name", self.cn],
            ["Organisation", self.o],
            ["Organizational unit", self.ou],
            ["Locality", self.l],
            ["State / Province", self.st],
            ["Country", self.c]
        ]
        if self.san != "":
            table.append(["Alternative names", self.san.replace(",", "\n")])
        return tabulate(table, tablefmt="psql")

    def get_dn(self):
        return "/C={}/ST={}/L={}/OU={}/O={}/CN={}".format(self.c, self.st, self.l, self.ou, self.o, self.cn)

    def from_dn(self, dn):
        fields = dn.split("/")[1:]
        parsed = {}
        for field in fields:
            part = field.split("=")
            parsed[part[0].lower()] = part[1]

        if "c" in parsed.keys():
            self.c = parsed["c"]
        if "l" in parsed.keys():
            self.l = parsed["l"]
        if "st" in parsed.keys():
            self.st = parsed["st"]
        if "ou" in parsed.keys():
            self.ou = parsed["ou"]
        if "cn" in parsed.keys():
            self.cn = parsed["cn"]
        if "o" in parsed.keys():
            self.o = parsed["o"]

    def __str__(self):
        return self.get_dn()

    def __repr__(self):
        return "<CertInfo {}>".format(self.get_dn())