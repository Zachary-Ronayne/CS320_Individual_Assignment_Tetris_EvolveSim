import Settings


# fileWriter: an opened fileReader in read mode
# this should load in all the settings from the given file reader
# the file must be at a valid line to load in the settings
def loadSettings(fileReader):
    fileReader.readline()
    Settings.GRID_WIDTH = loadInt(fileReader.readline())
    Settings.GRID_HEIGHT = loadInt(fileReader.readline())
    Settings.GRID_X = loadInt(fileReader.readline())
    Settings.GRID_Y = loadInt(fileReader.readline())
    Settings.SQUARE_SIZE = loadInt(fileReader.readline())
    Settings.GRID_SIZE = loadInt(fileReader.readline())
    Settings.GRID_LINE = loadInt(fileReader.readline())
    fileReader.readline()
    Settings.NUM_BRAINS = loadInt(fileReader.readline())
    Settings.MAX_MUTABILITY = loadFloat(fileReader.readline())
    Settings.WEIGHT_BIAS_SCALAR = loadFloat(fileReader.readline())
    Settings.MUTABILITY_CHANGE = loadFloat(fileReader.readline())
    Settings.START_CONNECTIONS = loadFloat(fileReader.readline())
    Settings.REMOVE_NODE_SCALAR = loadFloat(fileReader.readline())
    Settings.ADD_NODE_CHANCES = loadInt(fileReader.readline())
    Settings.MIN_ADD_NODE_CHANCE = loadInt(fileReader.readline())
    Settings.ADD_NODE_SCALAR = loadFloat(fileReader.readline())
    Settings.ADD_NODE_TO_OUTER_CHANCE = loadFloat(fileReader.readline())
    Settings.COPY_CONNECTION_CHANCES = loadInt(fileReader.readline())
    Settings.MIN_COPY_CONNECTION_CHANCE = loadInt(fileReader.readline())
    Settings.COPY_CONNECTION_SCALAR = loadFloat(fileReader.readline())
    Settings.COPY_CONNECTION_FROM_IN_CHANCE = loadFloat(fileReader.readline())
    Settings.CONNECTION_CHANCES = loadInt(fileReader.readline())
    Settings.MIN_CONNECTION_CHANCE = loadInt(fileReader.readline())
    Settings.CONNECTION_SCALAR = loadFloat(fileReader.readline())
    Settings.ADD_CONNECTION_PROBABILITY = loadFloat(fileReader.readline())
    fileReader.readline()
    Settings.SET_SEED = loadBoolean(fileReader.readline())
    Settings.DISTANCE_INPUTS = loadBoolean(fileReader.readline())
    Settings.RELATIVE_NEURAL_INPUTS = loadBoolean(fileReader.readline())
    Settings.SPLIT_NEURAL_INPUTS = loadBoolean(fileReader.readline())
    Settings.RELATIVE_INPUT_WIDTH = loadInt(fileReader.readline())
    Settings.RELATIVE_INPUT_HEIGHT = loadInt(fileReader.readline())
    s = fileReader.readline()
    numSeeds = int(s[s.index(": ") + 2:s.index(",")])
    Settings.SET_SEED_GAMES = []
    for i in range(numSeeds):
        s = s[s.index(",") + 1:len(s)]
        Settings.SET_SEED_GAMES.append(int(s[0:s.index(",")]))
    Settings.RANDOM_SEED_GAMES = loadInt(fileReader.readline())

    fileReader.readline()
    line = fileReader.readline()
    pieces = [int(s) for s in line.split()]
    fileReader.readline()
    line = fileReader.readline()
    rotates = [int(s) for s in line.split()]
    Settings.PIECE_SEQUENCE = []
    for i in range(len(pieces)):
        s = (pieces[i], rotates[i])
        Settings.PIECE_SEQUENCE.append(s)

    Settings.REMOVE_OUTLIER_FITNESS = loadFloat(fileReader.readline())
    Settings.REMOVE_FITNESS_TYPE = loadInt(fileReader.readline())
    Settings.USE_FILLED_FOR_FITNESS = loadBoolean(fileReader.readline())
    Settings.NUMBER_NET_MOVES = loadInt(fileReader.readline())
    Settings.FITNESS_PIECE = loadFloat(fileReader.readline())
    Settings.FITNESS_LINE = loadFloat(fileReader.readline())
    Settings.FITNESS_SCALAR = loadFloat(fileReader.readline())
    Settings.DISP_REFRESH_RATE = loadInt(fileReader.readline())
    Settings.MAX_ROWS = loadInt(fileReader.readline())
    Settings.PERCENT_BEST_REMOVE = loadFloat(fileReader.readline())
    fileReader.readline()
    Settings.STICKY_GUI = loadBoolean(fileReader.readline())
    Settings.FONT_SIZE = loadInt(fileReader.readline())
    Settings.NUM_BUTTON_COL = loadInt(fileReader.readline())


