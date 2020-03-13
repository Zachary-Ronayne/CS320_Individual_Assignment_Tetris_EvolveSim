from tkinter import *

from GuiController import MainGui
from GuiController import GameGui
from GuiController import SettingsGui
from GuiController.Graph import GraphHandler

from TetrisGame import CentralHandler
from TetrisGame import TetrisHandler

from NeuralNet import NeuralNetHandler

import pygame
import Settings


'''

CHANGES TO MAKE:

TODO NEXT:

Fitness changes:
Maybe somehow punish a NeuralNet for making a large stack of tiles, like make fitness gains based on the number
    of tiles in that row, like the amount added for placing a tile is the percentage of that row that is filled
    after the piece is placed

Misc changes:
Allow a subset of pieces to be used, like only suqares and 4x1s, but in any random order, not just a set order

Bugs:
Fix game not updating brain input node graphics correctly when AI makes moves
Fix crash when playing the Tetris game as player?
Fix the RELATIVE_INPUT width and height variables not working unless they are the grid width and height times 2

'''


# a class to keep track of the timing for the main loop updates
class Timer:

    def __init__(self):
        # keeps track of how many ticks have passed until the next full game tick should happen
        self.timer = 0


def updatePyGame():
    # if the game has ended, set the ai control to True and pause the game
    # this is needed to make sure the program doesn't freeze
    if handler.tetrisDisplay.gameOver:
        if not handler.tetrisHandler.toggleAiControl:
            handler.tetrisHandler.toggleAiControl()
        handler.tetrisHandler.stop()

    # check for key presses
    for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        #     pygame.quit()
        # elif event.type == pygame.KEYDOWN:
        if event.type == pygame.KEYDOWN:
            # test to see if the game should be paused or unpaused
            if event.key == pygame.K_p:
                if handler.tetrisHandler.running:
                    handler.tetrisHandler.stop()
                else:
                    handler.tetrisHandler.start()
            # test to see if the game should stop the AI cotnroling the game
            elif event.key == pygame.K_a:
                handler.tetrisHandler.toggleAiControl()
            # test to see if the game should reset
            elif event.key == pygame.K_r:
                handler.tetrisDisplay.resetGame()

            # show or hide all neural net lines
            if handler.displayGame:
                if event.key == pygame.K_n:
                    handler.netDisplay.setAllConnectionRender(True)
                    handler.gameGui.updateNeuralNetSurface(handler.netDisplay)
                elif event.key == pygame.K_m:
                    handler.netDisplay.setAllConnectionRender(False)
                    handler.gameGui.updateNeuralNetSurface(handler.netDisplay)

            # toggle graph view / show graph
            isG = event.key == pygame.K_g
            isH = event.key == pygame.K_h
            isJ = event.key == pygame.K_j
            isF = event.key == pygame.K_f
            s = handler.simMenu
            sLoop = s is not None and (s.testing or s.looping)

            if isG or isH or isJ or isF:
                # if the view is moving from the game, sotp the game
                handler.tetrisHandler.stop()
                # toggle the state of playing
                if isF:
                    handler.displayGame = not handler.displayGame
                # determine which graph to draw
                else:
                    if isG:
                        handler.displayGame = not handler.displayGame and handler.graphHandler.graph == 0
                        handler.graphHandler.graph = 0
                    elif isH:
                        handler.displayGame = not handler.displayGame and handler.graphHandler.graph == 1
                        handler.graphHandler.graph = 1
                    else:
                        handler.displayGame = not handler.displayGame and handler.graphHandler.graph == 2
                        handler.graphHandler.graph = 2
                    if sLoop:
                        handler.displayGame = False

                if not handler.displayGame:
                    # if the user presses a graph button, then draw the graph even though the sim is looping
                    if sLoop:
                        handler.graphHandler.renderWithPygame()

            # handle other key presses
            if handler.tetrisHandler.running and not handler.tetrisHandler.aiControl:
                t = handler.tetrisDisplay
                if event.key == pygame.K_LEFT:
                    t.movePiece(-1)
                if event.key == pygame.K_RIGHT:
                    t.movePiece(1)
                if event.key == pygame.K_UP:
                    t.rotateCurrentPiece(True)
                if event.key == pygame.K_DOWN:
                    t.rotateCurrentPiece(False)
                if event.key == pygame.K_SPACE:
                    t.nextLine()
                if event.key == pygame.K_RETURN:
                    t.snapPieceDown()

            # handle graph key presses
            if not handler.displayGame:
                g = handler.graphHandler.fitnessGraph
                pressed = pygame.key.get_pressed()
                ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
                shift = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]
                # upper percentile lines
                if ctrl:
                    if event.key == pygame.K_1:
                        g.displayLines[0] = not g.displayLines[0]
                    elif event.key == pygame.K_2:
                        g.displayLines[1] = not g.displayLines[1]
                    elif event.key == pygame.K_3:
                        g.displayLines[2] = not g.displayLines[2]
                    elif event.key == pygame.K_4:
                        g.displayLines[3] = not g.displayLines[3]
                    elif event.key == pygame.K_5:
                        g.displayLines[4] = not g.displayLines[4]
                    elif event.key == pygame.K_6:
                        g.displayLines[5] = not g.displayLines[5]
                    elif event.key == pygame.K_7:
                        g.displayLines[6] = not g.displayLines[6]
                    elif event.key == pygame.K_8:
                        g.displayLines[7] = not g.displayLines[7]
                    elif event.key == pygame.K_9:
                        g.displayLines[8] = not g.displayLines[8]
                # lower percentile lines
                elif shift:
                    if event.key == pygame.K_1:
                        g.displayLines[9] = not g.displayLines[9]
                    elif event.key == pygame.K_2:
                        g.displayLines[10] = not g.displayLines[10]
                    elif event.key == pygame.K_3:
                        g.displayLines[11] = not g.displayLines[11]
                    elif event.key == pygame.K_4:
                        g.displayLines[12] = not g.displayLines[12]
                    elif event.key == pygame.K_5:
                        g.displayLines[13] = not g.displayLines[13]
                    elif event.key == pygame.K_6:
                        g.displayLines[14] = not g.displayLines[14]
                    elif event.key == pygame.K_7:
                        g.displayLines[15] = not g.displayLines[15]
                    elif event.key == pygame.K_8:
                        g.displayLines[16] = not g.displayLines[16]
                    elif event.key == pygame.K_9:
                        g.displayLines[17] = not g.displayLines[17]
                # main lines
                else:
                    if event.key == pygame.K_BACKQUOTE:
                        g.displayLines[18] = not g.displayLines[18]
                    elif event.key == pygame.K_1:
                        g.displayLines[19] = not g.displayLines[19]
                    elif event.key == pygame.K_2:
                        g.displayLines[20] = not g.displayLines[20]
                    elif event.key == pygame.K_3:
                        g.displayLines[21] = not g.displayLines[21]
                    elif event.key == pygame.K_4:
                        g.displayLines[22] = not g.displayLines[22]
                    elif event.key == pygame.K_5:
                        g.displayLines[23] = not g.displayLines[23]
                    elif event.key == pygame.K_6:
                        g.displayLines[24] = not g.displayLines[24]
                    elif event.key == pygame.K_7:
                        g.displayLines[25] = not g.displayLines[25]
                    elif event.key == pygame.K_8:
                        g.displayLines[26] = not g.displayLines[26]
                    elif event.key == pygame.K_9:
                        g.displayLines[27] = not g.displayLines[27]
                    elif event.key == pygame.K_0:
                        g.displayLines[28] = not g.displayLines[28]

                # show all lines
                # upper percentile lines
                if ctrl:
                    if event.key == pygame.K_EQUALS:
                        for i in range(9):
                            g.displayLines[i] = True
                    if event.key == pygame.K_MINUS:
                        for i in range(9):
                            g.displayLines[i] = False

                # lower percentile lines
                elif shift:
                    if event.key == pygame.K_EQUALS:
                        for i in range(9):
                            g.displayLines[i + 9] = True
                    if event.key == pygame.K_MINUS:
                        for i in range(9):
                            g.displayLines[i + 9] = False
                else:
                    # main lines
                    if event.key == pygame.K_EQUALS:
                        for i in range(len(g.displayLines)):
                            g.displayLines[i] = True
                    # hide all lines
                    if event.key == pygame.K_MINUS:
                        for i in range(len(g.displayLines)):
                            g.displayLines[i] = False

        # add mouse events back in, this loop is only for key presses
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.event.post(event)

    if handler.tetrisHandler.aiControl:
        refreshRate = Settings.DISP_REFRESH_RATE
    else:
        refreshRate = 60

    # update the graph or game
    if gameTimer.timer >= refreshRate:
        # update the game
        if handler.displayGame:
            if handler.tetrisHandler.running:
                gameTimer.timer = 0
                # only continue to tick the game if it is not over
                if not handler.tetrisDisplay.gameOver:
                    # either make the AI make a move or only allow player moves
                    if handler.tetrisHandler.aiControl:
                        gameGui.tick(handler.tetrisDisplay, handler.netDisplay)
                    else:
                        gameGui.tick(handler.tetrisDisplay, None)
                        NeuralNetHandler.sendInputs(handler.netDisplay, handler.tetrisDisplay)
    else:
        gameTimer.timer += 1

    # draw gui, but only if the simulation is not making a new generation so that processing time is not
    # wasted on rendering during generation calculations
    s = handler.simMenu
    if s is None or not s.testing and not s.looping and not s.handler.loading:
        # draw either the graph or the game

        # game
        if handler.displayGame:
            n = handler.netDisplay
            if n is not None:
                # update the movement of the nodes on the NeuralNEt display, if the net was moved, then redraw it
                if n.moveWithPygame():
                    handler.gameGui.updateNeuralNetSurface(handler.netDisplay)
                # if the game is running, then the neural net also needs to keep updating
                elif handler.tetrisHandler.running:
                    handler.gameGui.updateNeuralNetSurface(handler.netDisplay)

            gameGui.render(handler.tetrisDisplay)
        # graph
        else:
            # send graph movement data
            gNum = handler.graphHandler.graph
            if gNum == 0:
                g = handler.graphHandler.fitnessGraph
                if g is not None:
                    g.moveWithPygame()
            elif gNum == 1:
                g = handler.graphHandler.mutabilityGraph
                if g is not None:
                    g.moveWithPygame()
            elif gNum == 2:
                g = handler.graphHandler.generationsGraph
                if g is not None:
                    g.moveWithPygame()

            # draw
            handler.graphHandler.renderWithPygame()

    # schedule next update
    root.after(1, updatePyGame)


