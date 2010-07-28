import os

import common

class SfxdataType(common.DatType):
    def __init__(self, number, attrs, tbl):
        common.DatType.__init__(self, number, attrs)
        self.file = tbl[self.file-1]

class SfxdataFile(common.DatTblFile):
    _count = 1144
    _fields = [
        ('file', 'I', 1144*0),
        ('unknown1', 'B', 1144*4),
        ('unknown2', 'B', 1144*5),
        ('unknown3', 'H', 1144*6),
        ('unknown4', 'B', 1144*8),
    ]
    _item_type = SfxdataType

sfxdata = SfxdataFile(
    open(os.path.join(os.path.dirname(__file__), 'files/sfxdata.dat')),
    open(os.path.join(os.path.dirname(__file__), 'files/sfxdata.tbl')),
)

if __name__ == "__main__":
    for x in xrange(sfxdata._count):
        print x, sfxdata[x].__dict__
