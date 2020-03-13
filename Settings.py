import SaveLoader

# tetris grid variables

# the number of tiles in the width of the grid
GRID_WIDTH = 10

# the number of tiles in the height of the grid
GRID_HEIGHT = 21

# x and y are the upper left hand corner of where the game is drawn on the scren
GRID_X = 10
GRID_Y = 10

# the size of each square in the tetris grid as rendered to the neural net display
SQUARE_SIZE = 18

# the width and hight of a game tile as drawn to the screen
GRID_SIZE = 38

# the thickness of a game tile line as drawn to the screen
GRID_LINE = 1


# neural net variables

# the number of neural networks in a simulation, keep this to even integers > 0
NUM_BRAINS = 40

# the maximum that the absolute value of mutability can be, if this value is n, then mutability range is (-n, n)
# mutability governs the rate that all mutations occur
# the current mutability of a neural net determines:
#   how much a node weight or bias can go up or down
#   the number of inner nodes that can be removed or added
#   the number of connections that can be removed or added
#   the chance of any particular node or connection to be removed or added
# keep this value to positive numbers only
# generally anyhting > 4 will make very wild mutations and is not recomended
MAX_MUTABILITY = .2

# this value is multiplied the the amount added to a bias or connection during a mutation
# the amount added is a random value between mutability and -mutability, and that value is
# multiplied by WEIGHT_BIAS_SCALAR
WEIGHT_BIAS_SCALAR = 0.08

# the max amount that can be added or subtracted from mutability during a mutation
# set to a negative value to allow mutability to change to any valid mutability during a mutation, evenly distributed
# over the valid range of (-MAX_MUTABILITY, MAX_MUTABILITY)
MUTABILITY_CHANGE = -1

# the chance for each possible connection from an input node to an output to happen
# use 0 to start with no connections
# use 1 to have a 100% chance
# use anything in between to have that probability of a connection initially being generated
START_CONNECTIONS = 0

# the inital probability for each node to be removed during a mutation
# the current mutability of the NeuralNet decreases or increases this probaility
# based on what percentage of MAX_MUTABILITY the current mutability is
REMOVE_NODE_SCALAR = 0.05

# the initial number of chances a node has to be added during a mutation
# this number is multiplied by the current mutability to determine the actual number of chances the NeuralNet has of
# gaining a node
ADD_NODE_CHANCES = 3

# the minimum amount of nodes that have a chance to be added during a mutation
# keep this value >= 0
MIN_ADD_NODE_CHANCE = 1

# the probability that each chance to add a node will succeed
# the current mutability of the NeuralNet decreases or increases this probaility
# based on what percentage of MAX_MUTABILITY the current mutability is
ADD_NODE_SCALAR = 0.1

# the probability that, when an inner node is added, that it will be added to a connection that feeds into an
# outer node
# 1 - ADD_NODE_TO_OUTER_CHANCE = probability to add a node to an inner node connection
# if there are no inner node connections, then no node will be added, even if all over values line up
ADD_NODE_TO_OUTER_CHANCE = 0.3

# the number of chances a random connection can be picked to be coppied or moved from an adjacent input node
# this number is multiplied by the current mutability to determine the actual number of chances the NeuralNet has of
# copying or moving a connection
# connections will only be coppied to places that don't already have connections
COPY_CONNECTION_CHANCES = 3

# the minimum amount of chances to have an in node connection coppied or moved
MIN_COPY_CONNECTION_CHANCE = 1

# the initial probabiliy for each chance to move or copy a connection will succeed
# the current mutability of the NeuralNet decreases or increases this probaility
# based on what percentage of MAX_MUTABILITY the current mutability is
COPY_CONNECTION_SCALAR = .65

# the probability that when it is chosen to move or copy a connection, that the connection will be from an in node
# to an out node
# chance to copy/move from an inner node = 1 - COPY_CONNECTION_FROM_IN_CHANCE
COPY_CONNECTION_FROM_IN_CHANCE = .4

# the initial number of chances a connection can be made during a mutation
# this number is multiplied by the current mutability to determine the actual number of chances the NeuralNet has of
# gaining or removing a connection
CONNECTION_CHANCES = 5

# the minimum amount of connections that have a chance to be added or removed during a mutation
MIN_CONNECTION_CHANCE = 1

