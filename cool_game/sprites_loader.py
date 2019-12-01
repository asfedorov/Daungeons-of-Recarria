import pyglet


class BaseTileManager:
    _asset_path = None
    # высота / длина
    _sheet_size = None, None
    _tile_size = None, None

    def __init__(self):
        self.tiles = self._load_tiles_grid()

    def _load_tiles_grid(self):
        img = pyglet.image.load(self._asset_path)
        return pyglet.image.ImageGrid(
            img,
            self._sheet_size[0]//self._tile_size[0],
            self._sheet_size[1]//self._tile_size[1],
            item_height=self._tile_size[0],
            item_width=self._tile_size[1]
        ).get_texture_sequence()


class DungeonTiles(BaseTileManager):
    _asset_path = "./assets/sprites/tiles_dungeon_spritesheet.png"
    # высота / длина
    _sheet_size = 384, 320
    _tile_size = 16, 16

    _row_len = _sheet_size[1]//_tile_size[1]

    def _get_floor_tiles(self):
        return self.tiles[
            (self._row_len)*(16//16)+80//16:(self._row_len)*(16//16)+80//16+32//16
        ] + self.tiles[
            (self._row_len)*(32//16)+80//16:(self._row_len)*(32//16)+80//16+48//16
        ] + self.tiles[
            (self._row_len)*(272//16):(self._row_len)*(272//16)+16//16
        ] * 10 + self.tiles[
            (self._row_len)*(288//16):(self._row_len)*(288//16)+32//16
        ] * 10 + self.tiles[
            (self._row_len)*(304//16):(self._row_len)*(304//16)+16//16
        ] * 20 + self.tiles[
            (self._row_len)*(288//16)+192//16:(self._row_len)*(288//16)+192//16 + 2
        ] + self.tiles[
            (self._row_len)*(304//16)+192//16:(self._row_len)*(304//16)+192//16 + 2
        ]

    def _get_cracked_tiles(self):
        # return self.tiles[
        #     (self._row_len)*(272//16)+16//16:(self._row_len)*(272//16)+16//16+32//16
        # ] + self.tiles[
        #     (self._row_len)*(288//16)+32//16:(self._row_len)*(288//16)+32//16+16//16
        # ] + self.tiles[
        #     (self._row_len)*(304//16)+16//16:(self._row_len)*(304//16)+16//16+32//16
        # ]

        return self.tiles[
            (self._row_len)*(256//16)+112//16:(self._row_len)*(256//16)+112//16 + 2
        ] + self.tiles[
            (self._row_len)*(272//16)+112//16:(self._row_len)*(272//16)+112//16 + 2
        ] + self.tiles[
            (self._row_len)*(288//16)+112//16:(self._row_len)*(288//16)+112//16 + 2
        ] + self.tiles[
            (self._row_len)*(304//16)+112//16:(self._row_len)*(304//16)+112//16 + 2
        ]

    def _get_cave_tiles(self):
        return self.tiles[
            (self._row_len)*(304//16)+48//16:(self._row_len)*(304//16)+48//16+16//16
        ]

    def _get_wall_tiles(self):
        return self.tiles[
            (self._row_len)*(0//16):(self._row_len)*(0//16)+64//16
        ] + self.tiles[
            (self._row_len)*(16//16):(self._row_len)*(16//16)+64//16
        ] + self.tiles[
            (self._row_len)*(32//16):(self._row_len)*(32//16)+64//16
        ] + self.tiles[
            (self._row_len)*(48//16):(self._row_len)*(48//16)+64//16
        ]

    def _get_wall_erode_tiles(self):
        return self.tiles[
            (self._row_len)*(48//16)+80//16:(self._row_len)*(48//16)+80//16+16//16
        ] + self.tiles[
            (self._row_len)*(48//16)+112//16:(self._row_len)*(48//16)+112//16+16//16
        ] + self.tiles[
            (self._row_len)*(138//16)+144//16:(self._row_len)*(138//16)+144//16+16//16
        ]

    def _get_water_tiles(self):
        return self.tiles[
            (self._row_len)*(0//16)+192//16:(self._row_len)*(0//16)+192//16+16//16
        ] + self.tiles[
            (self._row_len)*(16//16)+192//16:(self._row_len)*(16//16)+192//16+16//16
        ]

    def _get_down_tiles(self):
        return self.tiles[
            (self._row_len)*(122//16)+144//16:(self._row_len)*(122//16)+144//16+16//16
        ]

    def _get_up_tiles(self):
        return self.tiles[
            (self._row_len)*(122//16)+160//16:(self._row_len)*(122//16)+160//16+16//16
        ] + self.tiles[
            (self._row_len)*(138//16)+160//16:(self._row_len)*(138//16)+160//16+16//16
        ]

    @property
    def floor(self):
        return self._get_floor_tiles()

    @property
    def wall(self):
        return self._get_wall_tiles()

    @property
    def wall_erode(self):
        return self._get_wall_erode_tiles()

    @property
    def crack(self):
        return self._get_cracked_tiles()

    @property
    def cave(self):
        return self._get_cave_tiles()

    @property
    def water(self):
        return self._get_water_tiles()

    @property
    def up(self):
        return self._get_up_tiles()

    @property
    def down(self):
        return self._get_down_tiles()


class PlayerTiles(BaseTileManager):
    _asset_path = "./assets/sprites/chara_hero.png"
    # высота / длина
    _sheet_size = 528, 192
    _tile_size = 48, 48

    @property
    def up(self):
        return self.tiles[
            4*6:4*6 + 4
        ]

    @property
    def left(self):
        return self.tiles[
            4*7:4*7 + 4
        ]

    @property
    def down(self):
        return self.tiles[
            4*8:4*8 + 4
        ]
