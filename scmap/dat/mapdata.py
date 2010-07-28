import os

import common

class MapdataType(common.DatType):
    def __init__(self, number, attrs, tbl):
        common.DatType.__init__(self, number, attrs)
        self.file = tbl[self.file-1]

class MapdataFile(common.DatTblFile):
    _count = 65
    _fields = [
        ('file', 'I', 65*0),
    ]
    _item_type = MapdataType

mapdata = MapdataFile(
    open(os.path.join(os.path.dirname(__file__), 'files/mapdata.dat')),
    open(os.path.join(os.path.dirname(__file__), 'files/mapdata.tbl')),
)

if __name__ == "__main__":
    for x in xrange(mapdata._count):
        print x, mapdata[x].__dict__
