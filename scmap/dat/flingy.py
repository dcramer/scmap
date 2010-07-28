import os

import common
import sprites

class FlingyType(common.DatType):
    def __init__(self, number, attrs):
        common.DatType.__init__(self, number, attrs)
        self.sprite = sprites.sprites[self.sprite]
        self.move_control = ["flingy", "partial", "iscript"][self.move_control]

class FlingyFile(common.DatFile):
    _count = 209
    _fields = [
        ('sprite', 'H', 209*0),
        ('speed', 'I', 209*2),
        ('turn_style', 'H', 209*6),
        ('acceleration', 'I', 209*8),
        ('turn_radius', 'B', 209*12),
        ('unknown', 'B', 209*13),
        ('move_control', 'B', 209*14),
    ]
    _item_type = FlingyType

flingy = FlingyFile(open(os.path.join(os.path.dirname(__file__), 'files/flingy.dat')))

if __name__ == "__main__":
    for x in xrange(flingy._count):
        print x, flingy[x].__dict__
