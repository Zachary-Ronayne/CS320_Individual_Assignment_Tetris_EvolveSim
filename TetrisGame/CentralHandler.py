# a class that allows all the simulation objects and guis to communicate with each other
class CentralHandeler:

    def __init__(self):
        # the game displayed on the sim gui
        self.tetrisDisplay = None
        # the net displayed on the net gui
        self.netDisplay = None
        # the gui that controls the pygame
        self.pyGui = None
        # the GameGui object used by the simulation
        self.gameGui = None
        # the gui that controls the sim menu
        self.simWindow = None
        # the handler for the tetris game
        self.tetrisHandler = None
        # the sim menu of the program
        self.simMenu = None
        # the gui of the settings menu
        self.settingsMenu = None
        # the handler that keeps track of the graph being displayed
        self.graphHandler = None
        # the gui of the settings menu
        self.settingsGui = None
        # the gui of the settings menu
        self.simGui = None

        # true if the Tetirs game and neural net should be displayed, False to display the graph
        self.displayGame = True

    def setTetrisDisplay(self, tetris):
        self.tetrisDisplay = tetris

    def setNetDisplay(self, net):
        self.netDisplay = net
        if self.gameGui is not None:
            self.gameGui.updateNeuralNetSurface(self.netDisplay)

    def setPyGui(self, pyGui):
        self.pyGui = pyGui

    def setGameGui(self, gameGui):
        self.gameGui = gameGui
        self.gameGui.updateNeuralNetSurface(self.netDisplay)

    def setSimWindow(self, simWindow):
        self.simWindow = simWindow

    def setTetrisHandler(self, handler):
        self.tetrisHandler = handler

    def setSimMenu(self, simMenu):
        self.simMenu = simMenu

    def setSettingsMenu(self, settingsMenu):
        self.settingsMenu = settingsMenu

    def setGraphHandler(self, graphHandler):
        self.graphHandler = graphHandler

    def setSettingsGui(self, settingsGui):
        self.settingsGui = settingsGui

    def setSimGui(self, simGui):
        self.simGui = simGui
