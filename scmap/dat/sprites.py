import os

import common
import images

class SpritesType(common.DatType):
    def __init__(self, number, attrs):
        common.DatType.__init__(self, number, attrs)
        self.image = images.images[self.image]
        if number >= 130:
            self.selcircle = images.images[self.selcircle+561]
        else:
            del self.bar_length, self.selcircle, self.selcircle_y

class SpritesFile(common.DatFile):
    _count = 517
    _fields = [
        ('image', 'H', 517*0-130*0),
        ('bar_length', 'B', 517*2-130*1),
        ('unknown1', 'B', 517*3-130*1),
        ('unknown2', 'B', 517*4-130*1),
        ('selcircle', 'B', 517*5-130*2),
        ('selcircle_y', 'b', 517*6-130*3),
    ]
    _item_type = SpritesType

sprites = SpritesFile(open(os.path.join(os.path.dirname(__file__), 'files/sprites.dat')))

if __name__ == "__main__":
    for x in xrange(sprites._count):
        print x, sprites[x].__dict__
