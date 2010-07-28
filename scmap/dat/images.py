import os

import common
import iscript

class ImagesType(common.DatType):
    def __init__(self, number, attrs, tbl):
        common.DatType.__init__(self, number, attrs)
        self.file = 'unit\\%s' % tbl[self.file-1]
        self.iscript = iscript.iscript[self.iscript]
        self.overlay = self.overlay1, self.overlay2, self.overlay3, self.overlay4, self.overlay5, self.overlay6
        self.overlay = tuple(None if x == 0 else tbl[x-1] for x in self.overlay)
        del self.overlay1, self.overlay2, self.overlay3, self.overlay4, self.overlay5, self.overlay6
        if self.palette_type != 9:
            del self.palette

class ImagesFile(common.DatTblFile):
    _count = 999
    _fields = [
        ('file', 'I', 999*0),
        ('gfx_turns', 'B', 999*4),
        ('shadows_turns', 'B', 999*5),
        ('unknown', 'B', 999*6),
        ('floats', 'B', 999*7),
        ('palette_type', 'B', 999*8),
        ('palette', 'B', 999*9),
        ('iscript', 'I', 999*10),
        ('overlay1', 'I', 999*14),
        ('overlay2', 'I', 999*18),
        ('overlay3', 'I', 999*22),
        ('overlay4', 'I', 999*26),
        ('overlay5', 'I', 999*30),
        ('overlay6', 'I', 999*34),
    ]
    _item_type = ImagesType

images = ImagesFile(
    open(os.path.join(os.path.dirname(__file__), 'files/images.dat')),
    open(os.path.join(os.path.dirname(__file__), 'files/images.tbl')),
)
if __name__ == "__main__":
    for x in xrange(images._count):
        print x, images[x].__dict__
