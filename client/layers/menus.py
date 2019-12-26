import cocos
import cocos.actions as ac
from cocos.menu import Menu, MenuItem, zoom_in, zoom_out

from scenes import game


class MainMenu(Menu):
    def __init__(self):
        super().__init__()

        l = []
        l.append(
            MenuItem('New Game', self.on_new_game)
        )
        l.append(
            MenuItem('Options', self.on_options)
        )
        l.append(
            MenuItem('Quit', self.on_quit)
        )
        self.create_menu(
            l,
            ac.ScaleTo(1.2, duration=0.2),
            zoom_out()
        )

    def on_new_game(self):
        game_scene = game.GameScene()
        cocos.director.director.replace(game_scene)
        cocos.director.director.push(game_scene)

    def on_options(self):
        return

    def on_quit(self):
        cocos.director.director.pop()


class InGameMenu(Menu):
    def __init__(self):
        super().__init__()

        l = []
        l.append(
            MenuItem('Continue', self.on_continue)
        )
        # l.append(
        #     MenuItem('Quit', self.on_quit)
        # )
        self.create_menu(
            l,
            zoom_in(),
            zoom_out()
        )

    def on_continue(self):
        cocos.director.director.pop()

    # def on_quit(self):
    #     from scenes import menus
    #     cocos.director.director.replace(menus.MainMenuScene())
