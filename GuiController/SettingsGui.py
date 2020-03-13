from GuiController import Gui
from GuiController.Menu import SettingsMenu


class SettingsGui(Gui.Gui):

    def __init__(self, centralHandler, settingsGui):
        super().__init__(settingsGui)

        self.window.title("Settings")

        self.setMenu(SettingsMenu.SettingsMenu(centralHandler, settingsGui))
