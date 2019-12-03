import cocos

from map_layers import DungeonLayer
from player import PlayerLayer

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    width = 800
    height = 600
    cocos.director.director.init(
        width=width,
        height=height,
        vsync=True,
        autoscale=True,
        # resizable=True
    )
    cocos.director.director.show_FPS = True

    dungeon_layer = DungeonLayer(
        74,
        32,
        13,
        viewport=cocos.rect.Rect(0, 0, 800, 600)
    )
    player_layer = PlayerLayer(dungeon_layer.floor_layer.start_point)
    player_layer.player.world_size = width, height

    dungeon_layer.add(player_layer, 10)
    dungeon_layer.player = player_layer.player


    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(dungeon_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)
