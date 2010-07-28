import os

import common
import images

class TechdataType(common.DatType):
    def __init__(self, number, attrs):
        common.DatType.__init__(self, number, attrs)
        self.icon = images.images[self.icon]
        self.label = None if self.label == 0 else common.stat_txt[self.label-1]
        self.race = ["zerg", "terran", "protoss", "all"][self.race]

class TechdataFile(common.DatFile):
    _count = 44
    _fields = [
        ('minerals', 'H', 0),
        ('gas', 'H', 44*2),
        ('time', 'H', 44*4),
        ('energy', 'H', 44*6),
        ('icon', 'H', 44*12),
        ('label', 'H', 44*14),
        ('race', 'B', 44*16),
        ('researched', 'B', 44*17),
        ('brood_war', 'B', 44*18),
    ]
    _item_type = TechdataType

techdata = TechdataFile(open(os.path.join(os.path.dirname(__file__), 'files/techdata.dat')))

if __name__ == "__main__":
    for x in xrange(techdata._count):
        print x, techdata[x].__dict__
