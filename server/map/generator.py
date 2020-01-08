import copy
import random

from .constants import *

MAP_TILES = ''.join([
    WALL_TILE,
    OPEN_TILE,
    WATER_TILE,
])
TILES_WEIGHT = [30, 50, 10]

NOT_PASSABLE = (WALL_TILE, CAVE_TILE, WALL_ERODE_TILE)


class NotEnoughMapSize(Exception):
    """Не возможно уместить заданное количество комнат в размер карты
    """
    pass


def _generate_choice(tiles, weights=None, length=1):
    """
    Генератор псеводслучайного выбора из списка.

    Args:
        tiles (iterable): список тайлов для выбора
        weights (iterable|None): список в весами  вероятности выбора. Должен быть той же длины, что и список тайлов

    Returns:
        список
    """
    if not weights:
        return [random.choice(tiles)]
    return random.choices(tiles, weights, k=length)


class Map:
    """
    Класс карты, с генерацией и всем прочим
    """
    _min_room_size = (5, 5)
    _max_attemps = 5
    _wall_additional_size = 4
    _max_evolve = 1
    _max_erode = 3
    _live_limit = 6
    _die_limit = 3
    _erode_wall_limit = 4
    _erode_wall_chance = 3
    _erode_open_limit = 8
    _erode_open_chance = 3
    _erode_crack_limit = 4
    _erode_crack_chance = 3
    _erode_water_limit = 3
    _erode_water_chance = 3

    def __init__(self, width, height, rooms=1, excluded_rooms=0):
        """
        Инициализация карты

        Args:
            width (int): ширина
            height (int): высота
            rooms (int, optional): количество комнат
        """
        self._width = width
        self._height = height
        self._field = self._gen_blank(self._width, self._height)
        self._open_tiles = []
        self._rooms_count = rooms
        self._rooms = []
        self._excluded_rooms = excluded_rooms

        # делим карту на комнаты, потом генерируем эти комнаты
        self.shrink_rooms()

        self.exclude_rooms()

        self.generate_rooms()

        # делаем комнаты чуть крсивее, сглаживаем углы
        self.evolve()
        # соединяем комнаты, чтобы карты была полностью проходима
        self.connect_rooms()
        # доп красивости
        self.erode()
        # карта могла стать непроходимой, перепроверим
        self.connect_rooms()

        # расставляем вход и выход с карты
        self.set_entrances()

        self._cleanup_walls()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def erode(self):
        """Summary
        """
        for i in range(self._max_erode):
            self._erode()
            self.connect_rooms()

    def _erode(self):
        for i, j, col in self._iter_tiles_from_field(exclude_borders=True):
            neighbours = self._get_neighbours_coord(i, j)
            neighbours_walls = 0
            neighbours_open = 0
            neighbours_water = 0
            neighbours_crack = 0
            neighbours_cave = 0
            neighbours_wall_erode = 0

            for n in neighbours:
                neighbour_tile = self._field[n[0]][n[1]]
                if neighbour_tile == WALL_TILE:
                    neighbours_walls += 1
                elif neighbour_tile == OPEN_TILE:
                    neighbours_open += 1
                elif neighbour_tile == WATER_TILE:
                    neighbours_water += 1
                elif neighbour_tile == CRACK_TILE:
                    neighbours_crack += 1
                elif neighbour_tile == CAVE_TILE:
                    neighbours_cave += 1
                elif neighbour_tile == WALL_ERODE_TILE:
                    neighbours_wall_erode += 1

            if col == WALL_TILE:
                if neighbours_walls <= self._erode_wall_limit:
                    if random.randrange(10) < self._erode_wall_chance:
                        self._field[i][j] = WALL_ERODE_TILE

            if col == OPEN_TILE:
                if neighbours_open + neighbours_crack + neighbours_cave >= self._erode_open_limit:
                    if random.randrange(10) < self._erode_open_chance:
                        self._field[i][j] = CRACK_TILE

            if col == CRACK_TILE:
                if neighbours_crack >= self._erode_crack_limit:
                    if random.randrange(10) < self._erode_crack_chance:
                        self._field[i][j] = CAVE_TILE

            if col == WATER_TILE:
                if neighbours_water >= self._erode_water_limit:
                    if random.randrange(10) < self._erode_water_chance:
                        self._field[i][j] = DEEP_WATER_TILE

            if col == WALL_ERODE_TILE:
                if neighbours_walls == 0:
                    self._field[i][j] = OPEN_TILE

    def set_entrances(self):
        """Summary
        """
        up_room = random.choice(self._rooms)
        down_room = random.choice(self._rooms)

        up_coord = self._get_random_open_tile_from_room(up_room, is_near_wall=True)
        self._field[up_coord[0]][up_coord[1]] = UP_TILE

        down_coord = self._get_random_open_tile_from_room(down_room, is_near_wall=False)
        self._field[down_coord[0]][down_coord[1]] = DOWN_TILE

    def evolve(self):
        """Summary
        """
        for i in range(self._max_evolve):
            self._evolve(WALL_TILE, OPEN_TILE)
            self.connect_rooms()
            self._evolve(OPEN_TILE, WALL_TILE)

    def generate_rooms(self):
        """Summary
        """
        for room in self._rooms:
            my_room = self._gen_room(room)
            for i, j, col in self._iter_tiles_from_field(field=my_room):
                self._field[room[1][0]+i][room[0][0]+j] = col

    def exclude_rooms(self):
        rooms_to_exclude = []
        while len(rooms_to_exclude) != self._excluded_rooms:
            room = random.choice(self._rooms[1:])
            if room not in rooms_to_exclude:
                rooms_to_exclude.append(room)

        tiles = _generate_choice(
            [WALL_TILE, CAVE_TILE],
            weights=[10, 7],
            length=self._excluded_rooms
        )
        for i, room in enumerate(rooms_to_exclude):
            my_room = self._gen_with_tile(room, tiles[i])
            for i, j, col in self._iter_tiles_from_field(field=my_room):
                self._field[room[1][0]+i][room[0][0]+j] = col
            self._rooms.remove(room)

    def shrink_rooms(self, shrink_random_side=False):
        """Summary
        
        Args:
            shrink_random_side (bool, optional): Description
        
        Raises:
            NotEnoughMapSize: Description
        """
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

            if shrink_random_side:
                side = random.choice((True, False))
            else:
                side = shrink_room_width >= shrink_room_height

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
        """Summary
        """
        for i in range(0, len(self._rooms)):
            if i == len(self._rooms) - 1:
                break

            self._connect_rooms(self._rooms[i], self._rooms[i + 1])

    def tiles(self):
        return self._iter_tiles_from_field()

    def _iter_tiles_from_field(self, tiles_range=None, field=None, exclude_borders=False):
        """Summary

        Args:
            tiles_range (None, optional): Description
            field (None, optional): Description
            exclude_borders (bool, optional): Description

        Yields:
            TYPE: Description
        """
        if not field:
            field = self._field
        if not tiles_range:
            tiles_range = (
                (0, len(field[0])),
                (0, len(field))
            )

        for w in range(tiles_range[0][0], tiles_range[0][1]):
            for h in range(tiles_range[1][0], tiles_range[1][1]):
                if exclude_borders and (
                    h in (0, len(field)-1) or
                    w in (0, len(field[0])-1)
                ):
                    continue
                yield h, w, field[h][w]

    def _check_if_rooms_connected(self, room1, room2):
        """Summary
        
        Args:
            room1 (TYPE): Description
            room2 (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        start = None
        end = None

        for h, w, col in self._iter_tiles_from_field(tiles_range=room1):
            if col != WALL_TILE:
                start = (h, w)
                break

        for h, w, col in self._iter_tiles_from_field(tiles_range=room2):
            if col != WALL_TILE:
                end = (h, w)
                break

        temp_connected = [start]
        appended_new = True
        while True:
            if not appended_new:
                break
            appended_new = False
            for connected in temp_connected:
                neighbours = self._get_neighbours_coord(*connected, diag=False)
                for n in neighbours:
                    if self._field[n[0]][n[1]] not in NOT_PASSABLE and n not in temp_connected:
                        temp_connected.append(n)
                        appended_new = True

        return end in temp_connected

    def _get_random_open_tile_from_room(self, room, is_near_wall=None):
        """Summary
        
        Args:
            room (TYPE): Description
            is_near_wall (None, optional): Description
        
        Returns:
            TYPE: Description
        """
        open_tiles = []
        for h, w, col in self._iter_tiles_from_field(tiles_range=room):
            if col != WALL_TILE:
                if is_near_wall is None:
                    open_tiles.append((h, w))
                else:
                    wall_is_neighbour = False
                    for n in self._get_neighbours_coord(h, w):
                        if self._field[n[0]][n[1]] == WALL_TILE:
                            wall_is_neighbour = True
                            break
                    if (is_near_wall and wall_is_neighbour) or (not is_near_wall and not wall_is_neighbour):
                        open_tiles.append((h, w))

        return random.choice(open_tiles)

    def _connect_rooms(self, room1, room2):
        """Summary
        
        Args:
            room1 (TYPE): Description
            room2 (TYPE): Description
        """
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

                elif self._field[start[0]][start[1]] == UNDEFINED_TILE:
                    for n in self._get_neighbours_coord(start[0], start[1]):
                        if self._field[n[0]][n[1]] == UNDEFINED_TILE:
                            self._field[n[0]][n[1]] = WALL_TILE
                    self._field[start[0]][start[1]] = OPEN_TILE

                elif self._field[start[0]][start[1]] == CAVE_TILE:
                    self._field[start[0]][start[1]] = OPEN_TILE

    def _gen_room(self, room):
        """Summary
        
        Args:
            room (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        w = room[0][1] - room[0][0]
        h = room[1][1] - room[1][0]
        my_room = self._gen_blank(w, h)
        my_room = self._fill_random(my_room)
        return my_room

    def _gen_blank(self, w, h):
        """Summary
        
        Args:
            w (TYPE): Description
            h (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        result = []

        result.append(w * [WALL_TILE])
        for i in range(h - 2):
            result.append([WALL_TILE] + (w - 2) * [UNDEFINED_TILE] + [WALL_TILE])
        result.append(w * [WALL_TILE])
        return result

    def _fill_random(self, room):
        """Summary
        
        Args:
            room (TYPE): Description
        
        Returns:
            TYPE: Description
        """
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

    def _gen_with_tile(self, room, tile):
        result = []
        w = room[0][1] - room[0][0]
        h = room[1][1] - room[1][0]
        for i in range(h):
            result.append(w * [tile])
        return result

    def _get_neighbours_coord(self, i_row, j_col, diag=True):
        """Summary
        
        Args:
            i_row (TYPE): Description
            j_col (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if diag:
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

        return [
            (i_row, j_col-1),
            (i_row-1, j_col),
            (i_row, j_col+1),
            (i_row+1, j_col),
        ]

    def _evolve(self, live_tile, dead_tile):
        """Summary
        
        Args:
            live_tile (TYPE): Description
            dead_tile (TYPE): Description
        """
        field = copy.deepcopy(self._field)
        for i, j, col in self._iter_tiles_from_field(exclude_borders=True):
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
        """Summary

        Returns:
            TYPE: Description
        """
        return "\n".join([
            " ".join(x)
            for x in self._field
        ])

    def dump_to_string(self, delimeter=';'):
        """Summary

        Returns:
            TYPE: Description
        """
        return delimeter.join([
            "".join(x)
            for x in self._field
        ])

    def return_inverse(self):
        return self._field

    def _cleanup_walls(self):
        field = copy.deepcopy(self._field)
        for i, j, col in self._iter_tiles_from_field():
            unreachable = True
            for n_coord in self._get_neighbours_coord(i, j):
                try:
                    if self._field[n_coord[0]][n_coord[1]] != WALL_TILE:
                        unreachable = False
                except:
                    pass

            if unreachable:
                field[i][j] = UNDEFINED_TILE

        self._field = field


if __name__ == '__main__':

    def generate_map(width, height, rooms=5, excluded_rooms=0):
        """Summary

<<<<<<< Updated upstream
        Args:
            width (TYPE): Description
            height (TYPE): Description
            rooms (int, optional): Description
        """
        my_map = Map(width, height, rooms, excluded_rooms)
        # return my_map.return_inverse()
        print(my_map)

    generate_map(48, 32, rooms=7, excluded_rooms=3)

    # i = 0
    # while True:
    #     if i > 10:
    #         break
    #     map_width = random.randint(12, 72)
    #     map_height = random.randint(12, 72)
    #     map_rooms = random.randint(1, (map_width * map_height)//100)
    #     map_excluded_rooms = 0
    #     if map_rooms > 3:
    #         map_excluded_rooms = random.randint(0, map_rooms - 2)
    #     try:
    #         generate_map(map_width, map_height, rooms=map_rooms, excluded_rooms=map_excluded_rooms)
    #         break
    #     except:
    #         i += 1
    #         continue
