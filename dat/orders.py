import os

import common
import weapons
import techdata

class OrdersType(common.DatType):
    def __init__(self, number, attrs):
        common.DatType.__init__(self, number, attrs)
        self.label = common.stat_txt[self.label-1]
        self.weapon = None if self.weapon == 130 else weapons.weapons[self.weapon]
        self.tech = None if self.tech >= 44 else techdata.techdata[self.tech]
        if self.emulate == number:
            self.emulate = self
        else:
            self.emulate = orders[self.emulate]

class OrdersFile(common.DatFile):
    _count = 189
    _fields = [
        ('label', 'H', 189*0),
        ('unk1', 'B', 189*2),
        ('unk2', 'B', 189*3),
        ('unk3', 'B', 189*4),
        ('unk4', 'B', 189*5),
        ('unk5', 'B', 189*6),
        ('unk6', 'B', 189*7),
        ('unk7', 'B', 189*8),
        ('unk8', 'B', 189*9),
        ('unk9', 'B', 189*10),
        ('unk10', 'B', 189*11),
        ('unk11', 'B', 189*12),
        ('unk12', 'B', 189*13),
        ('weapon', 'B', 189*14),
        ('tech', 'B', 189*14),
        ('type', 'B', 189*16),
        ('unknown', 'H', 189*19),
        ('group', 'B', 189*18),
        ('emulate', 'B', 189*21),
    ]
    _item_type = OrdersType

orders = OrdersFile(open(os.path.join(os.path.dirname(__file__), 'files/orders.dat')))

if __name__ == "__main__":
    for x in xrange(orders._count):
        print x, orders[x].__dict__
