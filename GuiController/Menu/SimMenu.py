from tkinter import *
from GuiController.Menu import Menu

from GuiController.Menu.MenuHandlers import SimMenuHandler

from threading import Thread

import Settings

import functools
import random
import time


class SimMenu(Menu.Menu):

    def __init__(self, gui, window, centralHandler, newSim, initMenu):
        super().__init__(gui, window)

        self.centralHandler = centralHandler

        # true if the menu is currently testing a generation, when this is true, the button that starts the next
        # generation does nothing
        self.testing = True
        # true if the generaitons are currently looping
        self.looping = False
        # true if the menu is currently saving
        self.saving = False
        # true if the menu should automatically save the simulation after each generaiton is tested
        self.autoSave = False
        # the number of neural nets tested in the current generation
        self.netsTested = 0

        self.simButtons = []
        self.nextGenButton = None
        self.loopGensButton = None
        self.infoLabel = None
        self.advancedInfoLabel = None
        self.saveSimButton = None
        self.autoSaveButton = None
        self.setRandomSeedButton = None
        self.setSeedFrame = None
        self.pickSetSeedButton = None
        self.useSetSeedList = None
        self.seedLabel = None
        self.typeInSeedField = None
        self.UseTypeInSeed = None

        self.saveTextBox = None

        self.selectedSetSeed = Settings.SET_SEED_GAMES[0]

        self.handler = SimMenuHandler.SimMenuHandler(self.centralHandler, newSim, initMenu)
        if newSim:
            self.resetMenu()
            self.setUpHandler(initMenu)
        else:
            self.testing = False

    def setUpHandler(self, initMenu):
        self.handler.testGeneration(initMenu, False)
        self.testing = False
        self.netsTested = 0

        if self.looping:
            self.nextGenThread()

        self.updateInfoLabelText()
        for i in range(Settings.NUM_BRAINS):
            self.simButtons[i].configure(text=self.brainButtonText(i))

    def resetMenu(self):

        self.frame.configure(bg="#555555")

        self.netsTested = 0

        # this section creates a frame of the same size as the above
        # to display the buttons and other info for the simulation
        simButtonsFrame = Frame(self.frame, bg="#000000", padx=20)
        simButtonsFrame.pack_propagate(0)
        simButtonsFrame.grid(column=0, row=0)

        self.simButtons = []
        for i in range(len(self.handler.brains)):
            b = Button(simButtonsFrame, text=self.brainButtonText(i),
                       command=functools.partial(self.handleSimButtonPress, i))
            b.configure(font=('Impact', Settings.FONT_SIZE))
            if Settings.STICKY_GUI:
                b.grid(column=int(i % Settings.NUM_BUTTON_COL), row=int(i / Settings.NUM_BUTTON_COL),
                       sticky=N + S + E + W)
            else:
                b.grid(column=int(i % Settings.NUM_BUTTON_COL), row=int(i / Settings.NUM_BUTTON_COL))
            self.simButtons.append(b)

        # make sure all the buttons are sticky to fill the page and keep all text visible
        if Settings.STICKY_GUI:
            for i in range(Settings.NUM_BUTTON_COL):
                Grid.columnconfigure(simButtonsFrame, i, weight=1)
            for i in range(int(len(self.handler.brains) / Settings.NUM_BUTTON_COL)):
                Grid.rowconfigure(simButtonsFrame, i, weight=1)

        self.updateCentralHandler()

        # make a frame to house buttons for controlling the sim
        buttonFrame = Frame(self.frame)
        buttonFrame.grid(column=1, row=0)

        # add a button to go to the next generation
        self.nextGenButton = Button(buttonFrame, text="Next Gen", command=self.handleNextGenButtonPress)
        setUpMenuObject(self.nextGenButton, 0)

        # add button to loop gens
        self.loopGensButton = Button(buttonFrame, text="Loop Gens", command=self.handleLoopGensButtonPress)
        setUpMenuObject(self.loopGensButton, 1)

        # add label for some simulation information
        self.infoLabel = Label(buttonFrame, text="")
        self.updateInfoLabelText()
        setUpMenuObject(self.infoLabel, 2)

        # add a label for the advanced info of the selected NeuralNEt
        self.advancedInfoLabel = Label(buttonFrame, text="")
        setUpMenuObjectFontSize(self.advancedInfoLabel, 3, 15)
        self.setAdvancedInfoText(0)

        # add button to save sim
        self.saveSimButton = Button(buttonFrame, text="Save sim", command=self.handleSaveSimButtonPress)
        setUpMenuObject(self.saveSimButton, 4)

        # add text box for typing in save file name
        saveNameFrame = Frame(buttonFrame)
        saveNameFrame.grid(column=0, row=5)
        self.saveTextBox = Label(saveNameFrame, text="Save name:\n(Only use numbers/letters)")
        setUpColumnmObjectFontSize(self.saveTextBox, 0, 0, 15)
        self.saveTextBox = Text(saveNameFrame, width=20, height=1)
        self.saveTextBox.insert(END, "save")
        setUpColumnmObjectFontSize(self.saveTextBox, 0, 1, 15)

        # add button to toggle auto save
        self.autoSaveButton = Button(buttonFrame, text="Autosave off", command=self.handleAutoSaveButtonPress)
        setUpMenuObject(self.autoSaveButton, 6)

        # add button to pick a random seed
        self.setRandomSeedButton = Button(buttonFrame, text="Pick random seed",
                                          command=self.handleRandomSeedButtonPress)
        setUpMenuObjectFontSize(self.setRandomSeedButton, 7, 15)

        # create frame for set seed stuff
        self.setSeedFrame = Frame(buttonFrame)
        self.setSeedFrame.grid(column=0, row=8)

        # add dropdown menu to select seed
        # create a label
        self.seedLabel = IntVar(self.setSeedFrame)
        self.seedLabel.set(Settings.SET_SEED_GAMES[0])
        # create a list of all seeds
        seeds = []
        for s in Settings.SET_SEED_GAMES:
            seeds.append(s)
        # add list
        self.useSetSeedList = OptionMenu(self.setSeedFrame, self.seedLabel, *seeds)
        setUpColumnmObjectFontSize(self.useSetSeedList, 0, 0, 12)
        # set up drop down menu call
        self.seedLabel.trace('w', self.handleSetSeedDropDownMenuChange)
        # create button for selecting the seed
        self.pickSetSeedButton = Button(self.setSeedFrame, text="Use set seed",
                                        command=self.handlePickSetSeedButtonPress)
        setUpColumnmObjectFontSize(self.pickSetSeedButton, 1, 0, 12)

        # add text field for typing in seed
        self.typeInSeedField = Text(self.setSeedFrame, height=1, width=15)
        setUpColumnmObjectFontSize(self.typeInSeedField, 0, 1, 12)

        # add button for using typed in seed
        self.UseTypeInSeed = Button(self.setSeedFrame, text="Set typed seed",
                                    command=self.handleUseTypeInSeedButtonPress)
        setUpColumnmObjectFontSize(self.UseTypeInSeed, 1, 1, 12)

        # make sure all the buttons and framse stay sticky if STICK_GUI is True
        if Settings.STICKY_GUI:
            for i in range(2):
                Grid.columnconfigure(self.setSeedFrame, i, weight=1)
            for i in range(2):
                Grid.rowconfigure(self.setSeedFrame, i, weight=1)

        # make sure all the buttons and frames stay sticky if STICK_GUI is True
        if Settings.STICKY_GUI:
            for i in range(0):
                Grid.columnconfigure(buttonFrame, i, weight=1)
            for i in range(7):
                Grid.rowconfigure(buttonFrame, i, weight=1)

    def updateInfoLabelText(self):
        s = "Current gen: " + str(self.handler.generation)
        if self.testing:
            if Settings.SET_SEED and not self.handler.generation == 0:
                div = Settings.NUM_BRAINS / 2
            else:
                div = Settings.NUM_BRAINS
            s += "\nGen done:\n" + str(round(100.0 * (self.netsTested / div), 2)) + "%"
        self.infoLabel.configure(text=s)

    # sets the seed of the game to a random seed and resets the game, only if the tetris game is not None
    def handleRandomSeedButtonPress(self):
        if not self.looping and not self.testing:
            t = self.centralHandler.tetrisDisplay
            if t is not None:
                t.resetGame()
                random.seed(time.time())
                t.makeNewPiece()

    # sets the seed of the game to the selected set seed and resets the game, only if the tetris game is not None
    def handlePickSetSeedButtonPress(self):
        if not self.looping and not self.testing:
            t = self.centralHandler.tetrisDisplay
            if t is not None:
                t.resetGame()
                random.seed(self.selectedSetSeed)
                t.makeNewPiece()

    def handleSetSeedDropDownMenuChange(self, *args):
        if not self.looping and not self.testing:
            self.selectedSetSeed = self.seedLabel.get()

    def handleUseTypeInSeedButtonPress(self, *args):
        if not self.looping and not self.testing:
            self.selectedSetSeed = self.typeInSeedField.get("1.0", END)

    def handleAutoSaveButtonPress(self):
        self.autoSave = not self.autoSave
        if self.autoSave:
            self.autoSaveButton.configure(text="Autosave on")
        else:
            self.autoSaveButton.configure(text="Autosave off")

    # called when a sim button is pressed, should set the corresponding neural net index from the handeler as
    # the current net to view, and reset the displayed tetris game
    def handleSimButtonPress(self, index):
        # only allow the button press if the sim is not looping and not testing a generation
        if not self.testing and not self.looping:
            self.centralHandler.setNetDisplay(self.handler.brains[index])
            self.centralHandler.tetrisHandler.stop()
            self.centralHandler.tetrisDisplay.resetGame()
            self.setAdvancedInfoText(index)

    # set the text of the advanced info button the brain of the specified index
    def setAdvancedInfoText(self, index):
        if self.advancedInfoLabel is not None:
            b = self.handler.brains[index]

            s = "Selected:\n"\
                "Id: " + str(b.id) + "\n"\
                "Fit: " + str(b.fitness) + "\n"\
                "Mut: " + str(b.mutability) + "\n"\
                "Birth gen: " + str(b.birthGen) + "\n"\
                "Parent id: "

            if b.parentId == -1:
                s += "WILD"
            else:
                s += str(b.parentId)

            self.advancedInfoLabel.configure(text=s)

    def handleLoopGensButtonPress(self):
        self.centralHandler.tetrisHandler.stop()
        self.centralHandler.tetrisDisplay.resetGame()
        self.loopGens()

    def handleNextGenButtonPress(self):
        self.centralHandler.tetrisHandler.stop()
        self.centralHandler.tetrisDisplay.resetGame()
        if not self.looping:
            self.nextGenThread()
        else:
            self.nextGenButton.configure(text="Testing\nGen")

    def handleSaveSimButtonPress(self):
        if not self.saving and not self.looping and not self.testing:
            self.save()

    def save(self):
        self.saving = True
        self.saveSimButton.configure(text="Saving...")
        thread = Thread(target=self.saveThread())
        thread.start()

    def saveThread(self):
        self.handler.save()
        self.saveSimButton.configure(text="Save Sim")
        self.saving = False

    # gets the string the user typed in and converts it to only use numbers and letters
    def getValidSaveName(self):
        text = self.saveTextBox.get("1.0", END)
        saveName = ""
        for c in text:
            if c.isdigit() or c.isalpha():
                saveName += c

        if saveName == "":
            saveName = "save"

        return saveName

    # begins testing another generation, after that generation is done testing, another one is started automatically
    # loop stops when the button is pressed again
    # should only be called by self.loopGensButton
    def loopGens(self):
        self.looping = not self.looping
        if self.looping:
            self.loopGensButton.configure(text="Looping\npress to\nstop")
        else:
            self.loopGensButton.configure(text="Loop gens")

        self.nextGenThread()

    # creates a thread to generate the next generation
    def nextGenThread(self):
        # only make the thread if a generation is currently not being tested
        if self.testing:
            return

        self.testing = True

        self.nextGenButton.configure(text="Testing Gen")

        genThread = Thread(target=self.nextGen)
        genThread.start()

    def nextGen(self):
        # make and test the new geenration
        self.handler.nextGeneration(self)
        self.handler.testGeneration(self, True)

        self.nextGenButton.configure(text="Updating Info")

        self.testing = False

        if self.looping:
            self.nextGenThread()
        else:
            self.updateCentralHandler()

        self.netsTested = 0

        # only update graphics and selected game when not looping to prevent large delays between generations
        # also only update the text of the sim buttons when not looping, again to prevent lag
        if self.looping:
            self.setAdvancedInfoText(0)
        else:
            self.nextGenButton.configure(text="Updating Buttons")
            for i in range(Settings.NUM_BRAINS):
                self.simButtons[i].configure(text=self.brainButtonText(i))

        self.updateInfoLabelText()

        # handle auto saving
        if self.autoSave:
            self.nextGenButton.configure(text="Autosaving")
            self.saveSimButton.configure(text="Saving...")
            self.saving = True
            self.saveThread()

        if not self.looping:
            self.nextGenButton.configure(text="Next Gen")
        else:
            self.nextGenButton.configure(text="Moving to Next")

    # set the neuralNet in the central handler to the top performer
    def updateCentralHandler(self):
        self.centralHandler.setNetDisplay(self.handler.brains[0])
        self.centralHandler.tetrisDisplay.resetGame()
        if self.centralHandler.displayGame:
            self.centralHandler.netDisplay.renderWithPygame(self.centralHandler.pyGui, self.centralHandler)
        self.setAdvancedInfoText(0)

    # get the button text for the brain with the given index i
    def brainButtonText(self, i):
        if len(self.handler.brains) <= i:
            return ""
        return "id: " + str(self.handler.brains[i].id) +\
               "\nf: " + str(round(self.handler.brains[i].fitness, 2)) +\
               "\nm: " + str(round(self.handler.brains[i].mutability, 2))

    # should be called when a simulation is loaded
    # this will set all of the information of the sim menu to the appropriate labels
    def setUpInfoFromLoad(self):
        self.nextGenButton.configure(text="Next Gen")
        self.loopGensButton.configure(text="Loop Gens")
        self.setAdvancedInfoText(0)
        self.infoLabel.configure(text="Current gen: " + str(self.handler.generation))

    # update the current seeds list based on the current setting
    def updateSetSeedList(self):
        seeds = []
        for s in Settings.SET_SEED_GAMES:
            seeds.append(s)
        # add list
        self.useSetSeedList = OptionMenu(self.setSeedFrame, self.seedLabel, *seeds)
        setUpColumnmObjectFontSize(self.useSetSeedList, 0, 0, 12)

    def updateGridButtonsFontSize(self):
        for b in self.simButtons:
            b.configure(font=('Impact', Settings.FONT_SIZE))

    def updateButtonsGridLayout(self):
        cnt = 0
        for b in self.simButtons:
            b.grid(column=int(cnt % Settings.NUM_BUTTON_COL), row=int(cnt / Settings.NUM_BUTTON_COL),
                   sticky=N + S + E + W)
            cnt += 1


# set up a menu object for the side of the menu like a button or label
def setUpMenuObject(obj, index):
    setUpMenuObjectFontSize(obj, index, 30)


# set up a menu object for the side of the menu like a button or label
def setUpMenuObjectFontSize(obj, index, fontSize):
    obj.configure(font=('Impact', fontSize))
    if Settings.STICKY_GUI:
        obj.grid(column=0, row=index, sticky=N + S + E + W)
    else:
        obj.grid(column=0, row=index)


# set up a menu object in a colun for the side of the menu like a button or label
def setUpColumnmObjectFontSize(obj, x, y, fontSize):
    obj.configure(font=('Impact', fontSize))
    if Settings.STICKY_GUI:
        obj.grid(column=x, row=y, sticky=N + S + E + W)
    else:
        obj.grid(column=x, row=y)
