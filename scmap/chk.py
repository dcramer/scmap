import struct
import mpq
import StringIO

tilesets = {
    0: "badlands",
    1: "platform",
    2: "install",
    3: "ashworld",
    4: "jungle",
    5: "desert",
    6: "ice",
    7: "twilight",
}

tileset_numbers = dict((v,k) for k,v in tilesets.iteritems())

def load(filename):
    mf = StringIO.StringIO(mpq.Archive(filename)['staredit\\scenario.chk'])
        
    maps = {}
    while True:
        title = mf.read(4)
        if title == "": break
        data = mf.read(struct.unpack("<L",mf.read(4))[0])
        maps[title.strip(" ")] = data
        
    mapdim = struct.unpack("<2H", maps["DIM"])
    
    tileset = tilesets[struct.unpack("<H",maps["ERA"])[0]]
    
    
    tiles = struct.unpack("<"+str(len(maps["MTXM"])/2)+"H",maps["MTXM"])
    tiles = [tiles[x::mapdim[0]] for x in range(0,mapdim[0])]
    
    doodads = []
    thingy = StringIO.StringIO(maps["THG2"])
    while 1:
        raw = thingy.read(10)
        if raw == "": break
        number, x, y, owner, unknown, flag = struct.unpack("<HHHBBH", raw)
        doodads.append((number,x,y))
        
    unit = StringIO.StringIO(maps["UNIT"])
    units = []
    while 1:
        raw = unit.read(36)
        if raw == "": break
        serial, x, y, type, unknown, flag, validflag, owner, hp, shield, energy, resource, hanger, state, unknown2, unknown3 = struct.unpack("<LHHHHHHBBBBLHHLL", raw)
        units.append((type, (x, y), owner, resource))
    return mapdim, tileset, tiles, doodads, units
    
