from NeuralNet import NeuralNet

import random
import time
import math

import Settings


# values for setting up render pos values
class R:
    w = Settings.RELATIVE_INPUT_WIDTH
    h = Settings.RELATIVE_INPUT_HEIGHT
    xOffset = Settings.GRID_WIDTH
    yOffset = Settings.GRID_HEIGHT
    # the size of each node
    size = 50
    square = Settings.SQUARE_SIZE
    # the space between each node on the y axis
    ySpace = size / 6
    # the distance between the input and output nodes
    xSpace = 800


# this file handles allowing the neural net to communicate with the Tetris game

# creates a neural net fit for working with the Tetris game
def createNewNeuralNet(createId):
    random.seed(time.time())

    # set variables depending on which type of neural net should be made
    determineRenderVars()

    # create network for distance inputs
    # 32 input nodes because 8 directions for each of the 4 squares in a Tetirs piece
    if Settings.DISTANCE_INPUTS:
        neuralNet = NeuralNet.NeuralNet(32, 4, createId)
    # otherwise create network based on the size of the tetris game
    else:
        if Settings.SPLIT_NEURAL_INPUTS:
            neuralNet = NeuralNet.NeuralNet(R.w * R.h * 2, 4, createId)
        else:
            neuralNet = NeuralNet.NeuralNet(R.w * R.h, 4, createId)

    # set positions of nodes
    setInNodeRenderPos(neuralNet)

    # in nodes render positions
    for i in range(len(neuralNet.inNodes)):
        neuralNet.inNodes[i].setRenderPos((i % R.w - R.xOffset) * R.square + R.square / 2,
                                          (i // R.w - R.yOffset) * R.square + R.square / 2)

    # out nodes render positions
    setOutNodeRenderPos(neuralNet)

    # generate random initital connections
    if Settings.START_CONNECTIONS > 0:
        for h in range(4):
            for i in range(R.w):
                for j in range(h):
                    if random.uniform(0, 1) < Settings.START_CONNECTIONS:
                        neuralNet.addConnection(0, 0, i + j * Settings.GRID_WIDTH, h, random.uniform(-1, 1))

    # return network
    return neuralNet


# determine which values to use for render variables
def determineRenderVars():
    if Settings.RELATIVE_NEURAL_INPUTS:
        R.w = Settings.RELATIVE_INPUT_WIDTH
        R.h = Settings.RELATIVE_INPUT_HEIGHT
        R.xOffset = Settings.GRID_WIDTH
        R.yOffset = Settings.GRID_HEIGHT
    else:
        R.w = Settings.GRID_WIDTH
        R.h = Settings.GRID_HEIGHT
        R.xOffset = 0
        R.yOffset = 0


def setInNodeRenderPos(neuralNet):
    for i in range(len(neuralNet.inNodes)):
        neuralNet.inNodes[i].setRenderPos((i % R.w - R.xOffset) * R.square + R.square / 2,
                                          (i // R.w - R.yOffset) * R.square + R.square / 2)


def setOutNodeRenderPos(neuralNet):
    for i in range(len(neuralNet.outNodes)):
        neuralNet.outNodes[i].setRenderPos(R.xSpace + R.size / 2,
                                           i * (R.size + R.ySpace) + R.size / 2)


# calculates and feeds the inputs of the given tetris game to the given NeuralNet
def sendInputs(neuralNet, tetris):
    # first feed inputs into the net
    inputs = []
    g = tetris.grid

    # determine inputs based on the distance of each Tetris piece from everything else like walls and placed tiles
    if Settings.DISTANCE_INPUTS:
        # once set of 8 directions for each tile in a Tetris piece
        for tile in range(4):
            x = tetris.currentPiece.getX(tile)
            y = tetris.currentPiece.getY(tile)

            w = len(g) - 1
            h = len(g[0]) - 1

            # direction up
            i = 0
            while 0 <= y - i < h and 0 <= x < w and not g[x][y - i]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction up right
            i = 0
            while 0 <= y - i < h and 0 <= x + i < w and not g[x + i][y - i]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction right
            i = 0
            while 0 <= y < h and 0 <= x + i < w and not g[x + i][y]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction down right
            i = 0
            while 0 <= y + i < h and 0 <= x + i < w and not g[x + i][y + i]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction down
            i = 0
            while 0 <= y + i < h and 0 <= x < w and not g[x][y + i]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction down left
            i = 0
            while 0 <= y + i < h and 0 <= x - i < w and not g[x - i][y + i]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction left
            i = 0
            while 0 <= y < h and 0 <= x - i < w and not g[x - i][y]:
                i += 1
            inputs.append(sigmoid(i - 1))

            # direction left up
            i = 0
            while 0 <= y - i < h and 0 <= x - i < w and not g[x - i][y - i]:
                i += 1
            inputs.append(sigmoid(i - 1))

    # determine inputs based on the state of each tile
    else:
        # for relative position neural inputs
        if Settings.RELATIVE_NEURAL_INPUTS:
            p = tetris.currentPiece

            # go through entire grid in each direction * 2
            w = Settings.RELATIVE_INPUT_WIDTH
            h = Settings.RELATIVE_INPUT_HEIGHT
            for y in range(h):
                for x in range(w):
                    # send each input based on if they are outside the grid,
                    # 0 is always for outside the grif
                    # otherwise it is the same values for as if it was not relative

                    # first find the coordinates on the grid based on the current (x, y) of the itterations of the loop
                    # and based on the (x, y) of the current piece

                    # these coordinates are the indexes of the array
                    iX = x - Settings.GRID_WIDTH
                    iY = y - Settings.GRID_HEIGHT

                    # based on those coordinates, append a -1, 0, or 1 to the inputs
                    if 0 <= iX < Settings.GRID_WIDTH and 0 <= iY < Settings.GRID_HEIGHT:
                        if g[iX][iY]:
                            inputs.append(1)
                        else:
                            inputs.append(0)
                    else:
                        inputs.append(0)

            # set the inputs of neural net for the current piece, based on its position
            for j in range(len(p.tiles)):
                iX = p.getX(j) + Settings.GRID_WIDTH
                iY = p.getY(j) + Settings.GRID_HEIGHT
                inputs[iY * w + iX] = -1

        # for set position neural inputs
        else:
            if Settings.SPLIT_NEURAL_INPUTS:
                # get all the spots from the current grid for the main grid
                for y in range(Settings.GRID_HEIGHT):
                    for x in range(Settings.GRID_WIDTH):
                        if g[x][y]:
                            inputs.append(1)
                        else:
                            inputs.append(0)

                # get all the spots from the current grid for the currently controlled piece
                for y in range(Settings.GRID_HEIGHT):
                    for x in range(Settings.GRID_WIDTH):
                        foundPiece = False
                        for p in range(4):
                            if tetris.currentPiece.getX(p) == x and tetris.currentPiece.getY(p) == y:
                                foundPiece = True
                                break
                        if foundPiece:
                            inputs.append(1)
                        else:
                            inputs.append(0)
            else:
                # get all the spots from the current grid
                for y in range(Settings.GRID_HEIGHT):
                    for x in range(Settings.GRID_WIDTH):
                        if g[x][y]:
                            inputs.append(1)
                        else:
                            inputs.append(0)

                # get the inputs from the current piece
                p = tetris.currentPiece
                for j in range(len(p.tiles)):
                    x = p.getX(j)
                    y = p.getY(j)
                    if 0 <= x < Settings.GRID_WIDTH and 0 <= y < Settings.GRID_HEIGHT:
                        inputs[y * Settings.GRID_WIDTH + x] = -1

    # send the inputs
    neuralNet.setInputs(inputs)


def sigmoid(x):
    return 1.0 / (1.0 + pow(math.e, -x))


# this will make the given neural net make a set number of moves
# use None for centralHandeler if no graphical updates should happen
# when RELATIVE_NEURAL_INPUTS is False, the inputs will be of size GRID_WIDTH * GRID_HEIGHT
# when RELATIVE_NEURAL_INPUTS is True, the inputs will be of size (GRID_WIDTH * 2) * (GRID_HEIGHT * 2)
def makeNeuralNetMove(neuralNet, tetris, centralHandler):

    # allow the NeuralNet to make a number of moves per line
    for i in range(Settings.NUMBER_NET_MOVES):

        sendInputs(neuralNet, tetris)

        # now calculate the output values
        neuralNet.calculateOutputs()

        # now use the outputs to decide which moves to make for the current piece

        outputs = neuralNet.getOutputs()

        # output[0] = move left button
        # output[1] = move right button
        # output[2] = rotate up button
        # output[3] = rotate down button

        # if exactly one of the move left or move right buttons is > 0, then move in that direction
        # otherwise, don't move

        # if exactly one of the rotate up or rotate down buttons is > 0, then rotate in that direction
        # othersie don't rotate

        # variable to see if the neural net made a move
        update = False

        if outputs[0] > 0 and not outputs[1] > 0:
            update = tetris.movePiece(-1) or update
        elif not outputs[0] > 0 and outputs[1] > 0:
            update = tetris.movePiece(1) or update

        if outputs[2] > 0 and not outputs[3] > 0:
            update = tetris.rotateCurrentPiece(True) or update
        elif not outputs[2] > 0 and outputs[3] > 0:
            update = tetris.rotateCurrentPiece(False) or update

        if update:
            if centralHandler is not None:
                tetris.renderWithPygame(centralHandler.pyGui, centralHandler)
                neuralNet.renderWithPygame(centralHandler.pyGui, centralHandler)
        # if no move was made, that means that the NeuralNet doesn't want to move anymore, so exit the loop
        else:
            break