# create timer to keep track of game
gameTimer = Timer()

handler = CentralHandler.CentralHandeler()

# create the graph that will be displayed by pygame
graphHandler = GraphHandler.GraphHandler(handler)
handler.setGraphHandler(graphHandler)

# create the netural net that will be displayed by pygame
net = NeuralNetHandler.createNewNeuralNet(False)
handler.setNetDisplay(net)

# create the Tetris game that will be displayed by pygame
tetrisGame = TetrisHandler.createTetrisGame()
handler.setTetrisDisplay(tetrisGame)

tetrisHandler = TetrisHandler.TetrisHandler(handler)
tetrisHandler.setTetrisGame(tetrisGame)

handler.setTetrisHandler(tetrisHandler)

# create the window used by pygame
gameGui = GameGui.GameGui(handler)
handler.setPyGui(gameGui.gui)
handler.setGameGui(gameGui)

# create the tkinter windows
root = Tk()
handler.setSimWindow(root)

main = MainGui.MainGui(root, handler)
handler.setSimGui(main)

# create secondary tkinter windows
settingsGui = Toplevel(root)
handler.setSettingsGui(settingsGui)
settings = SettingsGui.SettingsGui(handler, settingsGui)
handler.setSettingsMenu(settings.currentMenu)

root.after(1, updatePyGame)

root.mainloop()
