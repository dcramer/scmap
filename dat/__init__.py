import units, flingy, sprites, images

def unit_get(x):
    return units.units[x].flingy.sprite.image.file

def unit_turns(x):
    return units.units[x].flingy.sprite.image.gfx_turns

def get_sprite(x):
    return sprites.sprites[x].image.file
