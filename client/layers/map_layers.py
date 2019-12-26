import random
from collections import deque

import cocos
import cocos.collision_model as cm

from utils import map_gen
from utils import sprites_loader
from utils.utils import Vector2
from .layers import MyRectCell
from .layers import MyRectMapLayer


class DungeonLayer(cocos.layer.ScrollingManager):
    _tile_size = Vector2(16, 16)
    _scale_me = 1.7
    _pos_offset = 8 * _scale_me

    def __init__(self, dungeon_map, viewport=None):
        self.PLAYER_WALL_COLLISION_MANAGER = cm.CollisionManagerGrid(
            0,
            dungeon_map.width * self._tile_size.x * self._scale_me,
            0,
            dungeon_map.height * self._tile_size.y * self._scale_me,
            self._tile_size.x * self._scale_me,
            self._tile_size.y * self._scale_me
        )
        self.PLAYER_WATER_COLLISION_MANAGER = cm.CollisionManagerGrid(
            0,
            dungeon_map.width * self._tile_size.x * self._scale_me,
            0,
            dungeon_map.height * self._tile_size.y * self._scale_me,
            self._tile_size.x * self._scale_me,
            self._tile_size.y * self._scale_me
        )
        self.PLAYER_CAVE_COLLISION_MANAGER = cm.CollisionManagerGrid(
            0,
            dungeon_map.width * self._tile_size.x * self._scale_me,
            0,
            dungeon_map.height * self._tile_size.y * self._scale_me,
            self._tile_size.x * self._scale_me,
            self._tile_size.y * self._scale_me
        )

        super().__init__(
            viewport=viewport
        )

        self.player = None
        self.start_point = None
        self.seen = deque([], maxlen=512)
        self.longseen = deque([], maxlen=1024)
        self.current_watched = []

        self._collision_layer = cocos.layer.ScrollableLayer()
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

        for i, j, col in dungeon_map.tiles():
            if j not in cells_dict_lvl0:
                cells_dict_lvl0[j] = []
                cells_dict_lvl1[j] = []
                cells_dict_lvl2[j] = []

            image_obj = random.choice(floor_tiles)
            # image_obj1 = blank_tile
            image_obj1 = None
            image_obj2 = None

            sprite_obj_w = None

            view_block = None

            if col == map_gen.CRACK_TILE:
                image_obj = random.choice(crack_tiles)
            elif col == map_gen.CAVE_TILE:
                image_obj = random.choice(cave_tiles)
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
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
                    self._pos_offset + (self._tile_size.x * self._scale_me * j),
                    self._pos_offset + (self._tile_size.y * self._scale_me * i)
                )

            elif col == map_gen.UP_TILE:
                image_obj2 = up_tiles[0]
            elif col == map_gen.WALL_TILE:
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
                view_block = 'full'
                image_obj1 = random.choice(wall_tiles)
            elif col == map_gen.WALL_ERODE_TILE:
                view_block = 'half'
                sprite_obj_w = cocos.sprite.Sprite(blank_tile.get_texture())
                image_obj1 = random.choice(wall_erode_tiles)
            elif col == map_gen.UNDEFINED_TILE:
                image_obj = None

            if image_obj:
                tile0 = cocos.tiles.Tile(
                    't1.{}{}'.format(j, i),
                    {},
                    image_obj,
                )
            else:
                tile0 = None
            cell0 = MyRectCell(
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
            cell1 = MyRectCell(
                j,
                i,
                16,
                16,
                {},
                tile1,
                view_block=view_block
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
            cell2 = MyRectCell(
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
                    self._pos_offset + (self._tile_size.x * self._scale_me * j),
                    self._pos_offset + (self._tile_size.y * self._scale_me * i)
                )
                self._collision_layer.add(sprite_obj_w)
                if col == map_gen.WALL_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        8 * self._scale_me,
                        8 * self._scale_me
                    )
                    self.PLAYER_WALL_COLLISION_MANAGER.add(sprite_obj_w)
                elif col == map_gen.WALL_ERODE_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        2 * self._scale_me,
                        2 * self._scale_me
                    )
                    self.PLAYER_WALL_COLLISION_MANAGER.add(sprite_obj_w)
                elif col in (map_gen.WATER_TILE, map_gen.DEEP_WATER_TILE):
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        8 * self._scale_me,
                        8 * self._scale_me
                    )
                    self.PLAYER_WATER_COLLISION_MANAGER.add(sprite_obj_w)
                elif col == map_gen.CAVE_TILE:
                    sprite_obj_w.cshape = cm.AARectShape(
                        sprite_obj_w.position,
                        8 * self._scale_me,
                        8 * self._scale_me
                    )
                    self.PLAYER_CAVE_COLLISION_MANAGER.add(sprite_obj_w)

        properties = {
            'width': dungeon_map.width,
            'height': dungeon_map.height,
            'px_width': dungeon_map.width * self._tile_size.x * self._scale_me,
            'px_heigth': dungeon_map.height * self._tile_size.y * self._scale_me,
            'tw': 16 * self._scale_me,
            'th': 16 * self._scale_me
        }

        self.floor_layer = MyRectMapLayer(
            0,
            16,
            16,
            list(cells_dict_lvl0.values()),
            properties=properties,
            scale_me=self._scale_me
        )

        self.walls_layer = MyRectMapLayer(
            1,
            16,
            16,
            list(cells_dict_lvl1.values()),
            properties=properties,
            scale_me=self._scale_me
        )
        self.upper_layer = MyRectMapLayer(
            2,
            16,
            16,
            list(cells_dict_lvl2.values()),
            properties=properties,
            scale_me=self._scale_me
        )
        for i, j in cell_water:
            self.upper_layer.set_cell_sprite_opacity(i, j, 10)
        for i, j in cell_deep_water:
            self.upper_layer.set_cell_sprite_opacity(i, j, 200)

        px_width = dungeon_map.width * self._tile_size.x * self._scale_me
        px_height = dungeon_map.height * self._tile_size.y * self._scale_me

        self.floor_layer.px_width = px_width
        self.floor_layer.px_height = px_height
        self.walls_layer.px_width = px_width
        self.walls_layer.px_height = px_height
        self.upper_layer.px_width = px_width
        self.upper_layer.px_height = px_height

        self.floor_layer.scale = self._scale_me
        self.walls_layer.scale = self._scale_me
        self.upper_layer.scale = self._scale_me

        self.add(self.floor_layer, z=1)
        self.add(self.walls_layer, z=3)
        self.add(self.upper_layer, z=5)
        self.add(self._collision_layer)

        self.schedule(self.update)

    def update(self, dt):
        if self.player:
            self.set_focus(*self.player.position)

    def get_watching_tiles(self, i, j, watch_range=8):
        start_tile = self.floor_layer.get_key_at_pixel(i, j)
        # print(start_tile)

        watch_hex = {start_tile}

        directions = {
            'left': (-1, 0),
            'up': (0, 1),
            'right': (1, 0),
            'down': (0, -1)
        }

        directions_offset = {
            'left': {
                'left': (-1, -1),
                'right': (-1, 1),
            },
            'up': {
                'left': (-1, 1),
                'right': (1, 1),
            },
            'right': {
                'left': (1, 1),
                'right': (1, -1),
            },
            'down': {
                'left': (-1, -1),
                'right': (1, -1),
            },
        }

        direction_sides = {
            'left': {
                'left': 'down',
                'right': 'up',
                'backward': 'right',
            },
            'up': {
                'left': 'left',
                'right': 'right',
                'backward': 'down',
            },
            'right': {
                'left': 'up',
                'right': 'down',
                'backward': 'left',
            },
            'down': {
                'left': 'left',
                'right': 'right',
                'backward': 'up',
            },
        }

        for direction, offset in directions.items():
            left_go = []
            center_go = [start_tile]
            right_go = []

            if self.player.parent.face == direction:
                _watch_range = watch_range
            elif direction == direction_sides[self.player.parent.face]['backward']:
                _watch_range = 2
            else:
                _watch_range = 3

            _blocked = []
            for r in range(0, _watch_range):
                _left_go = []
                _center_go = []
                _right_go = []

                # if r == 0:
                #     left_go.append(
                #         (
                #             start_tile[0] + directions_offset[direction]['left'][0],
                #             start_tile[1] + directions_offset[direction]['left'][1]
                #         )
                #     )
                #     center_go.append(
                #         (
                #             start_tile[0] + offset[0],
                #             start_tile[1] + offset[1]
                #         )
                #     )
                #     right_go.append(
                #         (
                #             start_tile[0] + directions_offset[direction]['right'][0],
                #             start_tile[1] + directions_offset[direction]['right'][1]
                #         )
                #     )

                for go in ('left', 'center', 'right'):
                    if go == 'left':
                        go_direction = left_go
                    elif go == 'right':
                        go_direction = right_go
                    elif go == 'center':
                        go_direction = center_go
                    for cell_pos in set(go_direction):
                        _to_block = False
                        _to_shade = False

                        cell = self.walls_layer.get_cell(*cell_pos)

                        if cell and cell.tile is not None and r > 0:
                            if cell.view_block == 'full':
                                _to_block = True
                            elif cell.view_block == 'half':
                                _to_shade = True

                        x_distance = (
                            cell_pos[0] - start_tile[0]
                            if cell_pos[0] >= start_tile[0]
                            else start_tile[0] - cell_pos[0]
                        )
                        y_distance = (
                            cell_pos[1] - start_tile[1]
                            if cell_pos[1] >= start_tile[1]
                            else start_tile[1] - cell_pos[1]
                        )
                        if x_distance + y_distance > _watch_range + 1:
                            continue

                        if cell_pos in _blocked:
                            _to_block = True
                        else:
                            watch_hex.add(cell_pos)
                        if go == 'center':
                            to_append = [
                                (
                                    cell_pos[0] + offset[0],
                                    cell_pos[1] + offset[1]
                                )
                            ]
                            left_append = []
                            right_append = []
                            if r % 2 == 0:
                                left_append = [
                                    (
                                        cell_pos[0] + directions_offset[direction]['left'][0],
                                        cell_pos[1] + directions_offset[direction]['left'][1]
                                    )
                                ]
                                right_append = [
                                    (
                                        cell_pos[0] + directions_offset[direction]['right'][0],
                                        cell_pos[1] + directions_offset[direction]['right'][1]
                                    )
                                ]
                            if _to_block:
                                _blocked.extend(to_append)
                                _blocked.extend(left_append)
                                _blocked.extend(right_append)
                            elif _to_shade:
                                self.seen.extend(to_append)
                                self.seen.extend(left_append)
                                self.seen.extend(right_append)
                            # else:
                            _center_go.extend(to_append)
                            _left_go.extend(left_append)
                            _right_go.extend(right_append)
                        elif (
                            go == 'left' and
                            direction_sides[direction]['left'] != direction_sides[self.player.parent.face]['backward']
                        ):
                            to_append = [
                                (
                                    cell_pos[0] + directions_offset[direction]['left'][0],
                                    cell_pos[1] + directions_offset[direction]['left'][1]
                                ),
                                (
                                    cell_pos[0] + offset[0],
                                    cell_pos[1] + offset[1]
                                )

                            ]
                            if _to_block:
                                _blocked.extend(to_append)
                            elif _to_shade:
                                self.seen.extend(to_append)
                            # else:
                            _left_go.extend(to_append)
                        elif (
                            go == 'right' and
                            direction_sides[direction]['right'] != direction_sides[self.player.parent.face]['backward']
                        ):
                            to_append = [
                                (
                                    cell_pos[0] + offset[0],
                                    cell_pos[1] + offset[1]
                                ),
                                (
                                    cell_pos[0] + directions_offset[direction]['right'][0],
                                    cell_pos[1] + directions_offset[direction]['right'][1]
                                )
                            ]
                            if _to_block:
                                _blocked.extend(to_append)
                            elif _to_shade:
                                self.seen.extend(to_append)
                            # else:
                            _right_go.extend(to_append)
                        go_direction.remove(cell_pos)
                        # for cp in _blocked:
                        #     if cp in go_direction:
                        #         go_direction.remove(cp)

                center_go = _center_go
                left_go = _left_go
                right_go = _right_go

        if watch_hex != self.current_watched:
            self.current_watched = watch_hex
            self.seen.extend(watch_hex)
            self.longseen.extend(watch_hex)
        return watch_hex
