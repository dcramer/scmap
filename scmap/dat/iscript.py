import os
import struct
import random

import cdict
import opcodes

names = "initial death ground_attk air_attk unused1 ground_rep air_rep spell".split(' ')
names += "ground_stop air_stop unused2 walk stop_walk special1 special2".split(' ')
names += "almost_built built landing liftoff isworking workingtoidle warp_in".split(' ')
names += "unused3 staredit_initial disable burrow unburrow enable".split(' ')

class IScriptEntryIterator(object):
    def __init__(self, data, p):
        self.data = data
        self.p = p
    def next(self, random=random):
        try:
         opc = self.data[self.p]
        except:
         raise NotImplementedError
        self.p += 1
        c = struct.unpack('B', opc)[0]
        name, type, args, desc = opcodes.opcodes[c]
        s = struct.calcsize('<%s'%type)
        arg = struct.unpack('<%s'%type, self.data[self.p:self.p+s])
        self.p += s
        d = {}
        for key, val in zip(args, arg):
            if key == 'dest':
                val = IScriptEntryIterator(self.data, val)
            d[key] = val
        return name, d

class IScriptEntry(object):
    def __init__(self, data, p):
        self.data = data
        self.p = p
    def __iter__(self):
        return IScriptEntryIterator(self.data, self.p)

class IScriptDir(object):
    def __init__(self, data, p):
        assert data[p:p+4] == "SCPE"
        self.type = struct.unpack("B", data[p+4:p+5])[0]
        spacer =  struct.unpack("BBB", data[p+5:p+8])
        assert spacer == (0, 0, 0)
        count = 28
        #count = max(self.type, 16)
        for x in xrange(count):
            y = struct.unpack("H", data[p+8+2*x:p+8+2*(x+1)])[0]
            if y:
                setattr(self, names[x], IScriptEntry(data, y))

class IScript(cdict.cdict):
    def __init__(self, file):
        cdict.cdict.__init__(self, self._read_dir)
        self.data = file.read()
        self.pointers = {}
        p = struct.unpack("H", self.data[:2])[0]
        while True:
        #assert self.data[-4:] == '\xff\xff\x00\x00'
        #for i in xrange(1, len(self.data)//4):
            if not self.data[p:p+4]: break
            id, dest = struct.unpack("HH", self.data[p:p+4])
            p += 4
            if id not in self.pointers:
                self.pointers[id] = dest
    
    def _read_dir(self, id):
        p = self.pointers[id]
        return IScriptDir(self.data, p)

iscript = IScript(open(os.path.join(os.path.dirname(__file__), 'files/iscript.bin')))

if __name__ == "__main__":
    print dir(iscript[0])
