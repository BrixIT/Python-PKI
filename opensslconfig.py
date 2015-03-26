__author__ = 'Martijn Braam <martijn@brixit.nl>'
import configparser
import itertools
import io


class OpenSSLConfig(configparser.ConfigParser):

    def read_file(self, f, source=None):
        with open(f) as stream:
            lines = itertools.chain(("[__global__]",), stream)
            super().read_file(lines)

    def optionxform(self, optionstr):
        return str(optionstr)

    def write(self, fp, space_around_delimiters=True):
        temp_buffer = io.StringIO()
        super().write(temp_buffer, space_around_delimiters)
        configfile = temp_buffer.getvalue()
        temp_buffer.close()
        lines = configfile.split("\n")[1:]
        with open(fp, "w") as stream:
            stream.write("\n".join(lines))