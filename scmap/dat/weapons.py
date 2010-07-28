"""
flags:

0x001 Air
0x002 Ground
0x004 lockdown
0x008 consume
0x010 spider mines, lockdown, parasite, spawn broodlings, consume,
    psionic storm
0x020 spawn broodlings
0x040 maelstrom, feedback, mind control, restoration, psionic storm,
    statis field, plague, ensnare, irradiate, emp shockwave
0x080 spawn broodlings
0x100 consume
"""

import os

import common
import sprites
import images
import upgrades

class WeaponsType(common.DatType):
    def __init__(self, number, attrs):
        common.DatType.__init__(self, number, attrs)
        self.label = common.stat_txt[self.label-1]
        self.sprite = sprites.sprites[self.sprite]
        self.spell = ["none", "lockdown", "emp shockwave", "spider mines", "unk1", "unk2", "unk3", "irradiate", "yamato gun", "unk4", "unk5", "unk6", "unk7", "broodlings", "dark swarm", "plague", "consume", "ensnare", "parasite", "psi storm", "unk8", "unk9", "stasis", "unk10", "restoration", "disruption web", "unk11", "unk12", "unk13", "feedback", "optical flare", "maelstrom", "unk14", "unk15", "unk16", "unk17", "unk18", "unk19", "unk20", "unk21", "unk22", "unk23", "unk24", "unk25", None][self.spell]
        self.range = self.range_min, self.range_max
        del self.range_min, self.range_max
        self.upgrade = upgrades.upgrades[self.upgrade]
        self.type = ["unknown", "explosive", "concussive", "normal", "spell"][self.type]
        self.explosion = [None, "normal", "radial splash", "line splash", "lockdown", "nuclear missile", "parasite", "broodlings", "emp shockwave", "irradiate", "ensnare", "plague", "stasis", "dark swarm", "consume", "yamato gun", "restoration", "disruption web", "corrosive acid", "mind control", "feedback", "optical flare", "maelstrom", "unk2", "air splash"][self.explosion]
        self.splash = self.splash_inner, self.splash_middle, self.splash_outer
        del self.splash_inner, self.splash_middle, self.splash_outer
        self.error_msg = common.stat_txt[self.error_msg-1]
        self.icon = images.images[self.icon]

class WeaponsFile(common.DatFile):
    _count = 130
    _fields = [
        ("label", "H", 130*0),
        ("sprite", "I", 130*2),
        ("spell", "B", 130*6),
        ("flag", "H", 130*7),
        ("range_min", "I", 130*9),
        ("range_max", "I", 130*13),
        ("upgrade", "B", 130*17),
        ("type", "B", 130*18),
        ("mbehavior", "B", 130*19),
        ("mtype", "B", 130*20),
        ("explosion", "B", 130*21),
        ("splash_inner", "H", 130*22),
        ("splash_middle", "H", 130*24),
        ("splash_outer", "H", 130*26),
        ("damage", "H", 130*28),
        ("bonus", "H", 130*30),
        ("cool", "B", 130*31),
        ("factor", "B", 130*32),
        ("pos1", "H", 130*34),
        ("pos2", "H", 130*36),
        ("error_msg", "H", 130*38),
        ("icon", "H", 130*40),
    ]
    _item_type = WeaponsType

weapons = WeaponsFile(open(os.path.join(os.path.dirname(__file__), 'files/weapons.dat')))

if __name__ == "__main__":
    for x in xrange(weapons._count):
        print x, weapons[x].__dict__
