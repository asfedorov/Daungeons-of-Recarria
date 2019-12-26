import cocos

from layers import menus


class MainMenuScene(cocos.scene.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        menu_layer = menus.MainMenu()

        self.add(menu_layer)


class InGameMenuScene(cocos.scene.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        menu_layer = menus.InGameMenu()

        self.add(menu_layer)
