import os
import random

import pygame

from . import tile
from . import chk
from . import stars
from . import grp
from . import dat
from . import file

package_root = os.path.dirname(__file__)

def init(path):
    global team_colors
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.display.set_mode((1,1), 0, 32)
    file.init(path)
    colors = pygame.image.load(os.path.join(package_root, "tunit.pcx"))
    team_colors = [[colors.get_at((x+c*8,0))[0:3] for x in range(7)] for c in xrange(16)]

class PaletteCache(cdict.cdict):
    def __init__(self, surface, palette):
        self.surface = surface
        self.palette = palette
        cdict.cdict.__init__(self, self._get)
    def _get(self, palette):
        x = self.surface.subsurface(self.surface.get_rect())
        self.palette[8:15] = team_colors[palette]
        x.set_palette(self.palette)
        return x

def generate(filename):
    global star_res
    mapdim, tileset, tiles, doodad, units = chk.load(filename)
    t = tile.tiles[tileset]
    i = pygame.Surface((32*mapdim[0], 32*mapdim[1]))
    
    if tileset == "platform":
        try:
            star_res
        except NameError:
            star_res = stars.load()
        for x in xrange(0, mapdim[0]*32, 1280):
            for y in xrange(0, mapdim[1]*32, 960):
                i.blit(star_res, (x, y))
    
    for x in xrange(mapdim[0]):
        for y in xrange(mapdim[1]):
            i.blit(t[tiles[x][y]], (32*x, 32*y))
    
    for x in ('bfire', 'blue'):
        try:
           unit_pal = t.subpalettes[x]
        except: pass
        else: break
    grps = cdict.cdict(lambda x: [PaletteCache(y, unit_pal) for y in grp.load(file.open(x))])
    
    for type, (x, y), owner, res in units:
        d = grps[dat.unit_get(type)]
        index = 0
        if type == 188:
            index = chk.tileset_numbers[tileset]
        elif dat.unit_turns(type):
            index = random.randrange(17)
        d = d[index][owner]
        i.blit(d, (x-d.get_width()/2, y-d.get_height()/2))
    
    for number, x, y in doodad:
        d = dat.get_sprite(number)
        d = grp.load(file.open(d))
        d = random.choice(d)
        d.set_palette(t.palette)
        i.blit(d, (x-d.get_width()/2, y-d.get_height()/2))
    
    return i

init(os.path.join(package_root, "data"))



