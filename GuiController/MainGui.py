from GuiController.Menu import InitMenu
from GuiController import Gui


class MainGui(Gui.Gui):

    def __init__(self, window, centralHandeler):
        super().__init__(window)

        self.window.title("Tetris Evolution Sim")

        initMenu = InitMenu.InitMenu(self, self.window, centralHandeler)
        self.setMenu(initMenu)
