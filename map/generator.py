import copy
import pprint
import random

"""

⬚
▣
▩

"""

UNDEFINED_TILE = '.'
WALL_TILE = '▣'
OPEN_TILE = '⬚'
WATER_TILE = '▨'
# CAVE_TILE = '◻'

MAP_TILES = ''.join([
    WALL_TILE,
    OPEN_TILE,
    WATER_TILE,
    # CAVE_TILE,
])
TILES_WEIGHT = [30, 50, 10]


def _generate_choice(tiles, weights=None):
    if not weights:
        return random.choice(tiles)
    return random.choices(tiles, weights)


class Map:
    _min_room_size = (5, 5)

    def __init__(self, width, height, rooms=1):
        self._width = width
        self._height = height
        self._field = self._gen_blank(self._width, self._height)

        self._rooms = []

        room = [
            [0, self._width],
            [0, self._height]
        ]
        self._rooms.append(room)

        while len(self._rooms) < rooms:
            shrink_room = random.choice(self._rooms)
            shrink_room_width = shrink_room[0][1] - shrink_room[0][0]
            shrink_room_height = shrink_room[1][1] - shrink_room[1][0]
            new_room = [[0, 0], [0, 0]]
            if shrink_room_width >= shrink_room_height:
                old_w = shrink_room[0][1]
                shrink_room[0][1] = old_w // 2
                new_room[0][0] = shrink_room[0][1]
                new_room[0][1] = old_w
                new_room[1][0] = shrink_room[1][0]
                new_room[1][1] = shrink_room[1][1]
            else:
                old_h = shrink_room[1][1]
                shrink_room[1][1] = old_h // 2
                new_room[1][0] = shrink_room[1][1]
                new_room[1][1] = old_h
                new_room[0][0] = shrink_room[0][0]
                new_room[0][1] = shrink_room[0][1]
            self._rooms.append(new_room)

        for room in self._rooms:
            my_room = self._gen_room(room)
            for i, row in enumerate(my_room):
                for j, col in enumerate(row):
                    self._field[room[1][0]+i][room[0][0]+j] = col

        # self._gen_blank(self._w)
        # self._fill_random()

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
                    if i < 3 or i > len(room) - 3:
                        _weights[0] = _weights[0] + 30
                    if j < 3 or j > len(row) - 3:
                        _weights[0] = _weights[0] + 30
                    room[i][j] = _generate_choice(MAP_TILES, _weights)[0]
        return room

    def __repr__(self):
        return "\n".join([
            "".join(x)
            for x in self._field
        ])


def generate_map(width, height, rooms=5):
    my_map = Map(width, height, rooms)
    print(my_map)
    # pprint.pprint(my_map._rooms)

generate_map(32, 32)