def loadDefaultSettings():
    Settings.GRID_WIDTH = 10
    Settings.GRID_HEIGHT = 21
    Settings.GRID_X = 10
    Settings.GRID_Y = 10
    Settings.SQUARE_SIZE = 18
    Settings.GRID_SIZE = 38
    Settings.GRID_LINE = 1
    Settings.NUM_BRAINS = 500
    Settings.MAX_MUTABILITY = 2
    Settings.WEIGHT_BIAS_SCALAR = 0.08
    Settings.MUTABILITY_CHANGE = .5
    Settings.START_CONNECTIONS = 0
    Settings.REMOVE_NODE_SCALAR = 0.05
    Settings.ADD_NODE_CHANCES = 3
    Settings.MIN_ADD_NODE_CHANCE = 1
    Settings.ADD_NODE_SCALAR = 0.1
    Settings.ADD_NODE_TO_OUTER_CHANCE = 0.3
    Settings.COPY_CONNECTION_CHANCES = 3
    Settings.MIN_COPY_CONNECTION_CHANCE = 1
    Settings.COPY_CONNECTION_SCALAR = .65
    Settings.COPY_CONNECTION_FROM_IN_CHANCE = .4
    Settings.CONNECTION_CHANCES = 5
    Settings.MIN_CONNECTION_CHANCE = 1
    Settings.CONNECTION_SCALAR = .8
    Settings.ADD_CONNECTION_PROBABILITY = .7
    Settings.SET_SEED = False
    Settings.DISTANCE_INPUTS = False
    Settings.RELATIVE_NEURAL_INPUTS = False
    Settings.SPLIT_NEURAL_INPUTS = False
    Settings.RELATIVE_INPUT_WIDTH = int(Settings.GRID_WIDTH * 2.0)
    Settings.RELATIVE_INPUT_HEIGHT = int(Settings.GRID_HEIGHT * 2.0)
    Settings.SET_SEED_GAMES = [1, 2, 3, 4]
    Settings.RANDOM_SEED_GAMES = 4
    Settings.PIECE_SEQUENCE = []
    Settings.REMOVE_OUTLIER_FITNESS = .2
    Settings.REMOVE_FITNESS_TYPE = 0
    Settings.USE_FILLED_FOR_FITNESS = True
    Settings.NUMBER_NET_MOVES = 10
    Settings.FITNESS_PIECE = 1
    Settings.FITNESS_LINE = 10
    Settings.FITNESS_SCALAR = 0
    Settings.DISP_REFRESH_RATE = 0
    Settings.MAX_ROWS = 500
    Settings.PERCENT_BEST_REMOVE = 0.15
    Settings.STICKY_GUI = True
    Settings.FONT_SIZE = 7
    Settings.NUM_BUTTON_COL = 25


# loads an integer from the given string in the form "label: number\n"
# returns the loaded int
def loadInt(s):
    return int(s[s.index(": ") + 2:len(s) - 1])


# loads an integer from the given string in the form "number\n"
# returns the loaded int
def intLine(s):
    return int(s[0:len(s) - 1])


# loads a float from the given string in the form "label: number\n"
# returns the loaded float
def loadFloat(s):
    return float(s[s.index(": ") + 2:len(s) - 1])


# loads a float from the given string in the form "number\n"
# returns the loaded float
def floatLine(s):
    return float(s[0:len(s) - 1])


# loads a boolean from the given string in the form "label: bool\n"
# returns False if the value is false, returns True otherwise
def loadBoolean(b):
    s = b[b.index(": ") + 2:len(b) - 1]
    if s == "False":
        return False
    else:
        return True
