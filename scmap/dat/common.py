import os
import struct

import cdict
import tbl

def read_field((name, type, start), count, dat_file):
    dat_file.seek(start)
    type = '<%i%s' % (count, type)
    return struct.unpack(type, dat_file.read(struct.calcsize(type)))

class DatType(object):
    def __init__(self, number, attrs):
        for key, value in attrs:
            setattr(self, key, value)

class DatFile(cdict.cdict):
    #_fields = None
    _item_type = DatType
    #_count = None
    def __init__(self, dat_file):
        cdict.cdict.__init__(self, self._read_item)
        self.data = zip(*[read_field(field, self._count, dat_file) for field in self._fields])
    def _read_item(self, key):
        return self._item_type(key, zip([x[0] for x in self._fields], self.data[key]))

class DatTblFile(DatFile):
    def __init__(self, dat_file, tbl_file):
        DatFile.__init__(self, dat_file)
        self._tbl = tbl.read(tbl_file)
    def _read_item(self, key):
        return self._item_type(key, zip([x[0] for x in self._fields], self.data[key]), self._tbl)

stat_txt = tbl.read(open(os.path.join(os.path.dirname(__file__), 'files/stat_txt.tbl')))
