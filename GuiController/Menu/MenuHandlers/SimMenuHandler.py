from NeuralNet import NeuralNetHandler
from NeuralNet import NeuralNet

from TetrisGame import Tetris

import copy
import random
import time

import Settings
import SaveLoader
import MergeSort


class SimMenuHandler:

    def __init__(self, centralHandler, newSim, initMenu):
        # the current generation of this simulator
        self.generation = 0

        self.centralHandler = centralHandler

        # the neural networks that are in a simulation
        self.brains = []
        for i in range(Settings.NUM_BRAINS):
            self.brains.append(None)

        # use a thread to start up the handler
        if newSim:
            self.setUpBrains(initMenu)

        # keeps track of if the menu is loading in a game
        self.loading = False

    # used by __init__ to set up all the brain data via a thread
    def setUpBrains(self, initMenu):
        for i in range(Settings.NUM_BRAINS):
            self.brains[i] = NeuralNetHandler.createNewNeuralNet(True)
            if initMenu is not None:
                initMenu.startButton.configure(
                        text="Creating " + str(round(10 * (i / Settings.NUM_BRAINS), 2)) + "% done")

    # tests the curtent generation and sorts them by performance
    # simMenu is passed as a parameter so this method can update information on the menu, pass None for this
    # value if no updating is needed
    # menu: the menu to update
    # siMenu: True if menu is a simMenu, false if it is an initMenu
    def testGeneration(self, menu, simMenu):
        if simMenu:
            menu.nextGenButton.configure(text="Testing gen...")
        else:
            menu.startButton.configure(text="Creating 10% done")

        # pick all the seeds to use for testing, only used if SET_SEED = False
        seeds = []
        random.seed(time.time())
        if Settings.SET_SEED:
            for i in Settings.SET_SEED_GAMES:
                seeds.append(i)
        else:
            for i in range(Settings.RANDOM_SEED_GAMES):
                seeds.append(random.uniform(-2000000, 2000000))

        # test each brain
        cnt = 0
        for b in self.brains:

            # only test the AI if it has not already been tested or if the game's pieces are randomized each time
            if not b.tested or not Settings.SET_SEED:
                fit = []

                # perform the appropriate amount of tests based on if a set seed is used
                for i in seeds:
                    game = Tetris.Tetris()

                    # seed the RNG
                    random.seed(i)
                    game.pieceCounter = 0
                    game.makeNewPiece()

                    # test the game with the current seed
                    while not game.gameOver:
                        NeuralNetHandler.makeNeuralNetMove(b, game, None)
                        game.nextLine()
                        if game.rowsRemoved > Settings.MAX_ROWS:
                            game.endGame()
                            break

                    # add the fitness of the last game to the list for averaging
                    fit.append(game.fitness)

                # remove the highest and lowest scores to get rid out outliers
                if Settings.REMOVE_OUTLIER_FITNESS > 0:
                    # sort the fitness values
                    fit = MergeSort.mergeSortNum(fit)

                    # get initital size of fitness list
                    initSize = len(fit)

                    # remove the top and bottom
                    if Settings.REMOVE_FITNESS_TYPE == 0:
                        # only continue if 2 fitness socres can be removed
                        if len(fit) >= 3:
                            # remove highest and lowest percents, always leaving at least 1 fitness score
                            while len(fit) > 1 and len(fit) / initSize > Settings.REMOVE_OUTLIER_FITNESS * 2:
                                # ensure that there is always at least 1 or 2 entries
                                if len(fit) <= 2:
                                    break

                                # remove first and last elements
                                fit.pop(0)
                                fit.pop(-1)
                    # remove all but the lowest
                    elif Settings.REMOVE_FITNESS_TYPE == 1:
                        # only continue if at least 1 fitness score can be remove
                        if len(fit) >= 2:
                            # remove all but the lowest performers
                            while len(fit) > 1 and len(fit) / initSize > Settings.REMOVE_OUTLIER_FITNESS:
                                # ensure that there is always at least 1 entry
                                if len(fit) < 2:
                                    break
                                # remove first element, the best performing seed
                                fit.pop(0)
                    # remove all but the highest
                    elif Settings.REMOVE_FITNESS_TYPE == 2:
                        # only continue if at least 1 fitness score can be remove
                        if len(fit) >= 2:
                            # remove all but the lowest performers
                            while len(fit) > 1 and len(fit) / initSize > Settings.REMOVE_OUTLIER_FITNESS:
                                # ensure that there is always at least 1 entry
                                if len(fit) < 2:
                                    break
                                # remove last element, the worst performing seed
                                fit.pop(-1)

                # find the average fitness among all remaning seeds
                f = 0
                fitCnt = 0
                for i in fit:
                    f += i
                    fitCnt += 1
                b.fitness = f / fitCnt

                b.setTested(True)
                # update the percentage complete count
                if simMenu:
                    menu.netsTested += 1
                    menu.updateInfoLabelText()
                else:
                    cnt += 1
                    menu.startButton.configure(
                        text="Creating " + str(round(10 + 80 * (cnt / len(self.brains)), 2)) + "% done")

        if simMenu:
            menu.nextGenButton.configure(text="Sorting")
        else:
            menu.startButton.configure(text="Creating 95% done")

        # sort the brains by fitness
        self.sortBrains()

        # add data points to the graphs
        # fitness

        # upper percentiles
        for i in range(9):
            self.centralHandler.graphHandler.fitnessGraph.addData(i, self.brains[
                int(len(self.brains) * .01 * (i + 1))
            ].fitness)

        # lower percentiles
        for i in range(9):
            self.centralHandler.graphHandler.fitnessGraph.addData(i + 9, self.brains[
                int(len(self.brains) * (0.9 + .01 * (i + 1)))
            ].fitness)

        # main values
        # best
        self.centralHandler.graphHandler.fitnessGraph.addData(18, self.brains[0].fitness)
        # 10-90 percentile
        for i in range(9):
            self.centralHandler.graphHandler.fitnessGraph.addData(19 + i, self.brains[
                int(len(self.brains) * .1 * (i + 1))
            ].fitness)

        # worst
        self.centralHandler.graphHandler.fitnessGraph.addData(28, self.brains[
            -1
        ].fitness)

        # add values to mutability graph
        mutabilities = []
        for b in self.brains:
            mutabilities.append(b.mutability)
        mutabilities = MergeSort.mergeSortNum(mutabilities)

        self.centralHandler.graphHandler.mutabilityGraph.addData(0, mutabilities[0])
        self.centralHandler.graphHandler.mutabilityGraph.addData(1, mutabilities[int(len(mutabilities) / 2)])
        self.centralHandler.graphHandler.mutabilityGraph.addData(2, mutabilities[-1])

        # add values to generations graph
        births = []
        for b in self.brains:
            births.append(b.birthGen)
        births = MergeSort.mergeSortNum(births)
        self.centralHandler.graphHandler.generationsGraph.addData(0, births[0])
        self.centralHandler.graphHandler.generationsGraph.addData(1, births[-1])
        self.centralHandler.graphHandler.generationsGraph.addData(2, abs(births[0] - births[-1]))

        if not simMenu:
            menu.startButton.configure(text="Creating 100% done")

    # removes the worst 50% of performers and generates new brains to fill in the
    # ones that were removed
    def nextGeneration(self, simMenu):
        simMenu.nextGenButton.configure(text="Removing worst")

        # seed the RNG
        random.seed(time.time())

        # remove the worst 50% of the performers, and store the rest in the removed list
        removed = self.brains[Settings.NUM_BRAINS // 2:]
        self.brains = self.brains[:Settings.NUM_BRAINS // 2]

        # only need to make replacements if Settings.PERCENT_BEST_REMOVE is > 0
        if Settings.PERCENT_BEST_REMOVE > 0:
            # make a list of all the index values of the top perofrmers
            indexes = []
            i = 0
            while i < Settings.NUM_BRAINS / 2:
                indexes.append(i)
                i += 1

            # pick some index values to replace some of the top performers with the worse performers
            replaceIndexes = []
            # the number of replacements to make
            numReplace = int(Settings.NUM_BRAINS * Settings.PERCENT_BEST_REMOVE)
            for i in range(numReplace):
                # if there are no more inedexes, stop trying to add more
                if len(indexes) <= 0:
                    break
                # pick a random index and put it in the list of indexes to replace, weighted towards higher indexes
                rand = 1 - pow(random.uniform(0, 1), 6)
                replaceIndexes.append(indexes.pop(int((len(indexes) - 1) * rand)))

            # now, using the replaceIndexes, pick one of those indexes at random and replace a NeuralNet from the
            # current survivors
            while len(replaceIndexes) > 0:
                # get an index and remove it from the list
                i = replaceIndexes.pop()
                # get a random brain from the removed list and remove it, weighted to lover values
                rand = pow(random.uniform(0, 1), 6)
                replaceBrain = removed.pop(int((len(removed) - 1) * rand))
                # set that removed brain in the brain list
                self.brains[i] = replaceBrain

        simMenu.nextGenButton.configure(text="Mutating best")

        # add coppies of the remaining brains to fill in the list and mutate the new coppies
        for i in range(int(Settings.NUM_BRAINS / 2)):
            oldBrain = copy.deepcopy(self.brains[i])
            self.brains.append(oldBrain)
            self.brains[i].mutate()
            self.brains[i].parentId = oldBrain.id
            self.brains[i].birthGen = self.generation + 1

        self.generation += 1

        simMenu.nextGenButton.configure(text="Now testing...")

    # sort all of the brains by their current fitness
    def sortBrains(self):
        self.brains = MergeSort.mergeSort(self.brains)

    # saves all information associated with the state of the simualtion
    # the file is a text file called "save.txt"
    # this includes: the current settings, all the brains, the current gen, graph data
    def save(self):
        with open('saves/' + self.centralHandler.simMenu.getValidSaveName() + '.txt', 'w') as f:
            # save settings
            Settings.save(f)

            # save general sim data
            f.write(str(self.generation) + '\n')
            f.write(str(NeuralNet.idCnt.id) + '\n')

            # save neural nets
            for b in self.brains:
                b.save(f)

            # save graph data
            self.centralHandler.graphHandler.fitnessGraph.save(f)
            self.centralHandler.graphHandler.mutabilityGraph.save(f)
            self.centralHandler.graphHandler.generationsGraph.save(f)

    # load, from the save file save.txt, the simulation in
    # this will set all data of the graphs, neural nets, general sim data, and so on
    def load(self, initMenu):
        self.loading = True

        with open('saves/' + initMenu.getLoadSaveName(), 'r') as f:

            initMenu.loadButton.configure(text="Loading 0% done")

            # load settings
            Settings.load(f)

            initMenu.loadButton.configure(text="Loading 5% done")

            # load general sim data
            self.generation = SaveLoader.intLine(f.readline())
            NeuralNet.idCnt.id = SaveLoader.intLine(f.readline())

            # load neural nets
            self.brains = []
            for i in range(Settings.NUM_BRAINS):
                newB = NeuralNet.NeuralNet(0, 0, 0)
                newB.load(f)
                self.brains.append(newB)
                initMenu.loadButton.configure(
                    text="Loading " + str(round(5 + 90 * (i / Settings.NUM_BRAINS), 2)) + "% done")

            initMenu.loadButton.configure(text="Loading 95% done")

            # load graph data
            self.centralHandler.graphHandler.fitnessGraph.load(f)
            self.centralHandler.graphHandler.mutabilityGraph.load(f)
            self.centralHandler.graphHandler.generationsGraph.load(f)

            initMenu.loadButton.configure(text="Loading 100% done")

        self.loading = False
