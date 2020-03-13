from tkinter import *

from GuiController.Menu import Menu
from GuiController.Menu import SimMenu

from threading import Thread

from os import listdir
from os.path import isfile, join


# The menu used for the first screen when the program is started up
class InitMenu(Menu.Menu):

    def __init__(self, gui, window, centralHandeler):
        super().__init__(gui, window)
        self.centralHandeler = centralHandeler
        self.startButton = None
        self.loadButton = None

        self.savesDropDown = None
        self.reloadSavesButton = None
        self.savesLabel = None
        self.selectedSave = None

        self.state = 0

    def resetMenu(self):
        super().resetMenu()

        self.frame.configure(padx=100, pady=100)

        # button to create a new simulation
        self.startButton = Button(self.frame, text="Create New Sim", command=self.handleStartButtonPress)
        self.startButton.configure(font=('Impact', 40))
        self.startButton.grid(row=0, column=0)

        # button to load a new simulation
        self.loadButton = Button(self.frame, text="Load Sim", command=self.handleLoadButtonPress)
        self.loadButton.configure(font=('Impact', 40))
        self.loadButton.grid(row=1, column=0)

        # button to refresh saves list
        self.reloadSavesButton = Button(self.frame, text="Reload Saves list", command=self.handleReloadSavesButtonPress)
        self.reloadSavesButton.configure(font=('Impact', 20))
        self.reloadSavesButton.grid(row=2, column=0, pady=20)

        # drop down list of the save files
        self.setUpSavesList()

    def handleReloadSavesButtonPress(self):
        self.setUpSavesList()

    def setUpSavesList(self):
        files = [file for file in listdir('saves') if isfile(join('saves', file))]

        saveFiles = []
        for f in files:
            if f[-4:] == ".txt":
                saveFiles.append(f)

        self.savesLabel = IntVar(self.frame)
        if len(saveFiles) == 0:
            self.savesLabel.set("")
            self.selectedSave = ""
            saveFiles.append("")
        else:
            self.savesLabel.set(saveFiles[0])
            self.selectedSave = saveFiles[0]

        self.savesDropDown = OptionMenu(self.frame, self.savesLabel, *saveFiles,
                                        command=self.handleSavesDropDownMenuChange)
        self.savesDropDown.configure(font=('Impact', 15))
        self.savesDropDown.grid(row=3, column=0)

    def handleSavesDropDownMenuChange(self, value):
        self.selectedSave = value

    def handleStartButtonPress(self):
        if self.state == 0:
            self.loadButton.grid_forget()
            self.savesDropDown.grid_forget()
            self.reloadSavesButton.grid_forget()
            self.startButton.configure(text="Creating...")
            thread = Thread(target=self.setToMainMenu)
            thread.start()
        else:
            self.state = 1
            return

    def setToMainMenu(self):
        s = SimMenu.SimMenu(self.gui, self.window, self.centralHandeler, True, self)
        self.centralHandeler.setSimMenu(s)
        self.gui.setMenu(s)
        self.frame.pack_forget()

    def handleLoadButtonPress(self):
        if self.state == 0:
            name = self.getLoadSaveName()
            if not len(name) > 4 or not name[-4:] == ".txt":
                return

            self.savesDropDown.grid_forget()
            self.reloadSavesButton.grid_forget()
            self.startButton.grid_forget()
            self.loadButton.configure(text="Loading...")
            thread = Thread(target=self.load)
            thread.start()
        else:
            self.state = 2
            return

    def getLoadSaveName(self):
        return self.selectedSave

    # load, from the save file save.txt, the simulation in
    # this will set all data of the graphs, neural nets, general sim data, and so on
    def load(self):
        s = SimMenu.SimMenu(self.gui, self.window, self.centralHandeler, False, self)
        self.centralHandeler.setSimMenu(s)
        self.centralHandeler.simMenu.handler.load(self)
        self.centralHandeler.setNetDisplay(self.centralHandeler.simMenu.handler.brains[0])
        self.loadButton.configure(text="Setting up menu")
        self.gui.setMenu(s)
        s.setUpInfoFromLoad()

        self.centralHandeler.settingsMenu.updateSettingsTextBoxes()

        self.frame.pack_forget()
