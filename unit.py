import random

from dat import units
from dat import images
from dat import sprites

from dat import opcodes

class Sprite(object):
    def __init__(self, state, type, pos):
        self.type = type
        self.pos = pos
        self.iscript = iter(self.type.image.iscript.initial)
        self.overlays = []
        self.underlays = []
        self.shadows = []
        self.frame = None
        self.wait = 0
        self.direction = state.random.randrange(32)
        self.vert_offset = 0
        self.no_brk = False
    @property
    def draw_state(self):
        if self.frame is None:
            f = None
        else:
            f = self.frame+self.direction*self.type.image.gfx_turns
        return self.shadows, self.underlays, f, self.overlays
    def step(self, state):
        if self.wait:
            self.wait -= 1
            return
        while self.wait == 0:
            inst, args = self.iscript.next()
            #print inst, args
            name = "iscript_%s" % inst
            if not hasattr(self, name):
                print
                print
                print self.frame, self.direction, self.overlays
                print name, args
                print enumerate(opcodes.opcodes).next()
                num = [i for i, x in opcodes.opcodes.iteritems() if x[0] == inst][0]
                print hex(num), opcodes.opcodes[num]
                raise SystemExit
            res = getattr(self, "iscript_%s" % inst)(state, **args)
            if res:
                self.wait = res
        self.wait -= 1
    def iscript_imgol(self, state, image, x, y):
        self.overlays.append((images.images[image], x, y))
    def iscript_imgul(self, state, image, x, y):
        self.underlays.append((images.images[image], x, y))
    def iscript_playfram(self, state, frame):
        self.frame = frame
    def iscript_waitrand(self, state, gameticks1, gameticks2):
        return state.random.choice([gameticks1, gameticks2])
    def iscript_randcondjmp(self, state, chance, dest):
        if state.random.randrange(128) <= chance:
            self.iscript = dest
    def iscript_wait(self, state, gameticks):
        return gameticks
    def iscript_turnrand(self, state, amount):
        self.direction += state.random.choice([-1, 1]) * amount
        self.direction %= 32
    def iscript_goto(self, state, dest):
        self.iscript = dest
    def iscript_setfldirect(self, state, direction):
        self.direction = direction
    def iscript_setvertpos(self, state, y):
        self.vert_offset = y
    def iscript_setflspeed(self, state, speed):
        self.speed = speed
    def iscript_playsnd(self, state, sound):
        print "play", sound
    def iscript_playframtile(self, state, frame):
        self.frame = frame + state.tileset
    def iscript_sigorder(self, state, signal):
        print "sigorder", signal
    def iscript_nobrkcodestart(self, state):
        self.nobrk = True
    def iscript_nobrkcodeend(self, state):
        self.nobrk = False
    def iscript_sprol(self, state, sprite, x, y):
        state.add_sprite(Sprite(state, sprites.sprites[sprite], (x, y)))
    def iscript_turncwise(self, sprite, amount):
        self.direction += amount
        self.direction %= 32
    def iscript_turnccwise(self, sprite, amount):
        self.direction -= amount
        self.direction %= 32
    def iscript_imgulnextid(self, state, x, y):
        self.shadows.append((x, y))
    def iscript_creategasoverlays(self, state, overlay):
        print "GAS", overlay
    def iscript_pwrupcondjmp(self, state, dest):
        print "POWERUP"
    def iscript_setflipstate(self, state, flipstate):
        self.flipstate = flipstate

class Flingy(object):
    def __init__(self, state, type, pos):
        self.type = type
        self.sprite = Sprite(state, self.type.sprite, pos)
    def step(self, state):
        self.sprite.step(state)
    @property
    def draw_state(self):
        return self.sprite.draw_state

class Unit(object):
    def __init__(self, state, type, pos):
        self.type = type
        self.flingy = Flingy(state, self.type.flingy, pos)
    def apply_order(self, order):
        pass
    def step(self, state):
        self.flingy.step(state)
    @property
    def draw_state(self):
        return self.flingy.draw_state

class GameState(object):
    def __init__(self, random, tileset):
        self.random = random
        self.tileset = tileset
        self.units = []
        self.sprites = []
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
    def add_unit(self, unit):
        self.units.append(unit)
    def step(self, orders):
        for unit, order in orders:
            self.units[unit].apply_order(order)
        for unit in self.units:
            unit.step(self)
        for sprite in self.sprites:
            sprite.step(self)

if __name__ == "__main__":
    s = GameState(random, 0)
    for num in xrange(units.units._count):
      x = Unit(s, units.units[num], (0, 0))
      print
      print "starting", x.type.label, num, units.units._count
      for i in xrange(10000):
        x.step(s)
      print num, x.draw_state
