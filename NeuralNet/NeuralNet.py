from NeuralNet import NeuralNetHandler

import math
import random
import time

import pygame

import Settings
import SaveLoader
import MiscUtil


class idCounter:
    def __init__(self):
        self.id = 0

    def next(self):
        self.id += 1
        return self.id


idCnt = idCounter()

# variables for rendering the net
# the upper lefthand corner of the initial position of the network drawing
R_X = 850
R_Y = 400
# the size of each node
R_SIZE = 50
R_SQUARE = Settings.SQUARE_SIZE
# the thickness of the lines of the nodes
R_THICK = 2


# An object that keeps track of an processes a neural network
class NeuralNet:

    # variables for keeping track of the mouse
    # if the mouse is held down or not
    leftMouseDown = False
    # the id of the inner node that should be positioned to the mouse, should be less than 0 if none should move
    moveNodeIndex = -1

    # numIn: the number of input nodes
    # numOut: the number of output nodes
    # createID: True if this netowrk should have an ID for th eismulation, false otherwise
    def __init__(self, numIn, numOut, createId):
        # create the neural net id
        if createId:
            self.id = idCnt.next()
        else:
            self.id = -1

        # the generation this NeuralNet was created in
        self.birthGen = 0
        # the id of the NeuralNet who mutated into this NeuralNet, -1 means they have no parent
        self.parentId = -1

        # the values in each of the input nodes that will be fed through the network
        self.inNodes = []
        for i in range(numIn):
            self.inNodes.append(Node(0))

        # make a random seed
        random.seed(time.time())

        # the values in each of the output nodes that can be acessed as outputs
        self.outNodes = []
        for i in range(numOut):
            self.outNodes.append(Node(random.uniform(-1, 1)))

        # the nodes on the inside of the net that can connect the inNodes to the outNodes
        self.innerNodes = []

        # the total number of shapes that the AI placed down before the game ended plus the number of rows made
        self.fitness = 0

        # true if this net has not yet recived a fitness score
        self.tested = False

        # the variable that governs how fast mutations occur.
        # 0 is no change at all
        # -MAX_MUTABILITY or MAX_MUTAVILITY are very large changes
        # this value is changed slightly whenever this net is mutated
        self.mutability = random.uniform(-Settings.MAX_MUTABILITY, Settings.MAX_MUTABILITY)

    def setTested(self, tested):
        self.tested = tested

    # find the values of each output based on the inputs
    def calculateOutputs(self):
        # set all the inner node calculated status to False
        for n in self.innerNodes:
            n.setCalculated(False)

        for i in range(len(self.outNodes)):
            self.calculateNode(2, i)

    # calculate the value of the given node
    # nodes: 0 = input list
    #        1 = inner list
    #        2 = output list
    # index: the index in the list of the node to calculate
    def calculateNode(self, nodes, index):
        if nodes == 0:
            return self.inNodes[index].value

        inputs = []
        if nodes == 1:
            if not self.innerNodes[index].calculated:
                for c in self.innerNodes[index].connections:
                    inputs.append(self.calculateNode(c.inType, c.inIndex))
                return self.innerNodes[index].calculateValue(inputs)
            else:
                return self.innerNodes[index].value

        elif nodes == 2:
            for c in self.outNodes[index].connections:
                inputs.append(self.calculateNode(c.inType, c.inIndex))
            return self.outNodes[index].calculateValue(inputs)

    # connect two nodes by a weight
    # inType: the type of node that the connection feeds out of
    #       0: input node
    #       1: inner node
    # outType: the type of node that the connection feeds in to
    #       0: output node
    #       1: inner node
    # outIndex: the node in the corresponding list to use as the input
    # inIndex: the node in the corresponding list to use as the output
    # weight: the weight between the 2 nodes
    # if the attempted to add connection is not in a valid position where the ranks of inner nodes are not in ascending
    #   order, then no connection is added
    # returns true if the connection is added, false otherwise
    def addConnection(self, inType, outType, inIndex, outIndex, weight):
        # check if the both nodes to connect are inner nodes, if they are then ensure that their ranks are in
        # decending order, if they are not, then return
        # this is to avoid infinite recursion

        # check if both nodes are inner nodes
        if inType == 1 and outType == 1:
            # check if the nodes are in decending order of, return if they are not
            if self.innerNodes[inIndex].rank >= self.innerNodes[outIndex].rank:
                return False

        if outType == 0:
            # check to see if a connection already exists in the given location
            found = False
            for c in self.outNodes[outIndex].connections:
                if c.inIndex == inIndex and c.inType == inType:
                    found = True
                    break

            if not found:
                self.outNodes[outIndex].connections.append(Connection(inType, inIndex, weight))
        elif outType == 1:
            # check to see if a connection already exists in the given location
            found = False
            for c in self.innerNodes[outIndex].connections:
                if c.inIndex == inIndex and c.inType == inType:
                    found = True
                    break

            if not found:
                self.innerNodes[outIndex].connections.append(Connection(inType, inIndex, weight))
        return True

    # split an existing connection, using a node
    # the connection that will be split is based on the given node and the index of its connection
    # inType: the type of node that the connection feeds in to
    #       0: output node
    #       1: inner node
    # nodeIndex: the index of the node that the connection that is to be split comes in to
    # conIndex: the index of the connections of the node that is to be split
    # bias: the bias for the new node
    # nothing is changed if no conenction is found
    # returns true if the node is added, false otherwise
    def addInnerNode(self, inType, nodeIndex, conIndex, bias):
        # variables to keep track of which node positions were used

        # add a new inner node
        newNode = Node(bias)
        # if this connection connects and in node to and out node, then its rank is 0
        if inType == 0 and self.outNodes[nodeIndex].connections[conIndex].inType == 0:
            newNode.setRank(0)
            pos1 = self.outNodes[nodeIndex].renderPos
            pos2 = self.inNodes[self.outNodes[nodeIndex].connections[conIndex].inIndex].renderPos

        # if this connection connects an in node and an inner node, then its rank is the inner node rank -1
        elif inType == 1 and self.innerNodes[nodeIndex].connections[conIndex].inType == 0:
            newNode.setRank(self.innerNodes[nodeIndex].rank - 1)
            pos1 = self.innerNodes[nodeIndex].renderPos
            pos2 = self.inNodes[self.innerNodes[nodeIndex].connections[conIndex].inIndex].renderPos

        # if this connection connects an out node and an inner node, then its rank is the inner node +1
        elif inType == 0 and self.outNodes[nodeIndex].connections[conIndex].inType == 1:
            newNode.setRank(self.innerNodes[self.outNodes[nodeIndex].connections[conIndex].inIndex].rank + 1)
            pos1 = self.outNodes[nodeIndex].renderPos
            pos2 = self.innerNodes[self.outNodes[nodeIndex].connections[conIndex].inIndex].renderPos

        # if this connection connects 2 inner nodes, then the rank of the new node is the average of the
        # previous 2 nodes
        elif inType == 1 and self.innerNodes[nodeIndex].connections[conIndex].inType == 1:
            newNode.setRank((self.innerNodes[nodeIndex].rank +
                             self.innerNodes[self.innerNodes[nodeIndex].connections[conIndex].inIndex].rank) / 2)
            pos1 = self.innerNodes[nodeIndex].renderPos
            pos2 = self.innerNodes[self.innerNodes[nodeIndex].connections[conIndex].inIndex].renderPos

        # invalid state, do nothing
        else:
            return False

        # add the node
        self.innerNodes.append(newNode)
        # determine the render pos of the node
        self.innerNodes[-1].setRenderPos((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)

        c = None

        # remove the old connection
        if inType == 0:
            c = self.outNodes[nodeIndex].connections.pop(conIndex)
        elif inType == 1:
            c = self.innerNodes[nodeIndex].connections.pop(conIndex)

        if c is None:
            return False

        # add a connection from the old in node to the new inner node
        # the new weight is the old conectionw eight
        self.innerNodes[-1].connections.append(Connection(c.inType, c.inIndex, c.weight))

        # add a connection from the new inner node to the node from the origional connection
        if inType == 0:
            self.outNodes[nodeIndex].connections.append(Connection(1, len(self.innerNodes) - 1, c.weight))
        elif inType == 1:
            self.innerNodes[nodeIndex].connections.append(Connection(1, len(self.innerNodes) - 1, c.weight))

        return True

    # remove the given inner node from the inner node list and adjust all connections to account for the change
    # in the index of all the inner nodes
    def removeInnerNode(self, index):
        # get and remove the inner node from the list
        self.innerNodes.pop(index)

        # if any nodes have connections to an inner node with indexes great than the remove index, their connected
        # index has to be changed
        for n in self.innerNodes:
            for c in n.connections:
                if c.inType == 1 and c.inIndex > index:
                    c.setInIndex(c.inIndex - 1)
        for n in self.outNodes:
            for c in n.connections:
                if c.inType == 1 and c.inIndex > index:
                    c.setInIndex(c.inIndex - 1)

        # all connections from this node need to be removed
        for n in self.innerNodes:
            i = 0
            while i < len(n.connections):
                if n.connections[i].inIndex == index and n.connections[i].inType == 1:
                    n.connections.pop(i)
                    i -= 1
                i += 1
        for n in self.outNodes:
            i = 0
            while i < len(n.connections):
                if n.connections[i].inIndex == index and n.connections[i].inType == 1:
                    n.connections.pop(i)
                    i -= 1
                i += 1

    # set the values in the input nodes
    # inputs: a list of numbers that will be the values of the input nodes
    def setInputs(self, inputs):
        for i in range(len(inputs)):
            self.inNodes[i].value = inputs[i]

    # get a list of all the outputs in their order according to indexes
    def getOutputs(self):
        outputs = []
        for o in self.outNodes:
            outputs.append(o.value)

        return outputs

    # randomly mutates the neural net.
    # this could add connections, remove connections, change values of connections,
    # add inner nodes, remove inner nodes and all of their associated connections,
    # or change the bias of any node
    # also gives this NEuralNet a new id
    def mutate(self):
        # make a random seed
        random.seed(time.time())
        # reset tested and fitness
        self.tested = False
        self.fitness = 0

        # give new id
        self.id = idCnt.next()

        # update mutability
        if Settings.MUTABILITY_CHANGE >= 0:
            self.mutability += random.uniform(-Settings.MUTABILITY_CHANGE, Settings.MUTABILITY_CHANGE)
        else:
            self.mutability = random.uniform(-Settings.MAX_MUTABILITY, Settings.MAX_MUTABILITY)
        # ensure that mutabililty stays in the normal range
        self.mutability = min(Settings.MAX_MUTABILITY, max(-Settings.MAX_MUTABILITY, self.mutability))
        # get the absolute value of mutability
        aMut = abs(self.mutability)

        # add and remove inner nodes

        # remove
        i = 0
        while i < len(self.innerNodes):
            # randomly choose if a node should be removed
            if random.uniform(0, 1) < aMut / Settings.MAX_MUTABILITY * Settings.REMOVE_NODE_SCALAR:
                self.removeInnerNode(i)
                i -= 1
            i += 1
        # add a number of chances to add a node, always at least MIN_ADD_NODE_CHANCE chances
        for i in range(int(max(Settings.MIN_ADD_NODE_CHANCE, aMut * Settings.ADD_NODE_CHANCES))):
            # randomly choose if a node should be added
            if random.uniform(0, 1) < aMut / Settings.MAX_MUTABILITY * Settings.ADD_NODE_SCALAR:
                # select a random out node. If that node has at least one connection, pick a random node
                # to add the inner node to
                if random.uniform(0, 1) < Settings.ADD_NODE_TO_OUTER_CHANCE:
                    nIndex = int(random.uniform(0, len(self.outNodes)))
                    n = self.outNodes[nIndex]
                    if len(n.connections) > 0:
                        cIndex = int(random.uniform(0, len(n.connections)))
                        self.addInnerNode(0, nIndex, cIndex, random.uniform(-1, 1))
                elif len(self.innerNodes) > 0:
                    nIndex = int(random.uniform(0, len(self.innerNodes)))
                    n = self.innerNodes[nIndex]
                    if len(n.connections) > 0:
                        cIndex = int(random.uniform(0, len(n.connections)))
                        self.addInnerNode(1, nIndex, cIndex, random.uniform(-1, 1))

        # mutate inNodes bais values and connections
        for n in self.inNodes:
            n.mutate(self.mutability)

        # mutate outNodes bais values and connections
        for n in self.outNodes:
            n.mutate(self.mutability)

        # mutate innerNodes bais values and connections
        for n in self.innerNodes:
            n.mutate(self.mutability)

        # randomly pick inner nodes to allow their connections to be coppied or moved

        # a number of chances to move or copy an in node connection, with a minimum
        # only applies when distance inputs are not being used
        if not Settings.DISTANCE_INPUTS:
            for i in range(int(max(Settings.MIN_COPY_CONNECTION_CHANCE, Settings.COPY_CONNECTION_CHANCES * aMut))):
                # a percent chance for each attempt to move or copy a connection to suceed
                if random.uniform(0, 1) < aMut / Settings.MAX_MUTABILITY * Settings.COPY_CONNECTION_SCALAR:

                    # chance to pick an outNode connection
                    if random.uniform(0, 1) < Settings.COPY_CONNECTION_FROM_IN_CHANCE:
                        newInType = 0
                    else:
                        newInType = 1

                    # if an inner node was selected, only continue if there is at least 1 inner node
                    if newInType == 1 and len(self.innerNodes) > 0 or newInType == 0:
                        # pick a random out node
                        if newInType == 0:
                            nodeIndex = int(random.uniform(0, len(self.outNodes) - 1))
                            node = self.outNodes[nodeIndex]
                        # pick a random inner node
                        else:
                            nodeIndex = int(random.uniform(0, len(self.innerNodes) - 1))
                            node = self.innerNodes[nodeIndex]

                        # pick a random connection from the inner node connections,
                        # but only if the node has at least one connection
                        if len(node.connections) > 0:
                            conIndex = int(random.uniform(0, len(node.connections) - 1))
                            con = node.connections[conIndex]
                            # only continue if that node connects to an input node
                            if con.inType == 0:
                                # determine the location of the connection in terms of x and y on the tetris grid
                                x = con.inIndex % Settings.GRID_WIDTH
                                y = con.inIndex // Settings.GRID_HEIGHT

                                # variable to keep track of if a change was made to x and y

                                # randomly adjust x and y by either -1, 1, or not at all
                                changed = [True, True]
                                r = random.uniform(0, 1)
                                if r > .66:
                                    x += 1
                                elif r > .33:
                                    x -= 1
                                else:
                                    changed[0] = False
                                r = random.uniform(0, 1)
                                if r > .66:
                                    y += 1
                                elif r > .33:
                                    y -= 1
                                else:
                                    changed[1] = False

                                # make sure x and y are still in range on the board
                                if x < 0:
                                    x = 0
                                    changed[0] = False
                                elif x > Settings.GRID_WIDTH - 1:
                                    x = Settings.GRID_WIDTH - 1
                                    changed[0] = False
                                if y < 0:
                                    y = 0
                                    changed[1] = False
                                elif y > Settings.GRID_HEIGHT - 1:
                                    y = Settings.GRID_HEIGHT - 1
                                    changed[1] = False

                                # if at least x or y has still changed, continue
                                if changed[0] or changed[1]:
                                    # find the new node index based on x and y
                                    newIndex = y * Settings.GRID_WIDTH + x

                                    # not decide to copy the connection to the new location, or move it
                                    # 50% chance to move, removing the origonal conection
                                    if random.uniform(0, 1) < .5:
                                        node.connections.pop(conIndex)
                                    # create a copy of the old connection at the new location
                                    self.addConnection(0, newInType, newIndex, nodeIndex, con.weight)

        # randomly remove or add connections

        # a number of chances to remove or add a connection, at least some some chanes
        for i in range(int(max(Settings.MIN_CONNECTION_CHANCE, Settings.CONNECTION_CHANCES * aMut))):
            # randomly choose to add or remove a connection or do nothing
            if random.uniform(0, 1) < aMut / Settings.MAX_MUTABILITY * Settings.CONNECTION_SCALAR:
                # total for a weighted chance for picking which node to remove or add a connection from
                total = len(self.innerNodes) + len(self.outNodes)
                if random.uniform(0, 1) > len(self.innerNodes) / total:
                    self.addRemoveConnection(self.outNodes, 0)
                else:
                    self.addRemoveConnection(self.innerNodes, 1)

        # check if any nodes have no connections feeding out of them, because if this is the case they are useless
        #   and don't do anything to the neural net
        # all of these nodes will be removed
        # this only applies to inner nodes

        # for each innerNode, check if any inner nodes have a connection to it, if none do, remove the node
        j = 0
        while j < len(self.innerNodes):
            n = self.innerNodes[j]
            # keep track of if this node has found a connection
            found = False

            # first check inner nodes
            i = 0
            while i < len(self.innerNodes) and not found:
                test = self.innerNodes[i]
                # only continue if there could be a connection
                if test.rank > n.rank:
                    # now check all of the connections feeding out of test
                    for c in test.connections:
                        if c.inIndex == j:
                            found = True
                            break
                i += 1

            # next check outer nodes
            i = 0
            while i < len(self.outNodes) and not found:
                test = self.outNodes[i]
                # now check all of the connections feeding out of test
                for c in test.connections:
                    if c.inIndex == j:
                        found = True
                        break
                i += 1

            # if no connections were found, remove the node
            if not found:
                self.removeInnerNode(j)
                j -= 1

            j += 1

    # adds or removes a connection from the given node list, should be called by mutate()
    # nodes: the node list to add or remove connections
    # outIndex: the node list that nodes comes from
    #   0: outNodes
    #   1: innerNodes
    def addRemoveConnection(self, nodes, outIndex):
        # pick an index of a node to add or remove a connection
        nIndex = int(random.uniform(0, len(nodes)))
        # if that node has a connection, then add or remove it
        n = nodes[nIndex]
        # add
        if random.uniform(0, 1) < Settings.ADD_CONNECTION_PROBABILITY:
            # pick either an inner node or in node to connect with
            total = len(self.inNodes) + len(self.innerNodes)
            # pick an in index to add the connection to
            if random.uniform(0, 1) < len(self.inNodes) / total:
                inIndex = int(random.uniform(0, len(self.inNodes)))
                self.addConnection(0, outIndex, inIndex, nIndex, random.uniform(-1, 1))
            # pick an innner index to add the connection to
            else:
                inIndex = int(random.uniform(0, len(self.innerNodes)))
                # check to make sure the selected nodes to connect are different
                if not (inIndex == nIndex and outIndex == 1):
                    self.addConnection(1, outIndex, inIndex, nIndex, random.uniform(-1, 1))
        # remove
        else:
            if len(n.connections) > 0:
                conIndex = int(random.uniform(0, len(n.connections)))
                n.connections.pop(conIndex)

    # draws the current neural net to the pygame window
    def renderWithPygame(self, pyGui, centralHandler):
        # fill in the background
        pygame.draw.rect(pyGui, (255, 255, 255), (0, 0, 1800, 1000))

        # draw the input nodes
        if Settings.RELATIVE_NEURAL_INPUTS:
            game = centralHandler.tetrisDisplay
            xx = R_X - game.currentPiece.x * R_SQUARE
            yy = R_Y - game.currentPiece.y * R_SQUARE
        else:
            xx = R_X
            yy = R_Y

            if Settings.SPLIT_NEURAL_INPUTS:
                yy -= 200
        for i in range(len(self.inNodes)):
            n = self.inNodes[i]

            if n.value < 0:
                color = (255, 0, 0)
            elif n.value > 0:
                color = (127, 127, 127)
            else:
                if Settings.RELATIVE_INPUT_HEIGHT:
                    iX = i % Settings.RELATIVE_INPUT_WIDTH
                    iY = i // Settings.RELATIVE_INPUT_WIDTH
                else:
                    iX = i % Settings.GRID_WIDTH
                    iY = i // Settings.GRID_HEIGHT

                if (0 <= iX >= Settings.GRID_WIDTH and 0 <= iY >= Settings.GRID_HEIGHT
                        or not Settings.RELATIVE_NEURAL_INPUTS):
                    color = (255, 255, 255)
                else:
                    color = None

            rX = xx + n.renderPos[0]
            rY = yy + n.renderPos[1]
            if color is not None:
                pygame.draw.rect(pyGui, (0, 0, 0),
                                 (rX - R_SQUARE / 2,
                                  rY - R_SQUARE / 2,
                                  R_SQUARE, R_SQUARE))
                pygame.draw.rect(pyGui, color,
                                 (rX - R_SQUARE / 2 + R_THICK,
                                  rY - R_SQUARE / 2 + R_THICK,
                                  R_SQUARE - R_THICK * 2, R_SQUARE - R_THICK * 2))

        # draw all connections
        # out node connections
        for n in self.outNodes:
            if n.showLines:
                for c in n.connections:
                    if c.inType == 0:
                        pos = self.inNodes[c.inIndex].renderPos
                    else:
                        pos = self.innerNodes[c.inIndex].renderPos

                    lineT = 1
                    if c.inType == 1:
                        lineT = 3
                    renderLine(pyGui, pos, n.renderPos, c.weight, R_X, R_Y, lineT)

        # inner node connections
        for n in self.innerNodes:
            if n.showLines:
                for c in n.connections:
                    if c.inType == 0:
                        pos = self.inNodes[c.inIndex].renderPos
                    else:
                        pos = self.innerNodes[c.inIndex].renderPos

                    renderLine(pyGui, pos, n.renderPos, c.weight, R_X, R_Y, 3)

        # draw the inner nodes
        for n in self.innerNodes:
            if n.value < 0:
                val = 255 * -n.value
                val = max(0, min(255, val))
                color = (255, 255 - val, 255 - val)
            else:
                val = 255 * n.value
                val = max(0, min(255, val))
                color = (255 - val, 255 - val, 255)

            s = str(int(n.value * 1000))
            pygame.draw.ellipse(pyGui, (0, 0, 0),
                                (R_X + n.renderPos[0] - R_SIZE / 2,
                                 R_Y + n.renderPos[1] - R_SIZE / 2,
                                 R_SIZE, R_SIZE))
            pygame.draw.ellipse(pyGui, color,
                                (R_X + n.renderPos[0] - R_SIZE / 2 + R_THICK,
                                 R_Y + n.renderPos[1] - R_SIZE / 2 + R_THICK,
                                 R_SIZE - R_THICK * 2, R_SIZE - R_THICK * 2))

            font = pygame.font.SysFont('Impact', int(R_SIZE / 3))
            tx = R_X + n.renderPos[0] - 8
            ty = R_Y + n.renderPos[1]
            text = font.render(s, False, (0, 0, 0))
            pyGui.blit(text, (tx, ty))
            text = font.render(str(n.rank), False, (0, 0, 0))
            pyGui.blit(text, (tx, ty - (R_SIZE / 3 + 4)))

        # draw the output nodes
        for n in self.outNodes:
            if n.value < 0:
                val = 255 * -n.value
                val = max(0, min(255, val))
                color = (255, 255 - val, 255 - val)
            else:
                val = 255 * n.value
                val = max(0, min(255, val))
                color = (255 - val, 255 - val, 255)

            s = str(int(n.value * 1000))
            pygame.draw.ellipse(pyGui, (0, 0, 0),
                                (R_X + n.renderPos[0] - R_SIZE / 2,
                                 R_Y + n.renderPos[1] - R_SIZE / 2,
                                 R_SIZE, R_SIZE))
            pygame.draw.ellipse(pyGui, color,
                                (R_X + n.renderPos[0] - R_SIZE / 2 + R_THICK,
                                 R_Y + n.renderPos[1] - R_SIZE / 2 + R_THICK,
                                 R_SIZE - R_THICK * 2, R_SIZE - R_THICK * 2))

            font = pygame.font.SysFont('Impact', int(R_SIZE / 3))
            tx = R_X + n.renderPos[0] - 8
            ty = R_Y + n.renderPos[1]
            text = font.render(s, False, (0, 0, 0))
            pyGui.blit(text, (tx, ty))

    # move and update the positions of the neural net nodes based on the mouse events in pygame
    # returns true if there was an update to the state of the net, false otherwise
    def moveWithPygame(self):
        moved = False

        if not self.leftMouseDown:
            # check for each inner and out node
            moved = showHideLines(self.innerNodes) or showHideLines(self.outNodes) or moved

            self.leftMouseDown = True

        if not pygame.mouse.get_pressed()[0]:
            self.leftMouseDown = False

        # move ibky the inner nodes if applicable
        # only move if the right mosue button is pressed
        if pygame.mouse.get_pressed()[2] and self.moveNodeIndex < 0:
            for i in range(len(self.innerNodes)):
                n = self.innerNodes[i]
                # if a node was in range, move it to the mouse position
                if MiscUtil.distance(
                        (n.renderPos[0] + R_X, n.renderPos[1] + R_Y),
                        pygame.mouse.get_pos()
                ) <= R_SIZE / 2:

                    # set the index to the current node
                    self.moveNodeIndex = i
                    break
        elif not pygame.mouse.get_pressed()[2]:
            self.moveNodeIndex = -1

        if self.moveNodeIndex >= 0:
            p = pygame.mouse.get_pos()
            self.innerNodes[self.moveNodeIndex].renderPos = (p[0] - R_X, p[1] - R_Y)
            moved = True

        return moved

    # reder = True: show all connection lines
    # render = False: hide all conneciton lines
    def setAllConnectionRender(self, render):
        if render:
            for n in self.innerNodes:
                n.showLines = True
            for n in self.outNodes:
                n.showLines = True
        else:
            for n in self.innerNodes:
                n.showLines = False
            for n in self.outNodes:
                n.showLines = False

    # fileWriter: an opened fileWriter in write mode
    # this should print all of the data for this neural net to the text file of that writer
    def save(self, fileWriter):
        # save general info
        fileWriter.write(str(self.id) + '\n')
        fileWriter.write(str(self.parentId) + '\n')
        fileWriter.write(str(self.birthGen) + '\n')
        fileWriter.write(str(self.fitness) + '\n')
        fileWriter.write(str(self.mutability) + '\n')
        fileWriter.write(str(self.tested) + '\n')

        # save innerNodes
        fileWriter.write(str(len(self.innerNodes)) + '\n')
        for n in self.innerNodes:
            n.save(fileWriter, False)

        # save outNodes
        fileWriter.write(str(len(self.outNodes)) + '\n')
        for n in self.outNodes:
            n.save(fileWriter, True)

    # fileWriter: an opened fileReader in read mode
    # this should load in all the data from the given file reader
    # the file must be at a valid line to load in the settings
    def load(self, fileReader):
        # load general info
        self.id = SaveLoader.intLine(fileReader.readline())
        self.parentId = SaveLoader.intLine(fileReader.readline())
        self.birthGen = SaveLoader.intLine(fileReader.readline())
        self.fitness = SaveLoader.floatLine(fileReader.readline())
        self.mutability = SaveLoader.floatLine(fileReader.readline())
        self.tested = SaveLoader.loadBoolean("b: " + fileReader.readline())

        # set up in nodes
        NeuralNetHandler.determineRenderVars()
        self.inNodes = []
        if Settings.SPLIT_NEURAL_INPUTS:
            for i in range(NeuralNetHandler.R.w * NeuralNetHandler.R.h * 2):
                self.inNodes.append(Node(0))
        else:
            for i in range(NeuralNetHandler.R.w * NeuralNetHandler.R.h):
                self.inNodes.append(Node(0))
        NeuralNetHandler.setInNodeRenderPos(self)

        # load inner nodes
        numNodes = SaveLoader.intLine(fileReader.readline())
        self.innerNodes = []
        for i in range(numNodes):
            n = Node(0)
            n.load(fileReader, False)
            self.innerNodes.append(n)

        # load outNodes
        numNodes = SaveLoader.intLine(fileReader.readline())
        self.outNodes = []
        for i in range(numNodes):
            n = Node(0)
            n.load(fileReader, True)
            self.outNodes.append(n)
        NeuralNetHandler.setOutNodeRenderPos(self)


# decides if each node in the given node list should be shown or hidden
# returns True if a line was changed, False otherwise
def showHideLines(nodes):
    # if the mouse was left clicked, then check if lines should be changed
    if pygame.mouse.get_pressed()[0]:
        for n in nodes:
            # check if the mouse is on a node
            if MiscUtil.distance((n.renderPos[0] + R_X, n.renderPos[1] + R_Y),
                                 pygame.mouse.get_pos()) <= R_SIZE / 2:
                # make the liens going into that node hidden or not hidden
                n.showLines = not n.showLines
                return True
    return False


# draws a NeuralNet line from the renderPos positions from 2 nodes, the line has the givne weight
# should only be used by renderWithPygame method
# x, y is the coordinates of the initial position of the net being drawn
# thick is the line thickness
def renderLine(pyGui, pos1, pos2, weight, x, y, thick):
    # determine color of line
    if weight < 0:
        val = 255 * -weight
        val = max(0, min(255, val))
        color = (255, 255 - val, 255 - val)
    else:
        val = 255 * weight
        val = max(0, min(255, val))
        color = (255 - val, 255 - val, 255)

    pygame.draw.line(pyGui, color, (x + pos1[0], y + pos1[1]), (x + pos2[0], y + pos2[1]), thick)


class Node:

    def __init__(self, bias):
        # the bias that this node has when determining its output
        self.bias = bias
        # the current value of this node
        self.value = 0

        # true if this node has already been calculated by the connections feeding into it
        # false otherwise
        self.calculated = False

        # the connectiosn going into this node
        self.connections = []

        # used only by inner nodes
        # this value dtermines its relative position to other inner nodes
        # inner nodes can only feed their falues to nodes with higher rank values, or output nodes
        # the first inner node has a rank of 0, then all furture inner nodes are based on that node rank
        # if the new node is added on a conection between an inner node and outer node, then the rank of the new
        #   inner node is that of the connected inner node's rank plus 1
        # if the new node is added on a connection between an inner node and input node, then the rank of the new
        #   inner node is that of the connected inner node's rank minus 1
        # if the node is added on a connections between two inner nodes, then the rank is the average of those 2
        # node's ranks
        # this ensures that no infinite connection loops occur betwen inner nodes
        self.rank = 0

        # the point (x, y) on the screen this node is rendered, only used by the pygame render method
        # the position is the center of the node
        self.renderPos = (0, 0)

        # True if the lines feeding into this node should be rendered, false otherwise
        self.showLines = True

    def setRenderPos(self, x, y):
        self.renderPos = (x, y)

    # determine value based on the given inputs
    # inputs must be a list of equal length to connections
    # also returns the calculated value
    def calculateValue(self, inputs):
        self.value = self.bias
        for i in range(len(inputs)):
            self.value += inputs[i] * self.connections[i].weight

        self.value = sigmoid(self.value)

        self.calculated = True
        return self.value

    def setCalculated(self, calculated):
        self.calculated = calculated

    def setRank(self, r):
        self.rank = r

    def setBias(self, bias):
        self.bias = bias
        # ensure the bias stays in the range (-1, 1)
        self.bias = min(1, max(-1, self.bias))

    # inType: the type of node that this connection is comming from
    #       0: input node
    #       1: inner node
    # inIndex: the index of the list that this connection connects to
    # weight: the weight of the connection
    def addConnection(self, inType, inIndex, weight):
        self.connections.append(Connection(inType, inIndex, weight))

    # randomly change the weights of all the connections and the bias of this node
    def mutate(self, mutability):
        # mudate bias
        self.setBias(self.bias + random.uniform(-mutability, mutability) * Settings.WEIGHT_BIAS_SCALAR)

        # mutate connections
        for c in self.connections:
            c.setWeight(c.weight + random.uniform(-mutability, mutability * Settings.WEIGHT_BIAS_SCALAR))

    # fileWriter: an opened fileWriter in write mode
    # outNode: True if this node is an out node, false otherwise
    # this should print all of the settings to the text file of that writer
    def save(self, fileWriter, outNode):
        # save general info
        fileWriter.write(str(self.bias) + '\n')
        if not outNode:
            fileWriter.write(str(self.rank) + '\n')
            fileWriter.write(str(self.renderPos[0]) + '\n')
            fileWriter.write(str(self.renderPos[1]) + '\n')

        # save connections
        fileWriter.write(str(len(self.connections)) + '\n')
        for c in self.connections:
            c.save(fileWriter)

    # fileWriter: an opened fileReader in read mode
    # outNode: True if this node is an out node, false otherwise
    # this should load in all the data from the given file reader
    # the file must be at a valid line to load in the settings
    def load(self, fileReader, outNode):
        # load general info
        self.bias = SaveLoader.floatLine(fileReader.readline())
        if not outNode:
            self.rank = SaveLoader.floatLine(fileReader.readline())
            x = SaveLoader.floatLine(fileReader.readline())
            y = SaveLoader.floatLine(fileReader.readline())
            self.setRenderPos(x, y)

        numConnections = SaveLoader.intLine(fileReader.readline())

        self.connections = []
        # load connections
        for i in range(numConnections):
            c = Connection(0, 0, 0)
            c.load(fileReader)
            self.connections.append(c)


class Connection:

    # inType: the type of node that this connection feeds out of
    #       0: input node
    #       1: inner node
    # inIndex: the index of the node that this connection feeds out of in the in list
    # weight: the weight of this ocnnection
    def __init__(self, inType, inIndex, weight):
        self.inType = inType
        self.inIndex = inIndex
        self.weight = weight

    def setWeight(self, weight):
        self.weight = weight
        # ensure the weight stays in the range (-1, 1)
        self.weight = min(1, max(-1, self.weight))

    def setInIndex(self, i):
        self.inIndex = i

    # fileWriter: an opened fileWriter in write mode
    # this should print all of the settings to the text file of that writer
    def save(self, fileWriter):
        fileWriter.write(str(self.inType) + '\n')
        fileWriter.write(str(self.inIndex) + '\n')
        fileWriter.write(str(self.weight) + '\n')

    def load(self, fileReader):
        self.inType = SaveLoader.intLine(fileReader.readline())
        self.inIndex = SaveLoader.intLine(fileReader.readline())
        self.weight = SaveLoader.floatLine(fileReader.readline())


def sigmoid(x):
    return 2.0 / (1.0 + pow(math.e, -x)) - 1