# the initial probabiliy for each chance to add or remove a connection will succeed
# the current mutability of the NeuralNet decreases or increases this probaility
# based on what percentage of MAX_MUTABILITY the current mutability is
CONNECTION_SCALAR = .8

# the probability for a connection to be added rather than removed when a connection is either added or removed
# 1 - ADD_CONNECTION_PROBABILITY = probability of a connection being removed
ADD_CONNECTION_PROBABILITY = .7


# simulation variables

# True to make the game use the list of seeds specified in SET_SEED_GAMES to test each NeuralNet
# False to make the game randomly pick seeds which will happen RANDOM_SEED_GAMES times
# the average fitness of the NeuralNet from each seed played is the final fitness used to rank the NeuralNet
SET_SEED = False

# True if the inputs should be based on the number of tiles in 8 directions each tile on a tetris piece is
# False if inputs should be based on if each tile is filled, empty, or has the current piece in it
DISTANCE_INPUTS = False

# True to make the neural nets inputs relative to the position of the piece. This means that every time the center of
# the curent piece moves, so does the positions where the neural net's inputs come from
# False to make the neural ent inputs always come from the same tile in the grid
RELATIVE_NEURAL_INPUTS = False

# True to make the neural network have 2 sets of input grids, one for if each piece has a placed down tile, and one for
#   if the curretnly controlled piece is in the grid
# False to make it just one grid, using 1, 0, and -1 for filled, empty, and current pieces respectively
SPLIT_NEURAL_INPUTS = False

# these values are the width and height of the neural net's possible inputs when RELATIVE_NEURAL_INPUTS = True
# Larger values give the neural net a wider view of the grid, but also increase computation time
# never make these values less than GRID_WIDTH and GRID_HEIGHY respectively
# making these values larger than GRID_WIDTH * 2 and GRID_HEIGHT * 2 respectively won't add more information to the net
# TODO currently anyhting but GRID_WIDTH * 2.0 and GRID_HEIGHT * 2.0 don't work
RELATIVE_INPUT_WIDTH = int(GRID_WIDTH * 2.0)
RELATIVE_INPUT_HEIGHT = int(GRID_HEIGHT * 2.0)

# the seeds used to test a NeuralNet when the games use a set seed
# more games means more computation time
# only applies when SET_SEED = True
SET_SEED_GAMES = [1, 3, 5]

# the number of games used to test a neural net when a random seed is used
# more games means more computation time
# only applies when SET_SEED = False
RANDOM_SEED_GAMES = 10

# The repeating sequence of peices to use by all Tetris games
# Leave empty to use seed settings
# Use tuples with the first number to define which pieces are which, using these numbers, and the second number the
# number of times it is rotated
# like (2, 1) would be a T shaped peice rotaetd forwards 1 time
# 0:
# OO
# OO
# 1:
# OOOO
# 2:
# OOO
#  O
# 3:
# OOO
#   O
# 4:
# OOO
# O
# 5:
# OO
#  OO
# 6:
#  OO
# OO
PIECE_SEQUENCE = []

# When testing at least 3 seeds to calculate fitness of one NeuralNet, remove this percentage of the lowest socres
# and the highest scores.
# This essentially removes outliers.
# Set to 0 to remove none
# keep this value less than .5
# one fitness score will always be recorded
REMOVE_OUTLIER_FITNESS = .3

# Only used when REMOVE_OUTLIER_FITNESS is not 0
# 0: change nothing, remove the lowest and highest percentage of seeds
# 1: only use that lower percentage of seeds, so the lowest scoring seeds are aveeraged
# 2: only use that higher percentage of seeds, so the highest scoring seeds are aveeraged
REMOVE_FITNESS_TYPE = 1

# True if the percentage of the grid which is filled in should be taken into acount when adding fitness,
# False for the percentage of the filled grid to have no effect on the fitness
# When true, every time a piece is going to be placed down, the fitness that would otherwise be gained is then
# multiplied by the percentage of the grid that is empty. This means that the more clear the grid is, the more fitness
# that is gained for that piece placed down
USE_FILLED_FOR_FITNESS = True

