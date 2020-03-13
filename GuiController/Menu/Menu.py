from tkinter import *


# An object that keeps track of a frame and all the components inside it
class Menu:

    # gui - the gui that this menu will exist in
    # window - the window that this menu will exist in
    def __init__(self, gui, window):
        self.gui = gui
        self.window = window
        self.frame = Frame()

    def placeInGui(self, window):
        self.frame = Frame(window)
        self.resetMenu()
        self.frame.pack()

    def resetMenu(self):
        self.frame.configure(background='#FFFFFF')
