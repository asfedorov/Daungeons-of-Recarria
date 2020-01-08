import random

from aiohttp import web
from utils import json_rpc2_web_response

from .generator import Map
from .constants import TILE_MAPPING


@json_rpc2_web_response
async def map_index(request):
    data = await request.json()

    params = data.get('params', {})
    func_name = data.get('method')
    func = _method_to_func_mapping.get(func_name)
    if not func:
        return {"error": "No such method: {!r}".format(func_name)}
    return await func(**params)


async def generate_map(*args, **kwargs):
    i = 0
    dungeon_map = None
    while True:
        if i > 10:
            break
        map_width = kwargs.get('width') or random.randint(12, 72)
        map_height = kwargs.get('height') or random.randint(12, 72)
        map_rooms = kwargs.get('rooms') or random.randint(1, (map_width * map_height)//100)

        map_excluded_rooms = kwargs.get('excluded_rooms')
        if not map_excluded_rooms:
            map_excluded_rooms = 0
            if map_rooms > 3:
                map_excluded_rooms = random.randint(0, map_rooms - 2)
        try:
            dungeon_map = Map(map_width, map_height, map_rooms, map_excluded_rooms)
            break
        except:
            i += 1
            continue
    if not dungeon_map:
        return {"error": "Can not create map with params: {!r}".format(kwargs)}

    return {'map': dungeon_map.dump_to_string()}


async def get_tile_mapping():
    return {'tile_mapping': TILE_MAPPING}


_method_to_func_mapping = {
    'generate': generate_map,
    'get_tile_mapping': get_tile_mapping,
}