# The number of moves a NeuralNet can try to make before it advances to the next line.
# A move happens each time the nural net calculates its outputs. It calculates which buttons should be held down,
# moves based on those buttons, then recalculates which buttons should be held down, and so on NUMBER_NET_MOVES times
# after making all its moves, it advances to the next row
# keep this value > 0, if it is 0, the NeuralNet will not do anything
# if this value is low, the NeuralNet will be able to perform very few actions before advacing to the next row
# if this value is too high, the NeuralNet will take a very long time performing any kind of task
# a value of 10 generally works well
NUMBER_NET_MOVES = 10

# the base amount of fitness gained from placing a piece down
# the actual fitness gained is FITNESS_PIECE / (2^(rows from bottom of grid))
FITNESS_PIECE = 1

# the base amount of fitness gained from removing a row
# the actual fitness gained is FITNESS_LINE * (percent of the way to the bottom of the grid)
FITNESS_LINE = 2

# the amount that fitness is multiplied by at the end of the game
# this has no effect on ranking of NeuralNets, but it can make the numbers easier to look at
# set to 0 to both have no scalar and to make the final fitness score not multiplied by the percentage of the board
# filled at the end of the game
# 5 generally gives readable values
FITNESS_SCALAR = 0

# the rate at which the neural net makes moves, 0 for fastest possible updating, and higher numbers to make the
# neural net play slower
# this only effects the playback simulation, not the games during evolution
DISP_REFRESH_RATE = 0

# The maximum number of rows a neural net can make before the game ends in a simulation
# this only effects evolution, not playback
# this is to prevent a simulation from going on forever if a NeuralNet ever learns how to play flawlessly
# Though that is only really a problem if the game is set to only use 4x1 peices or some other simple pattern
MAX_ROWS = 500

# the percentage of the best performers that will be replaced by worse performers
# use 0.0 to make exactly the top 50% survive every time
# use 1.0 to make every one of the top 50% get replaced
# generally this value should never exceed 0.9, which would be 90% of the top performers are replaced
# it also makes very little sense for this value to exceed 0.5
# the top performer of each generation is never removed
PERCENT_BEST_REMOVE = 0.15


# graphical options

# True if the parts of the tkiner Gui, the sim buttons, the labels, and so on, should adjust to the size of the window
# false if they should remain a constant size, this is less laggy, but for smaller moniters this may need to be set
# to true
# ALWAYS KEEP THIS VALUE AT True
STICKY_GUI = True

# The size of font used in the button Gui, not the game and neural net display Gui
# This only effects the sim buttons, use small values when using high values for NUM_BRAINS
FONT_SIZE = 1

# the number of columns in the sim grid of buttons for slecting a brain, use larger numbers along with
# smaller FONT_SIZE when using large NUM_BRAINS values
NUM_BUTTON_COL = 30


