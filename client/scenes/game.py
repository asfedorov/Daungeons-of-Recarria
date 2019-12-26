import random

import cocos

from utils import map_gen
from layers.map_layers import DungeonLayer
from layers.player import PlayerLayer


class GameScene(cocos.scene.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_width, screen_height = cocos.director.director.get_window_size()

        i = 0
        while True:
            if i > 10:
                break
            map_width = random.randint(12, 72)
            map_height = random.randint(12, 72)
            map_rooms = random.randint(1, (map_width * map_height)//100)
            map_excluded_rooms = 0
            if map_rooms > 3:
                map_excluded_rooms = random.randint(0, map_rooms - 2)
            try:
                dungeon_map = map_gen.Map(map_width, map_height, map_rooms, map_excluded_rooms)
                break
            except:
                i += 1
                continue

        dungeon_layer = DungeonLayer(
            dungeon_map,
            viewport=cocos.rect.Rect(0, 0, screen_width, screen_height)
        )
        player_layer = PlayerLayer(dungeon_layer._scale_me)
        dungeon_layer.add(player_layer, 10)
        player_layer.set_player(dungeon_layer.start_point)
        dungeon_layer.player = player_layer.player

        self.add(dungeon_layer)


def create_game_scene(screen_width, screen_height):
    return GameScene(screen_width, screen_height)
