import os

import common
import images

class UpgradesType(common.DatType):
    def __init__(self, number, attrs):
        common.DatType.__init__(self, number, attrs)
        self.icon = images.images[self.icon]
        self.label = common.stat_txt[self.label]
        self.race = ["zerg", "terran", "protoss", "all"][self.race]

class UpgradesFile(common.DatFile):
    _count = 61
    _fields = [
        ('minerals', 'H', 61*0),
        ('minerals_factor', 'H', 61*2),
        ('gas', 'H', 61*4),
        ('gas_factor', 'H', 61*6),
        ('time', 'H', 61*8),
        ('time_factor', 'H', 61*10),
        ('icon', 'H', 61*14),
        ('label', 'H', 61*16),
        ('race', 'B', 61*18),
        ('repeats', 'B', 61*19),
        ('brood_war', 'B', 61*20),
    ]
    _item_type = UpgradesType

upgrades = UpgradesFile(open(os.path.join(os.path.dirname(__file__), 'files/upgrades.dat')))

if __name__ == "__main__":
    for x in xrange(upgrades._count):
        print x, upgrades[x].__dict__
