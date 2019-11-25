import copy
import pprint
import random

"""
 
■
○

⬚
▣
▩
▨
"""

UNDEFINED_TILE = '.'
WALL_TILE = '■'
OPEN_TILE = ' '
WATER_TILE = '○'

MAP_TILES = ''.join([
    WALL_TILE,
    OPEN_TILE,
    WATER_TILE,
    # CAVE_TILE,
])
TILES_WEIGHT = [30, 50, 10]


class NotEnoughMapSize(Exception):
    """Не возможно уместить заданное количество комнат в размер карты"""
    pass


def _generate_choice(tiles, weights=None):
    if not weights:
        return random.choice(tiles)
    return random.choices(tiles, weights)


class Map:
    _min_room_size = (5, 5)
    _max_attemps = 5
    _wall_additional_size = 2
    _max_evolve = 1
    _live_limit = 6
    _die_limit = 3

    def __init__(self, width, height, rooms=1):
        self._width = width
        self._height = height
        self._field = self._gen_blank(self._width, self._height)
        self._open_tiles = []
        self._rooms_count = rooms
        self._rooms = []

        self.shrink_rooms()

        for room in self._rooms:
            my_room = self._gen_room(room)
            for i, row in enumerate(my_room):
                for j, col in enumerate(row):
                    self._field[room[1][0]+i][room[0][0]+j] = col

        for i in range(self._max_evolve):
            self._evolve(WALL_TILE, OPEN_TILE)
            self.connect_rooms()
            self._evolve(OPEN_TILE, WALL_TILE)

        self.connect_rooms()

    def shrink_rooms(self):
        room = [
            [0, self._width],
            [0, self._height]
        ]
        self._rooms.append(room)

        attemps = 0
        while len(self._rooms) < self._rooms_count:
            if attemps > self._max_attemps:
                raise NotEnoughMapSize()

            shrink_room = random.choice(self._rooms)
            shrink_room_width = shrink_room[0][1] - shrink_room[0][0]
            shrink_room_height = shrink_room[1][1] - shrink_room[1][0]
            new_room = [[0, 0], [0, 0]]
            side = random.choice((True, False))
            # if shrink_room_width >= shrink_room_height:
            if side:
                old_w = shrink_room[0][1]
                new_w = old_w - ((shrink_room[0][1] - shrink_room[0][0]) // random.randrange(2, 4))

                if old_w - new_w < self._min_room_size[0] or new_w - shrink_room[0][0] < self._min_room_size[0]:
                    attemps += 1
                    continue

                shrink_room[0][1] = new_w
                new_room[0][0] = shrink_room[0][1]
                new_room[0][1] = old_w
                new_room[1][0] = shrink_room[1][0]
                new_room[1][1] = shrink_room[1][1]
            else:
                old_h = shrink_room[1][1]
                new_h = old_h - (shrink_room[1][1] - shrink_room[1][0]) // random.randrange(2, 4)

                if old_h - new_h < self._min_room_size[1] or new_h - shrink_room[1][0] < self._min_room_size[1]:
                    attemps += 1
                    continue

                shrink_room[1][1] = new_h
                new_room[1][0] = shrink_room[1][1]
                new_room[1][1] = old_h
                new_room[0][0] = shrink_room[0][0]
                new_room[0][1] = shrink_room[0][1]
            self._rooms.append(new_room)

    def connect_rooms(self):
        for i in range(0, len(self._rooms)):
            if i == len(self._rooms) - 1:
                break

            self._connect_rooms(self._rooms[i], self._rooms[i + 1])

    def _check_if_rooms_connected(self, room1, room2):
        start = None
        end = None

        for w in range(room1[0][0], room1[0][1]):
            for h in range(room1[1][0], room1[1][1]):
                if self._field[h][w] != WALL_TILE:
                    start = (h, w)
                    break

        for w in range(room2[0][0], room2[0][1]):
            for h in range(room2[1][0], room2[1][1]):
                if self._field[h][w] != WALL_TILE:
                    end = (h, w)
                    break

        temp_connected = [start]
        appended_new = True
        while True:
            if not appended_new:
                break
            appended_new = False
            for connected in temp_connected:
                neighbours = self._get_neighbours_coord(*connected)
                for n in neighbours:
                    if self._field[n[0]][n[1]] != WALL_TILE and n not in temp_connected:
                        temp_connected.append(n)
                        appended_new = True

        return end in temp_connected

    def _get_random_open_tile_from_room(self, room):
        open_tiles = []
        for w in range(room[0][0], room[0][1]):
                for h in range(room[1][0], room[1][1]):
                    if self._field[h][w] != WALL_TILE:
                        open_tiles.append((h, w))
        return random.choice(open_tiles)

    def _connect_rooms(self, room1, room2):
        if not self._check_if_rooms_connected(room1, room2):
            start = self._get_random_open_tile_from_room(room1)
            end = self._get_random_open_tile_from_room(room2)

            while start != end:
                if start[0] < end[0]:
                    start = (start[0] + 1, start[1])
                elif start[0] > end[0]:
                    start = (start[0] - 1, start[1])
                elif start[1] < end[1]:
                    start = (start[0], start[1] + 1)
                elif start[1] > end[1]:
                    start = (start[0], start[1] - 1)

                if self._field[start[0]][start[1]] == WALL_TILE:
                    self._field[start[0]][start[1]] = OPEN_TILE

    def _gen_room(self, room):
        w = room[0][1] - room[0][0]
        h = room[1][1] - room[1][0]
        my_room = self._gen_blank(w, h)
        my_room = self._fill_random(my_room)
        return my_room

    def _gen_blank(self, w, h):
        result = []

        result.append(w * [WALL_TILE])
        for i in range(h - 2):
            result.append([WALL_TILE] + (w - 2) * [UNDEFINED_TILE] + [WALL_TILE])
        result.append(w * [WALL_TILE])
        return result

    def _fill_random(self, room):
        for i in range(len(room)):
            row = room[i]
            for j in range(len(row)):
                col = row[j]
                if col == UNDEFINED_TILE:
                    _weights = copy.copy(TILES_WEIGHT)
                    if i < self._wall_additional_size or i > len(room) - self._wall_additional_size:
                        _weights[0] = _weights[0] + 30
                    if j < self._wall_additional_size or j > len(row) - self._wall_additional_size:
                        _weights[0] = _weights[0] + 30
                    room[i][j] = _generate_choice(MAP_TILES, _weights)[0]
        return room

    def _get_neighbours_coord(self, i_row, j_col):
        return [
            (i_row, j_col-1),
            (i_row-1, j_col-1),
            (i_row-1, j_col),
            (i_row-1, j_col+1),
            (i_row, j_col+1),
            (i_row+1, j_col+1),
            (i_row+1, j_col),
            (i_row+1, j_col-1),
        ]

    def _evolve(self, live_tile, dead_tile):
        field = copy.deepcopy(self._field)
        # result_field = copy.copy(self._field)
        for i, row in enumerate(self._field):
            for j, col in enumerate(row):
                if i in (0, len(self._field)-1) or j in (0, len(row)-1):
                    continue

                # if random.choice([True, True, False]):
                #     continue

                live_neigbours_count = 0
                dead_neigbours_count = 0
                for n_coord in self._get_neighbours_coord(i, j):
                    if self._field[n_coord[0]][n_coord[1]] == live_tile:
                        live_neigbours_count += 1
                    else:
                        dead_neigbours_count += 1

                if col == live_tile:
                    if live_neigbours_count < self._die_limit:
                        field[i][j] = dead_tile

                elif col != live_tile:
                    if live_neigbours_count > self._live_limit:
                        field[i][j] = live_tile

        self._field = field

    def __repr__(self):
        return "\n".join([
            " ".join(x)
            for x in self._field
        ])


def generate_map(width, height, rooms=5):
    my_map = Map(width, height, rooms)
    print(my_map)

generate_map(48, 24)
