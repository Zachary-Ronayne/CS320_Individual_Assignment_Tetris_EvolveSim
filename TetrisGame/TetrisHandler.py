from TetrisGame import Tetris

# this class handles playing a tetris game


class TetrisHandler:

    def __init__(self, centralHandler):
        self.running = False
        self.tetrisGame = None
        self.centralHandler = centralHandler
        # true if the AI is controlling the game, false otherwise
        # if it is true, only the AI controls the game, if it is false, only the AI controlls the game
        self.aiControl = True

    def toggleAiControl(self):
        self.aiControl = not self.aiControl

    # make the game run
    def start(self):
        self.running = True

    # pause the game
    def stop(self):
        self.running = False

    # set the tetris game of this object to a given object
    def setTetrisGame(self, tetrisGame):
        self.tetrisGame = tetrisGame

    # set the given tkinter root up to take in key inputs
    def setUpKeyInput(self, root):
        root.bind_all("<Key>", self.handleKeyPress)

    # called by the root key event to make a key action
    # this is unused? but needed for tkinter key presses
    def handleKeyPress(self, event):
        # used ot keep track of it the Tetirs game needs to be redrawn
        update = False

        # puase or unpause game
        if event.char == 'p':
            self.running = not self.running

            # move piece to the left
        if event.char == 'a':
            self.tetrisGame.movePiece(-1)
            update = True
            # move piece to the right
        elif event.char == 'd':
            self.tetrisGame.movePiece(1)
            update = True
            # rotate the piece up
        elif event.char == 'w':
            self.tetrisGame.rotateCurrentPiece(True)
            update = True
            # rotate the piece down
        elif event.char == 's':
            self.tetrisGame.rotateCurrentPiece(False)
            update = True
            # manualy advance the game to the next line
        elif event.char == 'z':
            self.tetrisGame.nextLine()
            update = True

        if update:
            self.tetrisGame.renderWithPygame(self.centralHandler.pyGui)


def createTetrisGame():
    tetrisGame = Tetris.Tetris()
    return tetrisGame
