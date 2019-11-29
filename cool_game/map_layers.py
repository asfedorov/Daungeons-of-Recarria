import random

import cocos
import cocos.collision_model as cm

import map_gen
import sprites_loader
from collisions_managers import PLAYER_WALL_COLLISION_MANAGER
from collisions_managers import PLAYER_WATER_COLLISION_MANAGER


class CollisionLayer(cocos.layer.ScrollableLayer):
    pass


class MyRectMapLayer(cocos.tiles.RectMapLayer):
    def set_cell_sprite_opacity(self, i, j, opacity):
        cell = self.get_cell(i, j)
        if cell is None:
            return
        key = cell.origin[:2]
        if key in self._sprites:
            self._sprites[key].opacity = opacity

    def get_visible_cells(self):
        x, y = self.view_x / 1.5, self.view_y / 1.5
        w, h = self.view_w, self.view_h
        return self.get_in_region(x, y, x + w, y + h)


class WallsLayer(MyRectMapLayer):
    pass


class UpperLayer(MyRectMapLayer):
    pass


class FloorLayer(MyRectMapLayer):
    _tile_size = 16, 16
    _scale_me = 1
    _pos_offset = 8 * _scale_me

    def __init__(self, width, height, rooms):
        properties = {
            'width': width,
            'height': height,
            'px_width': width * 16 * 1.5,
            'px_heigth': height * 16 * 1.5,
            'tw': 16 * 1.5,
            'th': 16 * 1.5
        }
        self.start_point = None
        self.player = None

        self._collision_layer = CollisionLayer()
        self._collision_layer.visible = False

        cells_dict_lvl0 = {}
        cells_dict_lvl1 = {}
        cells_dict_lvl2 = {}

        cell_water = []
        cell_deep_water = []

        dungeon_tiles = sprites_loader.DungeonTiles()

        floor_tiles = dungeon_tiles.floor
        wall_tiles = dungeon_tiles.wall
        wall_erode_tiles = dungeon_tiles.wall_erode
        crack_tiles = dungeon_tiles.crack
        cave_tiles = dungeon_tiles.cave
        water_tiles = dungeon_tiles.water
        down_tiles = dungeon_tiles.down
        up_tiles = dungeon_tiles.up
        blank_tile = dungeon_tiles.tiles[5]

        map_field = map_gen.Map(width, height, rooms)
        # print(map_field)
        for i, j, col in map_field._iter_tiles_from_field():
            if j not in cells_dict_lvl0:
                cells_dict_lvl0[j] = []
                cells_dict_lvl1[j] = []
                cells_dict_lvl2[j] = []

            image_obj = random.choice(floor_tiles)
            # image_obj1 = blank_tile
            image_obj1 = None
            image_obj2 = None

            sprite_obj_w = None

            if col == map_gen.CRACK_TILE:
                image_obj = random.choice(crack_tiles)
            elif col == map_gen.CAVE_TILE:
                image_obj = random.choice(cave_tiles)
            elif col == map_gen.WATER_TILE:
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
                image_obj2 = random.choice(water_tiles)
                cell_water.append((j, i))
            elif col == map_gen.DEEP_WATER_TILE:
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
                image_obj2 = random.choice(water_tiles)
                cell_deep_water.append((j, i))
            elif col == map_gen.DOWN_TILE:
                image_obj2 = random.choice(down_tiles)

                self.start_point = (
                    self._pos_offset + (self._tile_size[0]*self._scale_me*j) * 1.5,
                    self._pos_offset + (self._tile_size[1]*self._scale_me*i) * 1.5
                )

            elif col == map_gen.UP_TILE:
                image_obj2 = up_tiles[0]
            elif col == map_gen.WALL_TILE:
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
                image_obj1 = random.choice(wall_tiles)
            elif col == map_gen.WALL_ERODE_TILE:
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
                image_obj1 = random.choice(wall_erode_tiles)

            tile0 = cocos.tiles.Tile(
                't0.{}{}'.format(j, i),
                {},
                image_obj,
            )
            cell0 = cocos.tiles.RectCell(
                j,
                i,
                16,
                16,
                {},
                tile0
            )
            cells_dict_lvl0[j].append(cell0)

            if image_obj1:
                tile1 = cocos.tiles.Tile(
                    't1.{}{}'.format(j, i),
                    {},
                    image_obj1,
                )
            else:
                tile1 = None
            cell1 = cocos.tiles.RectCell(
                j,
                i,
                16,
                16,
                {},
                tile1
            )
            cells_dict_lvl1[j].append(cell1)

            if image_obj2:
                tile2 = cocos.tiles.Tile(
                    't2.{}{}'.format(j, i),
                    {},
                    image_obj2,
                )
            else:
                tile2 = None
            cell2 = cocos.tiles.RectCell(
                j,
                i,
                16,
                16,
                {},
                tile2
            )
            cells_dict_lvl2[j].append(cell2)

            if sprite_obj_w:
                sprite_obj_w.position = (
                    self._pos_offset + (self._tile_size[0]*self._scale_me*j) * 1.5,
                    self._pos_offset + (self._tile_size[1]*self._scale_me*i) * 1.5
                )
                self._collision_layer.add(sprite_obj_w)
                if col == map_gen.WALL_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        8 * 1.5,
                        8 * 1.5
                    )
                    PLAYER_WALL_COLLISION_MANAGER.add(sprite_obj_w)
                elif col == map_gen.WALL_ERODE_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        2 * 1.5,
                        2 * 1.5
                    )
                    PLAYER_WALL_COLLISION_MANAGER.add(sprite_obj_w)
                elif col in (map_gen.WATER_TILE, map_gen.DEEP_WATER_TILE):
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        8 * 1.5,
                        8 * 1.5
                    )
                    PLAYER_WATER_COLLISION_MANAGER.add(sprite_obj_w)
            # sprite_obj_w = None
            # sprite_obj_w2 = None


            # if sprite_obj_w:
            #     sprite_obj_w.position = (
            #         self._pos_offset + (self._tile_size[0]*self._scale_me*j),
            #         self._pos_offset + (self._tile_size[1]*self._scale_me*i)
            #     )
            #     sprite_obj_w.scale = self._scale_me



            #     self.add(sprite_obj_w, 10)

            # if sprite_obj_w2:
            #     sprite_obj_w2.position = (
            #         self._pos_offset + (self._tile_size[0]*self._scale_me*j),
            #         self._pos_offset + (self._tile_size[1]*self._scale_me*(i+1))
            #     )
            #     sprite_obj_w2.scale = self._scale_me
            #     upper_layer.add(sprite_obj_w2)

        super().__init__(
            0,
            16,
            16,
            list(cells_dict_lvl0.values()),
            properties=properties
        )

        walls_layer = WallsLayer(
            1,
            16,
            16,
            list(cells_dict_lvl1.values()),
            properties=properties
        )
        upper_layer = UpperLayer(
            2,
            16,
            16,
            list(cells_dict_lvl2.values()),
            properties=properties
        )
        for i, j in cell_water:
            upper_layer.set_cell_sprite_opacity(i, j, 10)
        for i, j in cell_deep_water:
            upper_layer.set_cell_sprite_opacity(i, j, 200)
        walls_layer.scale = 1.5
        upper_layer.scale = 1.5
        # self.position = 0, 0
        self.scale = 1.5
        self.walls = walls_layer
        self.upper = upper_layer

        self.px_width = width * 16 * 1.5
        self.px_height = height * 16 * 1.5


class DungeonLayer(cocos.layer.ScrollingManager):
    def __init__(self, width, height, rooms, viewport=None):
        super().__init__(
            viewport=viewport
        )

        self.player = None
        self.floor_layer = FloorLayer(width, height, rooms)
        self.add(self.floor_layer, z=1)
        self.add(self.floor_layer.walls, z=3)
        self.add(self.floor_layer.upper, z=5)
        self.add(self.floor_layer._collision_layer)

        self.schedule(self.update)

    def update(self, dt):
        if self.player:
            self.set_focus(*self.player.position)

    def on_cocos_resize(self, usable_width, usable_height):
        if self.player:
            self.player.world_size = usable_width, usable_height
