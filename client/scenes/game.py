import cocos

from utils.map_gen import Map
from api.client import BaseAPIClient
from layers.player import PlayerLayer
from layers.map_layers import DungeonLayer


class GameScene(cocos.scene.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_width, screen_height = cocos.director.director.get_window_size()

        dungeon_map_dumped = BaseAPIClient.get_new_map()
        dungeon_map = Map(dungeon_map_dumped['map'])

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
