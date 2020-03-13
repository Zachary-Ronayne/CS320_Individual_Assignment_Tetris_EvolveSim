from tkinter import *


# An object that keeps track of a tkinter window and can keep track of one menu object that is inside it
class Gui:
    def __init__(self, window):
        self.window = window
        self.currentMenu = Menu()

    def setMenu(self, menu):
        menu.placeInGui(self.window)
        self.currentMenu = menu
