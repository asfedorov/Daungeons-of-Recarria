from api.client import BaseAPIClient

_tiles_mapping = BaseAPIClient.get_tile_mapping()['tile_mapping']

UNDEFINED_TILE = _tiles_mapping['UNDEFINED_TILE']
WALL_TILE = _tiles_mapping['WALL_TILE']
OPEN_TILE = _tiles_mapping['OPEN_TILE']
WATER_TILE = _tiles_mapping['WATER_TILE']
DEEP_WATER_TILE = _tiles_mapping['DEEP_WATER_TILE']
WALL_ERODE_TILE = _tiles_mapping['WALL_ERODE_TILE']
CRACK_TILE = _tiles_mapping['CRACK_TILE']
CAVE_TILE = _tiles_mapping['CAVE_TILE']

UP_TILE = _tiles_mapping['UP_TILE']
DOWN_TILE = _tiles_mapping['DOWN_TILE']


class Map:
    def __init__(self, map_dumped, delimeter=';'):
        map_array = map_dumped.split(';')
        self._width = len(map_array[0])
        self._height = len(map_array)
        self._field = map_array

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

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

    def __repr__(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return "\n".join([
            " ".join(x)
            for x in self._field
        ])

    def return_inverse(self):
        return self._field
