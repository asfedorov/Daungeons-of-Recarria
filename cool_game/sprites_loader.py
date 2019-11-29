import pyglet
from functools import lru_cache

_row_len = 320//16


@lru_cache(maxsize=None)
def load_tiles_grid():
    img = pyglet.image.load("assets/sprites/tiles_dungeon_spritesheet.png")
    return pyglet.image.ImageGrid(img, 384//16, _row_len, item_height=16, item_width=16)


def get_floor_tiles():
    tiles = load_tiles_grid().get_texture_sequence()
    return tiles[
        (_row_len)*(272//16):(_row_len)*(272//16)+16//16
    ] + tiles[
        (_row_len)*(288//16):(_row_len)*(288//16)+32//16
    ] + tiles[
        (_row_len)*(304//16):(_row_len)*(304//16)+16//16
    ]
    #  + tiles[
    #     (_row_len)*(16//16):(_row_len)*(16//16)+2//16
    # ] + tiles[
    #     (_row_len)*(32//16):(_row_len)*(32//16)+3//16
    # ] + tiles[
    #     (_row_len)*(48//16):(_row_len)*(48//16)+3//16
    # ]


def get_cracked_tiles():
    tiles = load_tiles_grid().get_texture_sequence()
    return tiles[
        (_row_len)*(272//16)+16//16:(_row_len)*(272//16)+16//16+32//16
    ] + tiles[
        (_row_len)*(288//16)+32//16:(_row_len)*(288//16)+32//16+16//16
    ] + tiles[
        (_row_len)*(304//16)+16//16:(_row_len)*(304//16)+16//16+32//16
    ]


def get_cave_tiles():
    tiles = load_tiles_grid().get_texture_sequence()
    return tiles[
        (_row_len)*(304//16)+48//16:(_row_len)*(304//16)+48//16+16//16
    ]


def get_wall_tiles():
    tiles = load_tiles_grid().get_texture_sequence()
    return tiles[
        (_row_len)*(0//16):(_row_len)*(0//16)+64//16
    ] + tiles[
        (_row_len)*(16//16):(_row_len)*(16//16)+64//16
    ] + tiles[
        (_row_len)*(32//16):(_row_len)*(32//16)+64//16
    ] + tiles[
        (_row_len)*(48//16):(_row_len)*(48//16)+64//16
    ]