# fileWriter: an opened fileWriter in write mode
# this should print all of the settings to the text file of that writer
def save(fileWriter):
    fileWriter.write('\n')
    fileWriter.write('GridWidth: ' + str(GRID_WIDTH) + '\n')
    fileWriter.write('GridHeight: ' + str(GRID_HEIGHT) + '\n')
    fileWriter.write('GridX: ' + str(GRID_X) + '\n')
    fileWriter.write('GridY: ' + str(GRID_Y) + '\n')
    fileWriter.write('SquareSize: ' + str(SQUARE_SIZE) + '\n')
    fileWriter.write('GridSize: ' + str(GRID_SIZE) + '\n')
    fileWriter.write('GridLine: ' + str(GRID_LINE) + '\n')
    fileWriter.write('\n')
    fileWriter.write('NumBrains: ' + str(NUM_BRAINS) + '\n')
    fileWriter.write('MaxMutability: ' + str(MAX_MUTABILITY) + '\n')
    fileWriter.write('WeightBiasScalar: ' + str(WEIGHT_BIAS_SCALAR) + '\n')
    fileWriter.write('MutabilityChange: ' + str(MUTABILITY_CHANGE) + '\n')
    fileWriter.write('StartConnections: ' + str(START_CONNECTIONS) + '\n')
    fileWriter.write('RemoveNodeScalar: ' + str(REMOVE_NODE_SCALAR) + '\n')
    fileWriter.write('AddNodeChances: ' + str(ADD_NODE_CHANCES) + '\n')
    fileWriter.write('MinAddNodeChance: ' + str(MIN_ADD_NODE_CHANCE) + '\n')
    fileWriter.write('AddNodeScalar: ' + str(ADD_NODE_SCALAR) + '\n')
    fileWriter.write('AddNodeToOuterChance: ' + str(ADD_NODE_TO_OUTER_CHANCE) + '\n')
    fileWriter.write('CopyConnectionChances: ' + str(COPY_CONNECTION_CHANCES) + '\n')
    fileWriter.write('MinCopyConnectionChance: ' + str(MIN_COPY_CONNECTION_CHANCE) + '\n')
    fileWriter.write('CopyConnectionScalar: ' + str(COPY_CONNECTION_SCALAR) + '\n')
    fileWriter.write('CopyConnectionFromInChance: ' + str(COPY_CONNECTION_FROM_IN_CHANCE) + '\n')
    fileWriter.write('ConnectionChances: ' + str(CONNECTION_CHANCES) + '\n')
    fileWriter.write('MinConnectionChance: ' + str(MIN_CONNECTION_CHANCE) + '\n')
    fileWriter.write('ConnectionScalar: ' + str(CONNECTION_SCALAR) + '\n')
    fileWriter.write('AddConnectionProbability: ' + str(ADD_CONNECTION_PROBABILITY) + '\n')
    fileWriter.write('\n')
    fileWriter.write('SetSeed: ' + str(SET_SEED) + '\n')
    fileWriter.write('DistanceInputs: ' + str(DISTANCE_INPUTS) + '\n')
    fileWriter.write('RelativeNeuralInputs: ' + str(RELATIVE_NEURAL_INPUTS) + '\n')
    fileWriter.write('SplitNeuralInputs: ' + str(SPLIT_NEURAL_INPUTS) + '\n')
    fileWriter.write('RelativeInputWidth: ' + str(RELATIVE_INPUT_WIDTH) + '\n')
    fileWriter.write('RelativeInputHeight: ' + str(RELATIVE_INPUT_HEIGHT) + '\n')
    s = str(len(SET_SEED_GAMES)) + ','
    for i in SET_SEED_GAMES:
        s += str(i) + ','
    fileWriter.write('SetSeedGames: ' + s + '\n')
    fileWriter.write('RandomSeedGames: ' + str(RANDOM_SEED_GAMES) + '\n')
    fileWriter.write('PieceSequenceIds:\n')
    s = ''
    for i in PIECE_SEQUENCE:
        s += str(i[0]) + ' '
    fileWriter.write(s + '\n')
    fileWriter.write('PieceSequenceRotate:\n')
    s = ''
    for i in PIECE_SEQUENCE:
        s += str(i[1]) + ' '
    fileWriter.write(s + '\n')
    fileWriter.write('RemoveOutlierFitness: ' + str(REMOVE_OUTLIER_FITNESS) + '\n')
    fileWriter.write('RemoveFitnessType: ' + str(REMOVE_FITNESS_TYPE) + '\n')
    fileWriter.write('UseFilledForFitness: ' + str(USE_FILLED_FOR_FITNESS) + '\n')
    fileWriter.write('NumberNetMoves: ' + str(NUMBER_NET_MOVES) + '\n')
    fileWriter.write('FitnessPiece: ' + str(FITNESS_PIECE) + '\n')
    fileWriter.write('FitnessLine: ' + str(FITNESS_LINE) + '\n')
    fileWriter.write('FitnessScalar: ' + str(FITNESS_SCALAR) + '\n')
    fileWriter.write('DispRefreshRate: ' + str(DISP_REFRESH_RATE) + '\n')
    fileWriter.write('MaxRows: ' + str(MAX_ROWS) + '\n')
    fileWriter.write('PercentBestRemove: ' + str(PERCENT_BEST_REMOVE) + '\n')
    fileWriter.write('\n')
    fileWriter.write('StickyGui: ' + str(STICKY_GUI) + '\n')
    fileWriter.write('FontSize: ' + str(FONT_SIZE) + '\n')
    fileWriter.write('NumButtonCol: ' + str(NUM_BUTTON_COL) + '\n')


# fileWriter: an opened fileReader in read mode
# this should load in all the settings from the given file reader
# the file must be at a valid line to load in the settings
def load(fileReader):
    SaveLoader.loadSettings(fileReader)


try:
    with open('settings.txt', 'r') as f:
        load(f)
except FileNotFoundError and ValueError:
    SaveLoader.loadDefaultSettings()
    with open('settings.txt', 'w') as f:
        save(f)
