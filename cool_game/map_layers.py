import random

import cocos
import cocos.collision_model as cm

import map_gen
import sprites_loader
from collisions_managers import PLAYER_WALL_COLLISION_MANAGER
from collisions_managers import PLAYER_WATER_COLLISION_MANAGER


class WallAndDecoysLayer(cocos.layer.ScrollableLayer):
    pass


class UpperLayer(cocos.layer.ScrollableLayer):
    pass


class FloorLayer(cocos.layer.ScrollableLayer):
    _tile_size = 16, 16
    _scale_me = 1.5
    _pos_offset = 8 * _scale_me

    def __init__(self, width, height, rooms):
        super().__init__()
        self.start_point = None
        self.player = None

        walls_nad_decoys_layer = WallAndDecoysLayer()
        upper_layer = UpperLayer()

        dungeon_tiles = sprites_loader.DungeonTiles()

        floor_tiles = dungeon_tiles.floor
        wall_tiles = dungeon_tiles.wall
        wall_erode_tiles = dungeon_tiles.wall_erode
        crack_tiles = dungeon_tiles.crack
        cave_tiles = dungeon_tiles.cave
        water_tiles = dungeon_tiles.water
        down_tiles = dungeon_tiles.down
        up_tiles = dungeon_tiles.up

        map_field = map_gen.Map(width, height, rooms)
        # print(map_field)
        for i, j, col in map_field._iter_tiles_from_field():
            sprite_obj = None
            if col == map_gen.CRACK_TILE:
                sprite_obj = cocos.sprite.Sprite(random.choice(crack_tiles))
            elif col == map_gen.CAVE_TILE:
                sprite_obj = cocos.sprite.Sprite(random.choice(cave_tiles))
            elif col == map_gen.DEEP_WATER_TILE:
                sprite_obj = cocos.sprite.Sprite(random.choice(crack_tiles))
            else:
                sprite_obj = cocos.sprite.Sprite(random.choice(floor_tiles))

            sprite_obj.position = (
                self._pos_offset + (self._tile_size[0]*self._scale_me*j),
                self._pos_offset + (self._tile_size[1]*self._scale_me*i)
            )
            sprite_obj.scale = self._scale_me
            self.add(sprite_obj)

            sprite_obj_w = None
            sprite_obj_w2 = None

            if col == map_gen.WALL_TILE:
                sprite_obj_w = cocos.sprite.Sprite(random.choice(wall_tiles))
            elif col == map_gen.WALL_ERODE_TILE:
                sprite_obj_w = cocos.sprite.Sprite(random.choice(wall_erode_tiles))
            elif col == map_gen.WATER_TILE:
                sprite_obj_w = cocos.sprite.Sprite(random.choice(water_tiles))
                sprite_obj_w.opacity = 100
            elif col == map_gen.DEEP_WATER_TILE:
                sprite_obj_w = cocos.sprite.Sprite(random.choice(water_tiles))
                sprite_obj_w.opacity = 200
            elif col == map_gen.DOWN_TILE:
                sprite_obj_w = cocos.sprite.Sprite(random.choice(down_tiles))
            elif col == map_gen.UP_TILE:
                sprite_obj_w = cocos.sprite.Sprite(up_tiles[0])
                sprite_obj_w2 = cocos.sprite.Sprite(up_tiles[1])

            if sprite_obj_w:
                sprite_obj_w.position = (
                    self._pos_offset + (self._tile_size[0]*self._scale_me*j),
                    self._pos_offset + (self._tile_size[1]*self._scale_me*i)
                )
                sprite_obj_w.scale = self._scale_me

                if col == map_gen.WALL_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        sprite_obj_w.width//2,
                        sprite_obj_w.height//2
                    )
                    PLAYER_WALL_COLLISION_MANAGER.add(sprite_obj_w)
                elif col == map_gen.WALL_ERODE_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        sprite_obj_w.width//8,
                        sprite_obj_w.height//8
                    )
                    PLAYER_WALL_COLLISION_MANAGER.add(sprite_obj_w)

                elif col in (map_gen.WATER_TILE, map_gen.DEEP_WATER_TILE):
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        sprite_obj_w.width//2,
                        sprite_obj_w.height//2
                    )
                    PLAYER_WATER_COLLISION_MANAGER.add(sprite_obj_w)

                walls_nad_decoys_layer.add(sprite_obj_w)
                if col == map_gen.DOWN_TILE:
                    self.start_point = sprite_obj_w.position
            if sprite_obj_w2:
                sprite_obj_w2.position = (
                    self._pos_offset + (self._tile_size[0]*self._scale_me*j),
                    self._pos_offset + (self._tile_size[1]*self._scale_me*(i+1))
                )
                sprite_obj_w2.scale = self._scale_me
                upper_layer.add(sprite_obj_w2)

        self.add(walls_nad_decoys_layer, z=1)
        self.add(upper_layer, z=2)


class DungeonLayer(cocos.layer.ScrollingManager):
    def __init__(self, width, height, rooms):
        super().__init__()

        self.player = None
        self.floor_layer = FloorLayer(width, height, rooms)
        self.add(self.floor_layer)

        self.schedule(self.update)

    def update(self, dt):
        if self.player:
            self.set_focus(*self.player.position)

    def on_cocos_resize(self, usable_width, usable_height):
        if self.player:
            self.player.world_size = usable_width, usable_height
