import random

import pyglet
pyglet.options['vsync'] = False

import cocos

import map_gen
import sprites_loader

class HelloWorld(cocos.layer.Layer):

    def __init__(self):
        super().__init__()

        floor_tiles = sprites_loader.get_floor_tiles()
        wall_tiles = sprites_loader.get_wall_tiles()
        crack_tiles = sprites_loader.get_cracked_tiles()
        cave_tiles = sprites_loader.get_cave_tiles()

        map_field = map_gen.Map(32, 24, 5)
        for i, j, col in map_field._iter_tiles_from_field():
            sprite_obj = None
            if col == map_gen.CRACK_TILE:
                sprite_obj = cocos.sprite.Sprite(random.choice(crack_tiles))
            elif col == map_gen.CAVE_TILE:
                sprite_obj = cocos.sprite.Sprite(random.choice(cave_tiles)) 
            else:
                sprite_obj = cocos.sprite.Sprite(random.choice(floor_tiles))

            sprite_obj.position = 8 + (16*j), 8 + (16*i)
            self.add(sprite_obj, 0)


            if col == map_gen.WALL_TILE:
                sprite_obj = cocos.sprite.Sprite(random.choice(wall_tiles))
                sprite_obj.position = 8 + (16*j), 8 + (16*i)
                self.add(sprite_obj, 1)
            # else:
             # col == map_gen.OPEN_TILE:

            # if sprite_obj:



if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(vsync=False)

    # We create a new layer, an instance of HelloWorld
    hello_layer = HelloWorld()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(hello_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)
