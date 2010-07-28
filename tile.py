import struct
import pygame
import os, time

import cdict
import file

class Tileset(cdict.cdict):
    def __init__(self, file_prefix):
        cdict.cdict.__init__(self, self.read_tile)
        self.file_prefix = file_prefix
        for i in ("cv5", "vx4", "vr4", "wpe"):
            setattr(self, i, file.open("tileset", self.file_prefix + "." + i))
        self.palette = self.read_palette()
        self.minitiles = cdict.cdict(self.read_minitile)
        self.rows = cdict.cdict(self.read_row)
        self.subpalettes = cdict.cdict(self.read_subpalette)
    def read_palette(self):
        palette = self.wpe.read()
        palette = struct.unpack(str(len(palette))+"B",palette)
        return [palette[4*x:4*x+3] for x in range(len(palette)/4)]
    def read_subpalette(self, name):
        i = pygame.image.load(file.open("tileset", self.file_prefix, name+'.pcx'))
        #assert i.get_height() == 1
        return [i.get_at((x, 0))[:3] for x in xrange(i.get_width())]
    def read_minitile(self, index):
        if index % 2 == 1:
            return pygame.transform.flip(self.minitiles[index-1], True, False)
        else:
            self.vr4.seek(index/2*64)
            minitile = self.vr4.read(64)
            minitile = pygame.image.fromstring(minitile,(8,8),"P")
            minitile.set_palette(self.palette)
            return minitile
    def read_row(self, index):
        self.cv5.seek(52*index)
        row = self.cv5.read(52)
        return struct.unpack("26H",row)
    def read_tile(self, index):
        row = self.rows[index>>4]
        rowd = row[10:]
        i = rowd[index&15]
        tile = pygame.surface.Surface((32,32), 0, 8) # should be 8?
        tile.set_palette(self.palette)
        tile.set_colorkey(0)
        self.vx4.seek(i*32)
        minindex = struct.unpack("16H",self.vx4.read(32))
        for x in range(4):
            for y in range(4):
                tile.blit(self.minitiles[minindex[x+y*4]],(x*8,y*8))
        return tile
        
tiles = cdict.cdict(Tileset)
