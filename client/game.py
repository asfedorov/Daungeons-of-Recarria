import cocos

# from scenes import game
from scenes import menus


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    width = 1240
    height = 720
    cocos.director.director.init(
        width=width,
        height=height,
        vsync=True,
        autoscale=True,
        # fullscreen=True,
        # resizable=True
    )
    cocos.director.director.show_FPS = True

    # main_scene = game.GameScene()
    main_scene = menus.MainMenuScene()

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)
