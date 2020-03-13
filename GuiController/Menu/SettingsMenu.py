from tkinter import *

from GuiController.Menu import Menu
from GuiController.Menu.InitMenu import InitMenu
from GuiController.Graph import GraphHandler

from TetrisGame import Tetris

import Settings

import ast
import functools


class SettingsMenu(Menu.Menu):

    def __init__(self, centralHandler, settingsGui):
        super().__init__(settingsGui, centralHandler.settingsGui)
        self.centralHandler = centralHandler

        self.descriptionLabel = None

        # Text fields for settings that can be changed at any time
        self.gridXText = None
        self.gridYText = None
        self.squareSizeText = None
        self.gridSizeText = None
        self.gridLineText = None
        self.maxMutabilityText = None
        self.weightBiasScalarText = None
        self.mutabilityChangeText = None
        self.removeNodeScalarText = None
        self.addNodeChancesText = None
        self.minAddNodeChanceText = None
        self.addNodeScalarText = None
        self.addNodeToOuterChanceText = None
        self.copyConnectionChancesText = None
        self.minCopyConnectionChancesText = None
        self.copyConnectionScalarText = None
        self.copyConnectionFromInChanceText = None
        self.connectionChancesText = None
        self.minConnectionChancesText = None
        self.connectionScalarText = None
        self.addConnectionProbabilityText = None
        self.setSeedText = None
        self.setSeedGamesText = None
        self.randomSeedGamesText = None
        self.pieceSequenceText = None
        self.removeOutlierFitnessText = None
        self.removeFitnessTypeText = None
        self.useFilledForFitnessText = None
        self.numberNetMovesText = None
        self.fitnessPieceText = None
        self.fitnessLineText = None
        self.fitnessScalarText = None
        self.dispRefreshRateText = None
        self.maxRowsText = None
        self.percentBestRemoveText = None
        self.fontSizeText = None
        self.numButtonColText = None

        # Text fields for settings that only effetc the start
        self.gridWidthText = None
        self.gridHeightText = None
        self.numBrainsText = None
        self.distanceInputsText = None
        self.relativeNeuralInputsText = None
        self.splitNeuralInputsText = None

        self.descriptions = [
            "X coordinate of the Tetris game location.",

            "Y coordinate of the Tetris game location.",

            "Size of a square in the neural net display.",

            "Size of a square in the main game display.",

            "The thickness of the lines in the main\n"
            "Tetris game display.",

            "The maximum that the absolute value of\n"
            "  mutability can be.\n"
            "Mutability governs the rate at which all\n"
            "  mutations occur which, during a\n"
            "  mutation, determines:\n"
            " - How much a node weight or bias can go up\n"
            "   or down\n"
            " - The number of inner nodes that can be\n"
            "   removed or added\n"
            " - The number of connections that can be\n"
            "   removed or added\n"
            " - The chance of any particular node or\n"
            "   connection to be removed or added\n"
            "Keep this value to positive\n"
            "  numbers only.\n"
            "Generally should be kept to values < 10\n"
            "  depending on other scalars.",

            "This value is multiplied the random value\n"
            "  added to connection weights and biases\n"
            "  during mutations.",

            "The maximum amount added to mutability\n"
            "  during a mutation. Set to a negative\n"
            "  value to pick a new random mutability\n"
            "  during a mutation.",

            "The initial probability for attempts to\n"
            "  remove a node to succeed.",

            "The maximum number of chances for a\n"
            "  node to be added.",

            "The minimum number of chances for a node\n"
            "  to be added.",

            "The initial probability for attempts to\n"
            "  add a node to succeed.",

            "When an innter node is added, the\n"
            "  probability that it will split up\n"
            "  a connection to an output node,\n"
            "  rather than to an inner node.",

            "The maximum number of chances for a\n"
            "  connection to be coppied or moved to\n"
            "  a nearby node.",

            "The minimum number of chances for a\n"
            "  connection to be coppied or moved to a\n"
            "  nearby node",

            "The initital probability for attempts\n"
            "  to copy or move a connection to succeed.",

            "When a connection is moved or coppied,\n"
            "  the probability that it will be an input\n"
            "  node to an output node, rather than an\n"
            "  inner node.",

            "The maximum number of chances for a\n"
            "  connection to be added or removed.",

            "The minimum number of chances for a\n"
            "  connection to be sdded or removed.",

            "The initial probability for attempts to\n"
            "  add connections to succeed.",

            "When a connection will be added or\n"
            "  removed, the probability that it will\n"
            "  be added, rather than removed.",

            "True if the list of seeds in, set seed\n"
            "  games, should be used as seeds for\n"
            "  which pieces are generated.\n"
            "False if a random seed should be\n"
            "  picked, random seed games, number of\n"
            "  times.\n"
            "The average fitness from each game\n"
            "  played determines the overall fitness\n"
            "  of the neural network.",

            "The list of seeds to use when using\n"
            "  a set seed.\n"
            "Must be in [] and each seed must be\n"
            "  seperated by a comma.\n"
            "All seeds should be integers.\n"
            "Examples: [1], [3, 5, 7], [324, 7]",

            "The number of random seeds to use when\n"
            "  not using a set seed.",

            "A repeating sequence of pices to use for\n"
            "  all Tetris games.\n"
            "Leave the list empty to not use a set\n"
            "  piece sequence.\n"
            "Each entry in the list should be in []\n"
            "  seperate by a comma.\n"
            "Each entry should have 2 integers in ()\n"
            "  seperated by a comma.\n"
            "The first integer is 0-6 for the id of the\n"
            "  specific piece.\n"
            "The second integer is the number of times\n"
            "  the tile is rotated.\n"
            "Ids: 0: square, 1: line, 2: T piece,\n"
            "  3: backwards L, 4: normal L,\n"
            "  5: Z piece, 6: S piece\n"
            "Examples: [], [(1, 2)], [(0, 1), (2, 6)],\n"
            "  [(1, 2), (6, 0), (0, 2)]",

            "When at least 2 seeds are used for average\n"
            "  fitness, the percentage of the highest and\n"
            "  lowest scores from each set of games of\n"
            "  each neural network that will be removed.\n"
            "Set to 0 to remove no fitness scores.",

            "The way that fitness scores will be removed\n"
            "  when, remove outlier fitness, is not\n"
            "  set to 0.\n"
            "The amount of fitness scores removed is\n"
            "  based on, remove outlier fitness.\n"
            "0: Remove both the highest and lowest\n"
            "  scores before averaging.\n"
            "1: Use only the lowest average scores.\n"
            "2: Use only the highest average scores.",

            "True if the percentage of the filled grid\n"
            "  should effect fitness when added.\n"
            "False if the percentage should have no\n"
            "  effect.\n"
            "When true, the more filled in the grid is,\n"
            "  the less fitness is gained.",

            "The number of moves a neural network can\n"
            "  make before it advances ot the next line.\n"
            "A move is 1 rotation of a piece or one\n"
            "  movement left or right.\n"
            "Generally 10 works well for allowing\n"
            "  functionality while preventing lag.",

            "The initial amount of fitness gained when a\n"
            "  piece is placed down.",

            "The initial amount of fitness gained when a\n"
            "  line is removed.",

            "This value is added to the fitness at\n"
            "  the end of a game, based on the filled\n"
            "  percetage of the board.\n"
            "Set to 0 to not add anything to the\n"
            "  final fitness.",

            "The time between moves when watching the\n"
            "  neural net play.\n"
            "Only effects playback, not the simulation\n"
            "  runtime.\n"
            "Set to 0 to playback as fast as possible.",

            "The maximum number of rows a neural\n"
            "network can get before the game ends\n"
            "  while a generation is tested.\n",

            "The percentage of the higher performing\n"
            "  neural networks that will be replaced \n"
            "  by lower performing networks.\n"
            "This means that any neural net can be\n"
            "  removed from the list in a generation,\n"
            "  not always the lowest 50%\n"
            "Set to 0.0 to always remove the lowest 50%\n"
            "  of the performers.\n"
            "Use 1.0 to replace every one of the to 50%\n"
            "  performers.",

            "The font size of the text on the buttons for\n"
            "  selecting neural networks to view.",

            "The number of neuralk nets on each row of\n"
            "  the main grid selection.",

            "The number of tiles in the width of a\n"
            "  tetris game, normally 10",

            "The number of tiles in the height of a\n"
            "  tetris game, normally 21",

            "The number of neural nets in a simulation.\n"
            "Must be an even integer > 0",

            "True if the inputs should be based on the\n"
            "  distance the currently controlled piece\n"
            "  is from nearby filled in tiles and walls.\n"
            "False if they should be based on the state\n"
            "  of each tile in the grid.",

            "Only does anything when Distance Inputs\n"
            "   is set to False\n"
            "True if the inputs for game tiles should\n"
            "  be based on their relative positions to\n"
            "  the currenly controlled piece.\n"
            "False if every tile should always give to\n"
            "  the same input.",

            "True to use 2 sets of neural inputs. One\n"
            "for pieces placed down, and one for\n"
            "currently controlled peices.\n"
            "False use one grid."
        ]

        # a list of bool determining which of the settings for a new sim are valid
        self.validSettings = [True, True, True, True, True, True]

    def resetMenu(self):
        super().resetMenu()
        self.window.configure(bg="#FFFFFF")
        self.frame.configure(padx=20, pady=20)

        # creating a frame for the settings text labels, these are the settings that can be changed during a simulation
        settingsFrame = Frame(self.frame, bg="#FFFFFF")
        settingsFrame.pack_propagate(0)
        settingsFrame.grid(column=0, row=0)

        # creating a title for settings
        titleLabel = Label(settingsFrame, text="Settings")
        titleLabel.configure(font=('Impact', 20), bg="#FFFFFF")
        titleLabel.grid(column=0, row=0, pady=2, padx=5, columnspan=2, sticky=N + S + E + W)

        # Add a label for displaying the desciprion of the hovered setting
        self.descriptionLabel = Label(self.frame, text="\t")
        self.descriptionLabel.configure(font=('Impact', 15), bg="#FFFFFF", width=35, anchor="w", justify="left")
        self.descriptionLabel.grid(column=1, row=0, pady=10, padx=5, sticky=N + S + E + W)

        # text inputs for settings
        makeSettingsLabel("Grid X: ", 1, settingsFrame)
        self.gridXText = makeSettingsText(1, settingsFrame)
        self.gridXText.insert(END, str(Settings.GRID_X))
        self.gridXText.bind('<KeyRelease>', self.gridXTextChange)
        self.gridXText.bind('<Enter>', functools.partial(self.setDescription, 0))
        self.gridXText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Grid Y: ", 2, settingsFrame)
        self.gridYText = makeSettingsText(2, settingsFrame)
        self.gridYText.insert(END, str(Settings.GRID_Y))
        self.gridYText.bind('<KeyRelease>', self.gridYTextChange)
        self.gridYText.bind('<Enter>', functools.partial(self.setDescription, 1))
        self.gridYText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Square Size: ", 3, settingsFrame)
        self.squareSizeText = makeSettingsText(3, settingsFrame)
        self.squareSizeText.insert(END, str(Settings.SQUARE_SIZE))
        self.squareSizeText.bind('<KeyRelease>', self.squareSizeTextChange)
        self.squareSizeText.bind('<Enter>', functools.partial(self.setDescription, 2))
        self.squareSizeText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Grid Size: ", 4, settingsFrame)
        self.gridSizeText = makeSettingsText(4, settingsFrame)
        self.gridSizeText.insert(END, str(Settings.GRID_SIZE))
        self.gridSizeText.bind('<KeyRelease>', self.gridSizeTextChange)
        self.gridSizeText.bind('<Enter>', functools.partial(self.setDescription, 3))
        self.gridSizeText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Grid Line: ", 5, settingsFrame)
        self.gridLineText = makeSettingsText(5, settingsFrame)
        self.gridLineText.insert(END, str(Settings.GRID_LINE))
        self.gridLineText.bind('<KeyRelease>', self.gridLineTextChange)
        self.gridLineText.bind('<Enter>', functools.partial(self.setDescription, 4))
        self.gridLineText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Max Mutability: ", 6, settingsFrame)
        self.maxMutabilityText = makeSettingsText(6, settingsFrame)
        self.maxMutabilityText.insert(END, str(Settings.MAX_MUTABILITY))
        self.maxMutabilityText.bind('<KeyRelease>', self.maxMutabilityTextChange)
        self.maxMutabilityText.bind('<Enter>', functools.partial(self.setDescription, 5))
        self.maxMutabilityText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Weight Bias Scalar: ", 7, settingsFrame)
        self.weightBiasScalarText = makeSettingsText(7, settingsFrame)
        self.weightBiasScalarText.insert(END, str(Settings.WEIGHT_BIAS_SCALAR))
        self.weightBiasScalarText.bind('<KeyRelease>', self.weightBiasScalarTextChange)
        self.weightBiasScalarText.bind('<Enter>', functools.partial(self.setDescription, 6))
        self.weightBiasScalarText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Mutability Change: ", 8, settingsFrame)
        self.mutabilityChangeText = makeSettingsText(8, settingsFrame)
        self.mutabilityChangeText.insert(END, str(Settings.MUTABILITY_CHANGE))
        self.mutabilityChangeText.bind('<KeyRelease>', self.mutabilityChangeTextChange)
        self.mutabilityChangeText.bind('<Enter>', functools.partial(self.setDescription, 7))
        self.mutabilityChangeText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Remove Node Scalar: ", 9, settingsFrame)
        self.removeNodeScalarText = makeSettingsText(9, settingsFrame)
        self.removeNodeScalarText.insert(END, str(Settings.REMOVE_NODE_SCALAR))
        self.removeNodeScalarText.bind('<KeyRelease>', self.removeNodeScalarTextChange)
        self.removeNodeScalarText.bind('<Enter>', functools.partial(self.setDescription, 8))
        self.removeNodeScalarText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Add Node Chances: ", 10, settingsFrame)
        self.addNodeChancesText = makeSettingsText(10, settingsFrame)
        self.addNodeChancesText.insert(END, str(Settings.ADD_NODE_CHANCES))
        self.addNodeChancesText.bind('<KeyRelease>', self.addNodeChancesTextChange)
        self.addNodeChancesText.bind('<Enter>', functools.partial(self.setDescription, 9))
        self.addNodeChancesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Min Add Node Chance: ", 11, settingsFrame)
        self.minAddNodeChanceText = makeSettingsText(11, settingsFrame)
        self.minAddNodeChanceText.insert(END, str(Settings.MIN_ADD_NODE_CHANCE))
        self.minAddNodeChanceText.bind('<KeyRelease>', self.minAddNodeChanceTextChange)
        self.minAddNodeChanceText.bind('<Enter>', functools.partial(self.setDescription, 10))
        self.minAddNodeChanceText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Add Node Scalar: ", 12, settingsFrame)
        self.addNodeScalarText = makeSettingsText(12, settingsFrame)
        self.addNodeScalarText.insert(END, str(Settings.ADD_NODE_SCALAR))
        self.addNodeScalarText.bind('<KeyRelease>', self.addNodeScalarTextChange)
        self.addNodeScalarText.bind('<Enter>', functools.partial(self.setDescription, 11))
        self.addNodeScalarText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Add Node to Outer Chance: ", 13, settingsFrame)
        self.addNodeToOuterChanceText = makeSettingsText(13, settingsFrame)
        self.addNodeToOuterChanceText.insert(END, str(Settings.ADD_NODE_TO_OUTER_CHANCE))
        self.addNodeToOuterChanceText.bind('<KeyRelease>', self.addNodeToOuterChanceTextChange)
        self.addNodeToOuterChanceText.bind('<Enter>', functools.partial(self.setDescription, 12))
        self.addNodeToOuterChanceText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Copy Connection Chances: ", 13, settingsFrame)
        self.copyConnectionChancesText = makeSettingsText(13, settingsFrame)
        self.copyConnectionChancesText.insert(END, str(Settings.COPY_CONNECTION_CHANCES))
        self.copyConnectionChancesText.bind('<KeyRelease>', self.copyConnectionChancesTextChange)
        self.copyConnectionChancesText.bind('<Enter>', functools.partial(self.setDescription, 13))
        self.copyConnectionChancesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Min Copy Connection Chances: ", 13, settingsFrame)
        self.minCopyConnectionChancesText = makeSettingsText(13, settingsFrame)
        self.minCopyConnectionChancesText.insert(END, str(Settings.MIN_COPY_CONNECTION_CHANCE))
        self.minCopyConnectionChancesText.bind('<KeyRelease>', self.minCopyConnectionChancesTextChange)
        self.minCopyConnectionChancesText.bind('<Enter>', functools.partial(self.setDescription, 14))
        self.minCopyConnectionChancesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Copy Connection Scalar: ", 14, settingsFrame)
        self.copyConnectionScalarText = makeSettingsText(14, settingsFrame)
        self.copyConnectionScalarText.insert(END, str(Settings.COPY_CONNECTION_SCALAR))
        self.copyConnectionScalarText.bind('<KeyRelease>', self.copyConnectionScalarTextChange)
        self.copyConnectionScalarText.bind('<Enter>', functools.partial(self.setDescription, 15))
        self.copyConnectionScalarText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Copy Connection From In Chance: ", 15, settingsFrame)
        self.copyConnectionFromInChanceText = makeSettingsText(15, settingsFrame)
        self.copyConnectionFromInChanceText.insert(END, str(Settings.COPY_CONNECTION_FROM_IN_CHANCE))
        self.copyConnectionFromInChanceText.bind('<KeyRelease>', self.copyConnectionFromInChanceTextChange)
        self.copyConnectionFromInChanceText.bind('<Enter>', functools.partial(self.setDescription, 16))
        self.copyConnectionFromInChanceText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Connection Chances: ", 16, settingsFrame)
        self.connectionChancesText = makeSettingsText(16, settingsFrame)
        self.connectionChancesText.insert(END, str(Settings.CONNECTION_CHANCES))
        self.connectionChancesText.bind('<KeyRelease>', self.connectionChancesTextChange)
        self.connectionChancesText.bind('<Enter>', functools.partial(self.setDescription, 17))
        self.connectionChancesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Min Connection Chances: ", 17, settingsFrame)
        self.minConnectionChancesText = makeSettingsText(17, settingsFrame)
        self.minConnectionChancesText.insert(END, str(Settings.MIN_CONNECTION_CHANCE))
        self.minConnectionChancesText.bind('<KeyRelease>', self.minConnectionChancesTextChange)
        self.minConnectionChancesText.bind('<Enter>', functools.partial(self.setDescription, 18))
        self.minConnectionChancesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Connection Scalar: ", 18, settingsFrame)
        self.connectionScalarText = makeSettingsText(18, settingsFrame)
        self.connectionScalarText.insert(END, str(Settings.CONNECTION_SCALAR))
        self.connectionScalarText.bind('<KeyRelease>', self.connectionScalarTextChange)
        self.connectionScalarText.bind('<Enter>', functools.partial(self.setDescription, 19))
        self.connectionScalarText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Add Connection Probability: ", 19, settingsFrame)
        self.addConnectionProbabilityText = makeSettingsText(19, settingsFrame)
        self.addConnectionProbabilityText.insert(END, str(Settings.ADD_CONNECTION_PROBABILITY))
        self.addConnectionProbabilityText.bind('<KeyRelease>', self.addConnectionProbabilityTextChange)
        self.addConnectionProbabilityText.bind('<Enter>', functools.partial(self.setDescription, 20))
        self.addConnectionProbabilityText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Set Seed: ", 20, settingsFrame)
        self.setSeedText = makeSettingsText(20, settingsFrame)
        self.setSeedText.insert(END, str(Settings.SET_SEED))
        self.setSeedText.bind('<KeyRelease>', self.setSeedTextChange)
        self.setSeedText.bind('<Enter>', functools.partial(self.setDescription, 21))
        self.setSeedText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Set Seed Games: ", 21, settingsFrame)
        self.setSeedGamesText = makeSettingsText(21, settingsFrame)
        self.setSeedGamesText.insert(END, str(Settings.SET_SEED_GAMES))
        self.setSeedGamesText.bind('<KeyRelease>', self.setSeedGamesTextChange)
        self.setSeedGamesText.bind('<Enter>', functools.partial(self.setDescription, 22))
        self.setSeedGamesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Random Seed Games: ", 22, settingsFrame)
        self.randomSeedGamesText = makeSettingsText(22, settingsFrame)
        self.randomSeedGamesText.insert(END, str(Settings.RANDOM_SEED_GAMES))
        self.randomSeedGamesText.bind('<KeyRelease>', self.randomSeedGamesTextChange)
        self.randomSeedGamesText.bind('<Enter>', functools.partial(self.setDescription, 23))
        self.randomSeedGamesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Piece Sequence: ", 23, settingsFrame)
        self.pieceSequenceText = makeSettingsText(23, settingsFrame)
        self.pieceSequenceText.insert(END, str(Settings.PIECE_SEQUENCE))
        self.pieceSequenceText.bind('<KeyRelease>', self.pieceSequenceTextChange)
        self.pieceSequenceText.bind('<Enter>', functools.partial(self.setDescription, 24))
        self.pieceSequenceText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Remove Outlier Fitness: ", 24, settingsFrame)
        self.removeOutlierFitnessText = makeSettingsText(24, settingsFrame)
        self.removeOutlierFitnessText.insert(END, str(Settings.REMOVE_OUTLIER_FITNESS))
        self.removeOutlierFitnessText.bind('<KeyRelease>', self.removeOutlierFitnessTextChange)
        self.removeOutlierFitnessText.bind('<Enter>', functools.partial(self.setDescription, 25))
        self.removeOutlierFitnessText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Remove Fitness Type: ", 25, settingsFrame)
        self.removeFitnessTypeText = makeSettingsText(25, settingsFrame)
        self.removeFitnessTypeText.insert(END, str(Settings.REMOVE_FITNESS_TYPE))
        self.removeFitnessTypeText.bind('<KeyRelease>', self.removeFitnessTypeLabelTextChange)
        self.removeFitnessTypeText.bind('<Enter>', functools.partial(self.setDescription, 26))
        self.removeFitnessTypeText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Use Filled For Fitness: ", 26, settingsFrame)
        self.useFilledForFitnessText = makeSettingsText(26, settingsFrame)
        self.useFilledForFitnessText.insert(END, str(Settings.USE_FILLED_FOR_FITNESS))
        self.useFilledForFitnessText.bind('<KeyRelease>', self.useFilledForFitnessTextChange)
        self.useFilledForFitnessText.bind('<Enter>', functools.partial(self.setDescription, 27))
        self.useFilledForFitnessText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Number Net Moves: ", 27, settingsFrame)
        self.numberNetMovesText = makeSettingsText(27, settingsFrame)
        self.numberNetMovesText.insert(END, str(Settings.NUMBER_NET_MOVES))
        self.numberNetMovesText.bind('<KeyRelease>', self.numberNetMovesTextChange)
        self.numberNetMovesText.bind('<Enter>', functools.partial(self.setDescription, 28))
        self.numberNetMovesText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Fitness Piece: ", 28, settingsFrame)
        self.fitnessPieceText = makeSettingsText(28, settingsFrame)
        self.fitnessPieceText.insert(END, str(Settings.FITNESS_PIECE))
        self.fitnessPieceText.bind('<KeyRelease>', self.fitnessPieceTextChange)
        self.fitnessPieceText.bind('<Enter>', functools.partial(self.setDescription, 29))
        self.fitnessPieceText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Fitness Line: ", 29, settingsFrame)
        self.fitnessLineText = makeSettingsText(29, settingsFrame)
        self.fitnessLineText.insert(END, str(Settings.FITNESS_LINE))
        self.fitnessLineText.bind('<KeyRelease>', self.fitnessLineTextChange)
        self.fitnessLineText.bind('<Enter>', functools.partial(self.setDescription, 30))
        self.fitnessLineText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Fitness Scalar: ", 30, settingsFrame)
        self.fitnessScalarText = makeSettingsText(30, settingsFrame)
        self.fitnessScalarText.insert(END, str(Settings.FITNESS_SCALAR))
        self.fitnessScalarText.bind('<KeyRelease>', self.fitnessScalarTextChange)
        self.fitnessScalarText.bind('<Enter>', functools.partial(self.setDescription, 31))
        self.fitnessScalarText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Disp Refresh Rate: ", 31, settingsFrame)
        self.dispRefreshRateText = makeSettingsText(31, settingsFrame)
        self.dispRefreshRateText.insert(END, str(Settings.DISP_REFRESH_RATE))
        self.dispRefreshRateText.bind('<KeyRelease>', self.dispRefreshRateTextChange)
        self.dispRefreshRateText.bind('<Enter>', functools.partial(self.setDescription, 32))
        self.dispRefreshRateText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Max Rows: ", 32, settingsFrame)
        self.maxRowsText = makeSettingsText(32, settingsFrame)
        self.maxRowsText.insert(END, str(Settings.MAX_ROWS))
        self.maxRowsText.bind('<KeyRelease>', self.maxRowsTextChange)
        self.maxRowsText.bind('<Enter>', functools.partial(self.setDescription, 33))
        self.maxRowsText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Percent Best Remove: ", 33, settingsFrame)
        self.percentBestRemoveText = makeSettingsText(33, settingsFrame)
        self.percentBestRemoveText.insert(END, str(Settings.PERCENT_BEST_REMOVE))
        self.percentBestRemoveText.bind('<KeyRelease>', self.percentBestRemoveTextChange)
        self.percentBestRemoveText.bind('<Enter>', functools.partial(self.setDescription, 34))
        self.percentBestRemoveText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("fontSize: ", 34, settingsFrame)
        self.fontSizeText = makeSettingsText(34, settingsFrame)
        self.fontSizeText.insert(END, str(Settings.FONT_SIZE))
        self.fontSizeText.bind('<KeyRelease>', self.fontSizeTextChange)
        self.fontSizeText.bind('<Enter>', functools.partial(self.setDescription, 35))
        self.fontSizeText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Num Button Col: ", 35, settingsFrame)
        self.numButtonColText = makeSettingsText(35, settingsFrame)
        self.numButtonColText.insert(END, str(Settings.NUM_BUTTON_COL))
        self.numButtonColText.bind('<KeyRelease>', self.numButtonColTextChange)
        self.numButtonColText.bind('<Enter>', functools.partial(self.setDescription, 36))
        self.numButtonColText.bind('<Leave>', self.removeDescription)

        # creating a frame for the new sim settings text labels, these are the settings that can only be changed for a
        # new simulation
        newSimSettingsFrame = Frame(self.frame,  bg="#FFFFFF")
        newSimSettingsFrame.pack_propagate(0)
        newSimSettingsFrame.grid(column=2, row=0)

        # creating a title for settings
        newSimSettingsLabel = Label(newSimSettingsFrame, text="New Sim Settings\nThese settings only effect\nnew sims.")
        newSimSettingsLabel.configure(font=('Impact', 16), bg="#FFFFFF")
        newSimSettingsLabel.grid(column=0, row=0, pady=2, padx=5, columnspan=2, sticky=N + S + E + W)

        makeSettingsLabel("Grid Width: ", 1, newSimSettingsFrame)
        self.gridWidthText = makeSettingsText(1, newSimSettingsFrame)
        self.gridWidthText.insert(END, str(Settings.GRID_WIDTH))
        self.gridWidthText.bind('<KeyRelease>', self.gridWidthTextChange)
        self.gridWidthText.bind('<Enter>', functools.partial(self.setDescription, 37))
        self.gridWidthText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Grid Height: ", 2, newSimSettingsFrame)
        self.gridHeightText = makeSettingsText(2, newSimSettingsFrame)
        self.gridHeightText.insert(END, str(Settings.GRID_HEIGHT))
        self.gridHeightText.bind('<KeyRelease>', self.gridHeightTextChange)
        self.gridHeightText.bind('<Enter>', functools.partial(self.setDescription, 38))
        self.gridHeightText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Num Brains: ", 3, newSimSettingsFrame)
        self.numBrainsText = makeSettingsText(3, newSimSettingsFrame)
        self.numBrainsText.insert(END, str(Settings.NUM_BRAINS))
        self.numBrainsText.bind('<KeyRelease>', self.numBrainsTextChange)
        self.numBrainsText.bind('<Enter>', functools.partial(self.setDescription, 39))
        self.numBrainsText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Distance Inputs: ", 4, newSimSettingsFrame)
        self.distanceInputsText = makeSettingsText(4, newSimSettingsFrame)
        self.distanceInputsText.insert(END, str(Settings.DISTANCE_INPUTS))
        self.distanceInputsText.bind('<KeyRelease>', self.distanceInputsTextChange)
        self.distanceInputsText.bind('<Enter>', functools.partial(self.setDescription, 40))
        self.distanceInputsText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Relative Neural Inputs: ", 5, newSimSettingsFrame)
        self.relativeNeuralInputsText = makeSettingsText(5, newSimSettingsFrame)
        self.relativeNeuralInputsText.insert(END, str(Settings.RELATIVE_NEURAL_INPUTS))
        self.relativeNeuralInputsText.bind('<KeyRelease>', self.relativeNeuralInputsTextChange)
        self.relativeNeuralInputsText.bind('<Enter>', functools.partial(self.setDescription, 41))
        self.relativeNeuralInputsText.bind('<Leave>', self.removeDescription)

        makeSettingsLabel("Split Neural Inputs: ", 6, newSimSettingsFrame)
        self.splitNeuralInputsText = makeSettingsText(6, newSimSettingsFrame)
        self.splitNeuralInputsText.insert(END, str(Settings.SPLIT_NEURAL_INPUTS))
        self.splitNeuralInputsText.bind('<KeyRelease>', self.splitNeuralInputsTextChange)
        self.splitNeuralInputsText.bind('<Enter>', functools.partial(self.setDescription, 42))
        self.splitNeuralInputsText.bind('<Leave>', self.removeDescription)

        # creating a button for setting the main Tkinter GUI to the input menu
        goToInitMenuButton = Button(newSimSettingsFrame, text="Delete sim and\nGo to init menu", font=('Impact', 20),
                                    command=self.handleNewSimButtonPress)
        goToInitMenuButton.grid(column=0, row=7, columnspan=2, sticky=N + S + E + W)

        # creating a button that updates all the settings that can only be changed at the start
        updateNewSimSettingsButton = Button(newSimSettingsFrame, text="Update New Sim Settings", font=('Impact', 20),
                                            command=self.handleUpdateNewSimSettingsButtonPress)
        updateNewSimSettingsButton.grid(column=0, row=8, columnspan=2, sticky=N + S + E + W)

        # creating a button to save settings
        saveSettingsButton = Button(newSimSettingsFrame, text="Save Settings", font=('Impact', 20),
                                    command=self.handleSaveSettingsButtonPress)
        saveSettingsButton.grid(column=0, row=9, columnspan=2, sticky=N + S + E + W)

        for i in range(40):
            Grid.columnconfigure(settingsFrame, i, weight=1)
        for i in range(40):
            Grid.rowconfigure(settingsFrame, i, weight=1)

        for i in range(20):
            Grid.columnconfigure(self.frame, i, weight=1)
        for i in range(20):
            Grid.rowconfigure(self.frame, i, weight=1)

    def handleSaveSettingsButtonPress(self):
        if self.updateNewSimSettings():
            with open('settings.txt', 'w') as f:
                Settings.save(f)
        else:
            self.descriptionLabel.configure(text="Invalid New Sim Settings", fg="#AF0000")

    def handleNewSimButtonPress(self):
        self.updateNewSimSettings()

        window = self.centralHandler.simWindow
        gui = self.centralHandler.simGui
        gui.currentMenu.frame.destroy()
        s = InitMenu(gui, window, self.centralHandler)
        gui.setMenu(s)
        self.descriptionLabel.configure(text="")
        self.centralHandler.setGraphHandler(GraphHandler.GraphHandler(self.centralHandler))

    def handleUpdateNewSimSettingsButtonPress(self):
        self.descriptionLabel.configure(text="")
        self.updateNewSimSettings()

    def updateNewSimSettings(self):
        s = self.centralHandler.simGui.currentMenu
        if s is None or (s is not None and not isinstance(s, InitMenu)):
            self.descriptionLabel.configure(text="Cannot change these settings\nuntil sim is deleted", fg="#AF0000")
            return False

        for b in self.validSettings:
            if not b:
                self.descriptionLabel.configure(text="Invalid New Sim Settings", fg="#AF0000")
                return False

        Settings.GRID_WIDTH = int(self.gridWidthText.get("1.0", END))
        Settings.GRID_HEIGHT = int(self.gridHeightText.get("1.0", END))
        Settings.NUM_BRAINS = int(self.numBrainsText.get("1.0", END))
        Settings.DISTANCE_INPUTS = self.distanceInputsText.get("1.0", END)[0:-1] == "True"
        Settings.RELATIVE_NEURAL_INPUTS = self.relativeNeuralInputsText.get("1.0", END)[0:-1] == "True"
        Settings.SPLIT_NEURAL_INPUTS = self.splitNeuralInputsText.get("1.0", END)[0:-1] == "True"
        return True

    def setDescription(self, i, *args):
        self.descriptionLabel.configure(text=self.descriptions[i] + "\t", fg="#000000")

    def removeDescription(self, *args):
        self.descriptionLabel.configure(text="\t")

    def gridXTextChange(self, *args):
        try:
            val = int(self.gridXText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.gridXText)
            return

        if val < 0:
            updateSettingTextColor(True, self.gridXText)
            return

        Settings.GRID_X = val
        updateSettingTextColor(False, self.gridXText)

    def gridYTextChange(self, *args):
        try:
            val = int(self.gridYText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.gridYText)
            return

        if val < 0:
            updateSettingTextColor(True, self.gridYText)
            return

        Settings.GRID_Y = val
        updateSettingTextColor(False, self.gridYText)

    def squareSizeTextChange(self, *args):
        try:
            val = int(self.squareSizeText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.squareSizeText)
            return

        if val < 0:
            updateSettingTextColor(True, self.squareSizeText)
            return

        Settings.SQUARE_SIZE = val
        updateSettingTextColor(False, self.squareSizeText)

    def gridSizeTextChange(self, *args):
        try:
            val = int(self.gridSizeText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.gridSizeText)
            return

        if val < 0:
            updateSettingTextColor(True, self.gridSizeText)
            return

        Settings.GRID_SIZE = val
        updateSettingTextColor(False, self.gridSizeText)

    def gridLineTextChange(self, *args):
        try:
            val = int(self.gridLineText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.gridLineText)
            return

        if val < 0:
            updateSettingTextColor(True, self.gridLineText)
            return

        Settings.GRID_LINE = val
        updateSettingTextColor(False, self.gridLineText)

    def maxMutabilityTextChange(self, *args):
        try:
            val = float(self.maxMutabilityText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.maxMutabilityText)
            return

        Settings.MAX_MUTABILITY = val
        updateSettingTextColor(False, self.maxMutabilityText)

    def weightBiasScalarTextChange(self, *args):
        try:
            val = float(self.weightBiasScalarText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.weightBiasScalarText)
            return

        Settings.WEIGHT_BIAS_SCALAR = val
        updateSettingTextColor(False, self.weightBiasScalarText)

    def mutabilityChangeTextChange(self, *args):
        try:
            val = float(self.mutabilityChangeText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.mutabilityChangeText)
            return

        Settings.MUTABILITY_CHANGE = val
        updateSettingTextColor(False, self.mutabilityChangeText)

    def removeNodeScalarTextChange(self, *args):
        try:
            val = float(self.removeNodeScalarText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.removeNodeScalarText)
            return

        Settings.REMOVE_NODE_SCALAR = val
        updateSettingTextColor(False, self.removeNodeScalarText)

    def addNodeChancesTextChange(self, *args):
        try:
            val = int(self.addNodeChancesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.addNodeChancesText)
            return

        if val < 0:
            updateSettingTextColor(True, self.addNodeChancesText)
            return

        Settings.ADD_NODE_CHANCES = val
        updateSettingTextColor(False, self.addNodeChancesText)

    def minAddNodeChanceTextChange(self, *args):
        try:
            val = int(self.minAddNodeChanceText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.minAddNodeChanceText)
            return

        if val < 0:
            updateSettingTextColor(True, self.minAddNodeChanceText)
            return

        Settings.MIN_ADD_NODE_CHANCE = val
        updateSettingTextColor(False, self.minAddNodeChanceText)

    def addNodeScalarTextChange(self, *args):
        try:
            val = float(self.addNodeScalarText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.addNodeScalarText)
            return

        Settings.ADD_NODE_SCALAR = val
        updateSettingTextColor(False, self.addNodeScalarText)

    def addNodeToOuterChanceTextChange(self, *args):
        try:
            val = float(self.addNodeToOuterChanceText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.addNodeToOuterChanceText)
            return

        if val < 0 or val > 1:
            updateSettingTextColor(True, self.addNodeToOuterChanceText)
            return

        Settings.ADD_NODE_TO_OUTER_CHANCE = val
        updateSettingTextColor(False, self.addNodeToOuterChanceText)

    def copyConnectionChancesTextChange(self, *args):
        try:
            val = int(self.copyConnectionChancesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.copyConnectionChancesText)
            return

        if val < 0:
            updateSettingTextColor(True, self.copyConnectionChancesText)
            return

        Settings.COPY_CONNECTION_CHANCES = val
        updateSettingTextColor(False, self.copyConnectionChancesText)

    def minCopyConnectionChancesTextChange(self, *args):
        try:
            val = int(self.minCopyConnectionChancesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.minCopyConnectionChancesText)
            return

        if val < 0:
            updateSettingTextColor(True, self.minCopyConnectionChancesText)
            return

        Settings.MIN_COPY_CONNECTION_CHANCE = val
        updateSettingTextColor(False, self.minCopyConnectionChancesText)

    def copyConnectionScalarTextChange(self, *args):
        try:
            val = float(self.copyConnectionScalarText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.copyConnectionScalarText)
            return

        Settings.COPY_CONNECTION_SCALAR = val
        updateSettingTextColor(False, self.copyConnectionScalarText)

    def copyConnectionFromInChanceTextChange(self, *args):
        try:
            val = float(self.copyConnectionFromInChanceText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.copyConnectionFromInChanceText)
            return

        if val < 0 or val > 1:
            updateSettingTextColor(True, self.copyConnectionFromInChanceText)
            return

        Settings.COPY_CONNECTION_FROM_IN_CHANCE = val
        updateSettingTextColor(False, self.copyConnectionFromInChanceText)

    def connectionChancesTextChange(self, *args):
        try:
            val = int(self.connectionChancesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.connectionChancesText)
            return

        if val < 0:
            updateSettingTextColor(True, self.connectionChancesText)
            return

        Settings.CONNECTION_CHANCES = val
        updateSettingTextColor(False, self.connectionChancesText)

    def minConnectionChancesTextChange(self, *args):
        try:
            val = int(self.minConnectionChancesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.minConnectionChancesText)
            return

        if val < 0:
            updateSettingTextColor(True, self.minConnectionChancesText)
            return

        Settings.MIN_CONNECTION_CHANCE = val
        updateSettingTextColor(False, self.minConnectionChancesText)

    def connectionScalarTextChange(self, *args):
        try:
            val = float(self.connectionScalarText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.connectionScalarText)
            return

        if val < 0 or val > 1:
            updateSettingTextColor(True, self.connectionScalarText)
            return

        Settings.CONNECTION_SCALAR = val
        updateSettingTextColor(False, self.connectionScalarText)

    def addConnectionProbabilityTextChange(self, *args):
        try:
            val = float(self.addConnectionProbabilityText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.addConnectionProbabilityText)
            return

        if val < 0 or val > 1:
            updateSettingTextColor(True, self.addConnectionProbabilityText)
            return

        Settings.ADD_CONNECTION_PROBABILITY = val
        updateSettingTextColor(False, self.addConnectionProbabilityText)

    def setSeedTextChange(self, *args):
        val = self.setSeedText.get("1.0", END)[0:-1]
        if stringToBool(val) == 0:
            updateSettingTextColor(True, self.setSeedText)
            return

        Settings.SET_SEED = val == "True"
        updateSettingTextColor(False, self.setSeedText)

    def setSeedGamesTextChange(self, *args):
        try:
            string = str(self.setSeedGamesText.get("1.0", END))
            val = ast.literal_eval(string)
            for i in range(len(val)):
                val[i] = int(val[i])

        except (SyntaxError, IndexError, ValueError, TypeError):
            updateSettingTextColor(True, self.setSeedGamesText)
            return

        Settings.SET_SEED_GAMES = val
        updateSettingTextColor(False, self.setSeedGamesText)
        m = self.centralHandler.simMenu
        if m is not None:
            m.updateSetSeedList()

    def randomSeedGamesTextChange(self, *args):
        try:
            val = int(self.randomSeedGamesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.randomSeedGamesText)
            return

        if val < 0:
            updateSettingTextColor(True, self.randomSeedGamesText)
            return

        Settings.RANDOM_SEED_GAMES = val
        updateSettingTextColor(False, self.randomSeedGamesText)

    def pieceSequenceTextChange(self, *args):
        try:
            string = str(self.pieceSequenceText.get("1.0", END))
            val = ast.literal_eval(string)
            for i in range(len(val)):
                if not len(val[i]) == 2:
                    updateSettingTextColor(True, self.pieceSequenceText)
                    return
                val[i] = [val[i][0], val[i][1]]

            for i in range(len(val)):
                val[i][0] = int(val[i][0])
                val[i][1] = int(val[i][1])

                if val[i][0] >= Tetris.NUM_TILE_TYPES:
                    updateSettingTextColor(True, self.pieceSequenceText)
                    return

            for i in range(len(val)):
                val[i] = (val[i][0], val[i][1])

        except (SyntaxError, IndexError, ValueError, TypeError):
            updateSettingTextColor(True, self.pieceSequenceText)
            return

        Settings.PIECE_SEQUENCE = val
        updateSettingTextColor(False, self.pieceSequenceText)

    def removeOutlierFitnessTextChange(self, *args):
        try:
            val = float(self.removeOutlierFitnessText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.removeOutlierFitnessText)
            return

        if val < 0 or val >= .5:
            updateSettingTextColor(True, self.removeOutlierFitnessText)
            return

        Settings.REMOVE_OUTLIER_FITNESS = val
        updateSettingTextColor(False, self.removeOutlierFitnessText)

    def removeFitnessTypeLabelTextChange(self, *args):
        try:
            val = int(self.removeFitnessTypeText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.removeFitnessTypeText)
            return

        if not (val is 0 or val is 1 or val is 2):
            updateSettingTextColor(True, self.removeFitnessTypeText)
            return

        Settings.REMOVE_FITNESS_TYPE = val
        updateSettingTextColor(False, self.removeFitnessTypeText)

    def useFilledForFitnessTextChange(self, *args):
        val = self.useFilledForFitnessText.get("1.0", END)[0:-1]
        if stringToBool(val) == 0:
            updateSettingTextColor(True, self.useFilledForFitnessText)
            return

        Settings.USE_FILLED_FOR_FITNESS = val is "True"
        updateSettingTextColor(False, self.useFilledForFitnessText)

    def numberNetMovesTextChange(self, *args):
        try:
            val = int(self.numberNetMovesText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.numberNetMovesText)
            return

        if val < 1:
            updateSettingTextColor(True, self.numberNetMovesText)
            return

        Settings.NUMBER_NET_MOVES = val
        updateSettingTextColor(False, self.numberNetMovesText)

    def fitnessPieceTextChange(self, *args):
        try:
            val = float(self.fitnessPieceText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.fitnessPieceText)
            return

        Settings.FITNESS_PIECE = val
        updateSettingTextColor(False, self.fitnessPieceText)

    def fitnessLineTextChange(self, *args):
        try:
            val = float(self.fitnessLineText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.fitnessLineText)
            return

        Settings.FITNESS_LINE = val
        updateSettingTextColor(False, self.fitnessLineText)

    def fitnessScalarTextChange(self, *args):
        try:
            val = float(self.fitnessScalarText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.fitnessScalarText)
            return

        Settings.FITNESS_SCALAR = val
        updateSettingTextColor(False, self.fitnessScalarText)

    def dispRefreshRateTextChange(self, *args):
        try:
            val = int(self.dispRefreshRateText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.dispRefreshRateText)
            return

        if val < 0:
            updateSettingTextColor(True, self.dispRefreshRateText)
            return

        Settings.DISP_REFRESH_RATE = val
        updateSettingTextColor(False, self.dispRefreshRateText)

    def maxRowsTextChange(self, *args):
        try:
            val = int(self.maxRowsText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.maxRowsText)
            return

        if val < 0:
            updateSettingTextColor(True, self.maxRowsText)
            return

        Settings.MAX_ROWS = val
        updateSettingTextColor(False, self.maxRowsText)

    def percentBestRemoveTextChange(self, *args):
        try:
            val = float(self.percentBestRemoveText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.percentBestRemoveText)
            return

        if val < 0 or val > 1:
            updateSettingTextColor(True, self.percentBestRemoveText)
            return

        Settings.PERCENT_BEST_REMOVE = val
        updateSettingTextColor(False, self.percentBestRemoveText)

    def fontSizeTextChange(self, *args):
        try:
            val = int(self.fontSizeText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.fontSizeText)
            return

        if val < 1:
            updateSettingTextColor(True, self.fontSizeText)
            return

        Settings.FONT_SIZE = val
        updateSettingTextColor(False, self.fontSizeText)
        m = self.centralHandler.simMenu
        if m is not None:
            m.updateGridButtonsFontSize()

    def numButtonColTextChange(self, *args):
        try:
            val = int(self.numButtonColText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.numButtonColText)
            return

        if val < 1:
            updateSettingTextColor(True, self.numButtonColText)
            return

        Settings.NUM_BUTTON_COL = val
        updateSettingTextColor(False, self.numButtonColText)
        m = self.centralHandler.simMenu
        if m is not None:
            m.updateButtonsGridLayout()

    def gridWidthTextChange(self, *args):
        self.validSettings[0] = False
        try:
            val = int(self.gridWidthText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.gridWidthText)
            return

        if val < 4:
            updateSettingTextColor(True, self.gridWidthText)
            return

        self.validSettings[0] = True
        updateSettingTextColor(False, self.gridWidthText)

    def gridHeightTextChange(self, *args):
        self.validSettings[1] = False
        try:
            val = int(self.gridHeightText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.gridHeightText)
            return

        if val < 4:
            updateSettingTextColor(True, self.gridHeightText)
            return
        self.validSettings[1] = True
        updateSettingTextColor(False, self.gridHeightText)

    def numBrainsTextChange(self, *args):
        self.validSettings[2] = False
        try:
            val = int(self.numBrainsText.get("1.0", END))
        except ValueError:
            updateSettingTextColor(True, self.numBrainsText)
            return

        if val < 2 or val % 2 is not 0:
            updateSettingTextColor(True, self.numBrainsText)
            return

        self.validSettings[2] = True
        updateSettingTextColor(False, self.numBrainsText)

    def distanceInputsTextChange(self, *args):
        self.validSettings[3] = False
        val = self.distanceInputsText.get("1.0", END)[0:-1]
        if stringToBool(val) == 0:
            updateSettingTextColor(True, self.distanceInputsText)
            return

        self.validSettings[3] = True
        updateSettingTextColor(False, self.distanceInputsText)

    def relativeNeuralInputsTextChange(self, *args):
        self.validSettings[4] = False
        val = self.relativeNeuralInputsText.get("1.0", END)[0:-1]
        if stringToBool(val) == 0:
            updateSettingTextColor(True, self.relativeNeuralInputsText)
            return

        self.validSettings[4] = True
        updateSettingTextColor(False, self.relativeNeuralInputsText)

    def splitNeuralInputsTextChange(self, *args):
        self.validSettings[5] = False
        val = self.splitNeuralInputsText.get("1.0", END)[0:-1]
        if stringToBool(val) == 0:
            updateSettingTextColor(True, self.splitNeuralInputsText)
            return

        self.validSettings[5] = True
        updateSettingTextColor(False, self.splitNeuralInputsText)

    def updateSettingsTextBoxes(self):
        self.gridWidthText.delete('1.0', END)
        self.gridWidthText.insert(END, str(Settings.GRID_WIDTH))

        self.gridHeightText.delete('1.0', END)
        self.gridHeightText.insert(END, str(Settings.GRID_HEIGHT))

        self.gridXText.delete('1.0', END)
        self.gridXText.insert(END, str(Settings.GRID_X))

        self.gridYText.delete('1.0', END)
        self.gridYText.insert(END, str(Settings.GRID_Y))

        self.squareSizeText.delete('1.0', END)
        self.squareSizeText.insert(END, str(Settings.SQUARE_SIZE))

        self.gridSizeText.delete('1.0', END)
        self.gridSizeText.insert(END, str(Settings.GRID_SIZE))

        self.gridLineText.delete('1.0', END)
        self.gridLineText.insert(END, str(Settings.GRID_LINE))

        self.numBrainsText.delete('1.0', END)
        self.numBrainsText.insert(END, str(Settings.NUM_BRAINS))

        self.maxMutabilityText.delete('1.0', END)
        self.maxMutabilityText.insert(END, str(Settings.MAX_MUTABILITY))

        self.weightBiasScalarText.delete('1.0', END)
        self.weightBiasScalarText.insert(END, str(Settings.WEIGHT_BIAS_SCALAR))

        self.mutabilityChangeText.delete('1.0', END)
        self.mutabilityChangeText.insert(END, str(Settings.MUTABILITY_CHANGE))

        self.removeNodeScalarText.delete('1.0', END)
        self.removeNodeScalarText.insert(END, str(Settings.REMOVE_NODE_SCALAR))

        self.addNodeChancesText.delete('1.0', END)
        self.addNodeChancesText.insert(END, str(Settings.ADD_NODE_CHANCES))

        self.minAddNodeChanceText.delete('1.0', END)
        self.minAddNodeChanceText.insert(END, str(Settings.MIN_ADD_NODE_CHANCE))

        self.addNodeScalarText.delete('1.0', END)
        self.addNodeScalarText.insert(END, str(Settings.ADD_NODE_SCALAR))

        self.addNodeToOuterChanceText.delete('1.0', END)
        self.addNodeToOuterChanceText.insert(END, str(Settings.ADD_NODE_TO_OUTER_CHANCE))

        self.copyConnectionChancesText.delete('1.0', END)
        self.copyConnectionChancesText.insert(END, str(Settings.COPY_CONNECTION_CHANCES))

        self.minCopyConnectionChancesText.delete('1.0', END)
        self.minCopyConnectionChancesText.insert(END, str(Settings.MIN_COPY_CONNECTION_CHANCE))

        self.copyConnectionScalarText.delete('1.0', END)
        self.copyConnectionScalarText.insert(END, str(Settings.COPY_CONNECTION_SCALAR))

        self.copyConnectionFromInChanceText.delete('1.0', END)
        self.copyConnectionFromInChanceText.insert(END, str(Settings.COPY_CONNECTION_FROM_IN_CHANCE))

        self.connectionChancesText.delete('1.0', END)
        self.connectionChancesText.insert(END, str(Settings.CONNECTION_CHANCES))

        self.minConnectionChancesText.delete('1.0', END)
        self.minConnectionChancesText.insert(END, str(Settings.MIN_CONNECTION_CHANCE))

        self.connectionScalarText.delete('1.0', END)
        self.connectionScalarText.insert(END, str(Settings.CONNECTION_SCALAR))

        self.addConnectionProbabilityText.delete('1.0', END)
        self.addConnectionProbabilityText.insert(END, str(Settings.ADD_CONNECTION_PROBABILITY))

        self.setSeedText.delete('1.0', END)
        self.setSeedText.insert(END, str(Settings.SET_SEED))

        self.distanceInputsText.delete('1.0', END)
        self.distanceInputsText.insert(END, str(Settings.DISTANCE_INPUTS))

        self.relativeNeuralInputsText.delete('1.0', END)
        self.relativeNeuralInputsText.insert(END, str(Settings.RELATIVE_NEURAL_INPUTS))

        self.splitNeuralInputsText.delete('1.0', END)
        self.splitNeuralInputsText.insert(END, str(Settings.SPLIT_NEURAL_INPUTS))

        self.setSeedGamesText.delete('1.0', END)
        self.setSeedGamesText.insert(END, str(Settings.SET_SEED_GAMES))

        self.randomSeedGamesText.delete('1.0', END)
        self.randomSeedGamesText.insert(END, str(Settings.RANDOM_SEED_GAMES))

        self.pieceSequenceText.delete('1.0', END)
        self.pieceSequenceText.insert(END, str(Settings.PIECE_SEQUENCE))

        self.removeOutlierFitnessText.delete('1.0', END)
        self.removeOutlierFitnessText.insert(END, str(Settings.REMOVE_OUTLIER_FITNESS))

        self.removeFitnessTypeText.delete('1.0', END)
        self.removeFitnessTypeText.insert(END, str(Settings.REMOVE_FITNESS_TYPE))

        self.useFilledForFitnessText.delete('1.0', END)
        self.useFilledForFitnessText.insert(END, str(Settings.USE_FILLED_FOR_FITNESS))

        self.numberNetMovesText.delete('1.0', END)
        self.numberNetMovesText.insert(END, str(Settings.NUMBER_NET_MOVES))

        self.fitnessPieceText.delete('1.0', END)
        self.fitnessPieceText.insert(END, str(Settings.FITNESS_PIECE))

        self.fitnessLineText.delete('1.0', END)
        self.fitnessLineText.insert(END, str(Settings.FITNESS_LINE))

        self.fitnessScalarText.delete('1.0', END)
        self.fitnessScalarText.insert(END, str(Settings.FITNESS_SCALAR))

        self.dispRefreshRateText.delete('1.0', END)
        self.dispRefreshRateText.insert(END, str(Settings.DISP_REFRESH_RATE))

        self.maxRowsText.delete('1.0', END)
        self.maxRowsText.insert(END, str(Settings.MAX_ROWS))

        self.percentBestRemoveText.delete('1.0', END)
        self.percentBestRemoveText.insert(END, str(Settings.PERCENT_BEST_REMOVE))

        self.fontSizeText.delete('1.0', END)
        self.fontSizeText.insert(END, str(Settings.FONT_SIZE))

        self.numButtonColText.delete('1.0', END)
        self.numButtonColText.insert(END, str(Settings.NUM_BUTTON_COL))


# return 0 for invalid string, 1 for true, -1 for false
def stringToBool(string):
    if string == "True":
        return 1
    elif string == "False":
        return -1
    else:
        return 0


# error = True: set the color to be red
# error = False: set th ecolor to white
# text: the text field that should be changed
def updateSettingTextColor(error, text):
    if error:
        text.configure(bg="#FFAAAA", highlightcolor="#A00000")
    else:
        text.configure(bg="#FFFFFF", highlightcolor="#000000")


def makeSettingsLabel(name, r, frame):
    lab = Label(frame, height=1, text=name, bg="#FFFFFF", font=('Impact', 13), anchor="e")
    lab.grid(column=0, row=r, sticky=N + S + E + W)
    return lab


def makeSettingsText(r, frame):
    text = Text(frame, height=1, width=15, font=('Impact', 13), highlightthickness=2)
    text.grid(column=1, row=r, sticky=N + S + E + W)
    return text
