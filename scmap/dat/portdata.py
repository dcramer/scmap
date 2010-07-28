import os

import common

class PortdataType(common.DatType):
    def __init__(self, number, attrs, tbl):
        common.DatType.__init__(self, number, attrs)
        self.file = "portrait\\%s.smk"%tbl[self.file-1]

class PortdataFile(common.DatTblFile):
    _count = 220
    _fields = [
        ('file', 'I', 220*0),
        ('unknown1', 'B', 220*4),
        ('unknown2', 'B', 220*5),
    ]
    _item_type = PortdataType

portdata = PortdataFile(
    open(os.path.join(os.path.dirname(__file__), 'files/portdata.dat')),
    open(os.path.join(os.path.dirname(__file__), 'files/portdata.tbl')),
)

if __name__ == "__main__":
    for x in xrange(portdata._count):
        print x, portdata[x].__dict__
