import struct
import pygame

import file
import tile

def load():
    global stars
    palette = tile.tiles["platform"].subpalettes["blue"]
    f = file.open("parallax", "star.spk")
    header = struct.unpack("<H",f.read(2))[0]
    header = struct.unpack("<"+str(header)+"H",f.read(header*2))
    
    star = []
    for x in range(len(header)):
        img = pygame.surface.Surface((640,480),pygame.SRCALPHA,32)
        layer = []
        for y in range(header[x]):
            posx, posy, posfile = struct.unpack("<3H2x",f.read(8))
            pos = f.tell() ; f.seek(posfile)
            sizex, sizey = struct.unpack("<2H",f.read(4))
            data = f.read(sizex*sizey)
            f.seek(pos)
            surf = pygame.image.fromstring(data,(sizex,sizey),"P")
            surf.set_palette(palette)
            surf.set_colorkey(0)
            for xadd in (-640,0,640):
                for yadd in (-480,0,480):
                    img.blit(surf,(posx-sizex/2+xadd,posy-sizex/2+yadd))
        star.append(img)
    stars = pygame.Surface((640,480))
    for x in star:
        #for xadd in (0,320/2,320,320*3/2):
        #    for yadd in (0,240/2,240,240*3/2):
                stars.blit(x, (xadd, yadd))
    #stars = pygame.transform.smoothscale(stars, (1280, 960))
    return stars

