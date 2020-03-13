import random
import pygame
import time
import Settings

# the number of diferent tile types that exist of Tetris peices
NUM_TILE_TYPES = 7


class Tetris:

    def __init__(self):

        # variables to keep track of pieces placed and removed for scoring
        self.piecesPlaced = 0
        self.rowsRemoved = 0
        # the fitness of the game based on pieces placed and rows removed, and the position they were removed at
        self.fitness = 0

        self.gameOver = False

        self.grid = [[]]
        self.gridColors = [[]]

        # variable for the current piece
        self.currentPiece = None

        # variable for keeping track of which piece the game is on in the sequence.
        # Only used when not Settings.PIECE_SEQUENCE = []
        self.pieceCounter = 0

        self.resetGame()

    # brings the game to a default state, also sets the random seed to 0 to ensure that each time the
    # game is played the same shapes are generated
    def resetGame(self):
        if Settings.SET_SEED:
            random.seed(Settings.SET_SEED_GAMES[0])
        else:
            random.seed(time.time())

        self.piecesPlaced = 0
        self.rowsRemoved = 0
        self.fitness = 0

        self.gameOver = False

        self.grid = [[]]
        self.gridColors = [[]]
        for i in range(Settings.GRID_WIDTH):
            self.grid.append([])
            self.gridColors.append([])
            for j in range(Settings.GRID_HEIGHT):
                self.grid[i].append(False)
                self.gridColors[i].append((255, 255, 255))

        self.pieceCounter = 0
        self.makeNewPiece()

    def makeNewPiece(self):
        p = Settings.PIECE_SEQUENCE
        if len(p) == 0:
            # set the current piece to a randpm peice
            r = int(random.uniform(0, NUM_TILE_TYPES))
            self.currentPiece = TetrisShape(r)
            for i in range(int(random.uniform(0, 3))):
                self.currentPiece.rotatePiece(True)
        else:
            if self.pieceCounter >= len(p):
                self.pieceCounter = 0
            self.currentPiece = TetrisShape(p[self.pieceCounter][0])
            for i in range(p[self.pieceCounter][1]):
                self.currentPiece.rotatePiece(True)
            self.pieceCounter += 1

        # shift piece over
        self.currentPiece.x += int(Settings.GRID_WIDTH * .4)

    # uses pygame and draws the current game state to the pygame window, doesn't draw a background at all
    def renderWithPygame(self, pyGui, centralHsndeler):
        # draw the grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(pyGui, (0, 0, 0),
                                 (getPixelX(i), getPixelY(j),
                                  Settings.GRID_SIZE, Settings.GRID_SIZE))
                color = self.gridColors[i][j]
                pygame.draw.rect(pyGui, color,
                                 (getPixelX(i) + Settings.GRID_LINE,
                                  getPixelY(j) + Settings.GRID_LINE,
                                  Settings.GRID_SIZE - Settings.GRID_LINE * 2,
                                  Settings.GRID_SIZE - Settings.GRID_LINE * 2))

        # draw the current piece
        c = self.currentPiece
        for i in range(len(self.currentPiece.tiles)):
            x = c.getX(i)
            y = c.getY(i)
            if 0 <= x < Settings.GRID_WIDTH and 0 <= y < Settings.GRID_HEIGHT:
                fadeColor = self.currentPiece.getColor()
                fadeColor = (
                    min(255, fadeColor[0] + (255 - fadeColor[0]) * .5),
                    min(255, fadeColor[1] + (255 - fadeColor[0]) * .5),
                    min(255, fadeColor[2] + (255 - fadeColor[0]) * .5)
                )
                pygame.draw.rect(pyGui, fadeColor,
                                 (Settings.GRID_X + x * Settings.GRID_SIZE + Settings.GRID_LINE,
                                  Settings.GRID_Y + y * Settings.GRID_SIZE + Settings.GRID_LINE,
                                  Settings.GRID_SIZE - Settings.GRID_LINE * 2,
                                  Settings.GRID_SIZE - Settings.GRID_LINE * 2))

        # draw the current number of pieces and rows score
        font = pygame.font.SysFont('Impact', 20)
        text = font.render("Pieces: " + str(self.piecesPlaced), False, (0, 0, 0))
        pyGui.blit(text,
                   (Settings.GRID_X + Settings.GRID_WIDTH * Settings.GRID_SIZE + 10,
                    Settings.GRID_Y + Settings.GRID_HEIGHT * Settings.GRID_SIZE * .5))
        text = font.render("Rows: " + str(self.rowsRemoved), False, (0, 0, 0))
        pyGui.blit(text,
                   (Settings.GRID_X + Settings.GRID_WIDTH * Settings.GRID_SIZE + 10,
                    Settings.GRID_Y + Settings.GRID_HEIGHT * Settings.GRID_SIZE * .5 + 23))
        text = font.render("Fitness: " + str(self.fitness), False, (0, 0, 0))
        pyGui.blit(text,
                   (Settings.GRID_X + Settings.GRID_WIDTH * Settings.GRID_SIZE + 10,
                    Settings.GRID_Y + Settings.GRID_HEIGHT * Settings.GRID_SIZE * .5 + 46))

        # if the game is over draw it
        if self.gameOver:
            text = font.render("Game Over!", False, (0, 0, 0))
            pyGui.blit(text,
                       (Settings.GRID_X + Settings.GRID_WIDTH * Settings.GRID_SIZE + 10,
                        Settings.GRID_Y + Settings.GRID_HEIGHT * Settings.GRID_SIZE * .3 + 23))

        # draw instructions for which keyboard keys play the game
        strs = [
            "P: pause/unpause game, currently: ",
            "A: toggle AI or player controlled, currently: ",
            "Up arrow: rotate counter clockwise",
            "Down arrow: rotate clockwise",
            "Left arrow: move left",
            "Up arrow: move right",
            "Space: go down one row",
            "Enter: move down until the piece is placed down",
            "R: reset game",
            "F: toggle game/graph view",
            "G/H/J: show fitness/mutability/generations graph",
            "Left click node: toggle show connections",
            "Right click/drag node: move node",
            "N/M: show/hide all connections"
        ]
        if centralHsndeler.tetrisHandler.running:
            strs[0] += "Unpaused"
        else:
            strs[0] += "Paused"

        if centralHsndeler.tetrisHandler.aiControl:
            strs[1] += "AI"
        else:
            strs[1] += "Player"

        for i in range(len(strs)):
            text = font.render(strs[i], False, (0, 0, 0))
            pyGui.blit(text,
                       (Settings.GRID_X + Settings.GRID_WIDTH * Settings.GRID_SIZE + 10,
                        Settings.GRID_Y + Settings.GRID_HEIGHT * Settings.GRID_SIZE * .85 + i * 23 - 20))

    # moves the current peice that the player controls to the next line
    # if the peice cannot move downwards anymore, the piece is placed down,
    # a new piece is generated at the top, and any lines that should be removed
    # are removed and all the other peices are shitfed down
    # returns true if the current piece was placed down, false otherwise
    def nextLine(self):
        # if the game is over, do nothing
        if self.gameOver:
            return

        # will be true if the peice should be placed down
        place = False
        # determine if the piece should be placed down
        for i in range(len(self.currentPiece.tiles)):
            x = self.currentPiece.getX(i)
            y = self.currentPiece.getY(i) + 1
            if y >= Settings.GRID_HEIGHT:
                place = True
                break

            if 0 <= x < Settings.GRID_WIDTH and 0 <= y:
                if self.grid[x][y]:
                    place = True
                    break

        # place the piece
        if place:
            # add one to the piece score
            self.piecesPlaced += 1
            # find the lowest tile in the current piece, meaning the highest index
            low = 0
            for i in range(len(self.currentPiece.tiles)):
                if self.currentPiece.getY(i) + 1 > low:
                    low = self.currentPiece.getY(i) + 1
            low = min(Settings.GRID_HEIGHT, low)
            # this bases fitness gains explonetially, the further down the piece lands, the higher fitness gained
            y = Settings.FITNESS_PIECE / pow(2, max(0, Settings.GRID_HEIGHT - low))

            # if applicable, multiply fitness by the percentage of the empty grid
            if Settings.USE_FILLED_FOR_FITNESS:
                # for size of filled grid
                empty = 0
                total = 0
                # check each of the spots in the grid and count the number of filed ones
                for i in self.grid:
                    for j in i:
                        if not j:
                            empty += 1
                        total += 1
                # multiply the fitness to add by the percent of the filled grid
                if total is not 0:
                    y = y * (empty / total)

            # add the appropritae amount of fitness based on where the piece was placed
            self.fitness += y

            for i in range(len(self.currentPiece.tiles)):
                x = self.currentPiece.getX(i)
                y = self.currentPiece.getY(i)

                # if one of the pieces is above the grid or placed in a spot thats filled, then the game is over
                if y < 0 or 0 <= x < len(self.grid) and self.grid[x][y]:
                    self.endGame()
                    return

                # set colors of piece
                if 0 <= x < Settings.GRID_WIDTH and 0 <= y < Settings.GRID_HEIGHT:
                    self.grid[x][y] = True
                    self.gridColors[x][y] = self.currentPiece.getColor()
            self.makeNewPiece()
        else:
            self.currentPiece.y += 1

        # now check to see if any lines need to be removed
        # for each row
        for i in range(Settings.GRID_HEIGHT):
            # check if that row is filled
            rowFull = True
            for j in range(Settings.GRID_WIDTH):
                if not self.grid[j][i]:
                    rowFull = False
                    break

            # if the row is filled, it must be removed
            if rowFull:
                # add one to the row score
                self.rowsRemoved += 1
                self.fitness += max(1.0, min(Settings.FITNESS_LINE, 10 * ((i + 1) / Settings.GRID_HEIGHT)))

                # delete the full row
                for j in range(Settings.GRID_WIDTH):
                    self.grid[j][i] = False
                    self.gridColors[j][i] = (255, 255, 255)

                # shift each row down
                for y in range(i):
                    for j in range(Settings.GRID_WIDTH):
                        self.grid[j][i - y] = self.grid[j][i - y - 1]
                        self.gridColors[j][i - y] = self.gridColors[j][i - y - 1]

                # delete the top row
                for j in range(Settings.GRID_WIDTH):
                    self.grid[j][0] = False
                    self.gridColors[j][0] = (255, 255, 255)

        return place

    # the game has ended, so the final fintes calculation msut happen
    def endGame(self):
        # add more fitness based on the percentage of the filled board at the end of the game
        self.fitness += self.calculateFitnessDensity()
        # game is now over
        self.gameOver = True

    # advances the current piece down until it is placed
    def snapPieceDown(self):
        while True:
            if self.nextLine():
                break

    # move the current piece on the x plane by the given number.
    # if the new position of the piece places it outside the grid, it will be automatically readjusted
    # returns True if the piece was moved, false otherwise
    def movePiece(self, x):
        # keeps track of the old x value to return if the piece was moved
        oldX = self.currentPiece.x

        if self.currentPiece is None:
            return False

        # set the new position of the current piece
        self.currentPiece.x += x

        # check to see if the current piece is now in a tile, if it is, then the movement of the tile will be undone
        if self.currentPieceInTile():
            self.currentPiece.x -= x

        # ensure that the current piece remains in the grid
        offset = 0
        for i in range(len(self.currentPiece.tiles)):
            tX = self.currentPiece.tiles[i].x + self.currentPiece.x
            if abs(offset) < abs(tX):
                if tX < 0:
                    offset = tX
                elif tX > Settings.GRID_WIDTH - 1:
                    offset = tX - (Settings.GRID_WIDTH - 1)
        self.currentPiece.x -= offset

        return not oldX == self.currentPiece.x

    # rotates the currentt piece
    # use up = True to rotate counter clock wise
    # use up = False to rotate clock wise
    # returns True if the piece was moved, false otherwise
    def rotateCurrentPiece(self, up):
        moved = True

        # attempt to rotate the pieice, if it becomes in an existing tile or
        # outside the grid on the left, right, or bottom, the undo the rotation
        self.currentPiece.rotatePiece(up)
        if self.currentPieceInTile():
            self.currentPiece.rotatePiece(not up)
            moved = False
        # now check for the piece being outside the grid
        for i in range(len(self.currentPiece.tiles)):
            x = self.currentPiece.getX(i)
            y = self.currentPiece.getY(i)
            if x < 0 or x >= Settings.GRID_WIDTH or y >= Settings.GRID_HEIGHT:
                self.currentPiece.rotatePiece(not up)
            moved = False

        return moved

    # returns true if the current piece is inside an existing tile
    def currentPieceInTile(self):
        inside = False
        for i in range(len(self.currentPiece.tiles)):
            tx = self.currentPiece.getX(i)
            ty = self.currentPiece.getY(i)
            if 0 <= tx < Settings.GRID_WIDTH and 0 <= ty < Settings.GRID_HEIGHT:
                if self.grid[tx][ty]:
                    inside = True
                    break
        return inside

    # calculate the fitness percentage of the game based on the tiles remaining
    # the value returned is 5 for 100%
    # this is to make the fitness values more useful to look at
    def calculateFitnessDensity(self):
        if Settings.FITNESS_SCALAR == 0:
            return 0

        cnt = 0
        tot = 0
        for i in self.grid:
            for j in i:
                if j:
                    cnt += 1
                tot += 1

        if tot > 0:
            return Settings.FITNESS_SCALAR * (cnt / tot)
        return Settings.FITNESS_SCALAR


# get a x coordinate to draw a pixel to the screen based on the given x index
def getPixelX(x):
    return Settings.GRID_X + Settings.GRID_SIZE * x


# get a y coordinate to draw a pixel to the screen based on the given y index
def getPixelY(y):
    return Settings.GRID_Y + Settings.GRID_SIZE * y


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# an object that keeps track of all the data of a piece in tetris
class TetrisShape:

    # tileId: the name of the tile type that should be created
    # Potential names:
    # 0: the 2x2 tile
    # 1: the 4x1 tile
    # 2: the 3x1 tile with a piece in the middle
    # 3: the 3x1 tile with a piece that makes it look like an L
    # 4: the other variant of the L shape
    # 5: the peice that is a 2x2 with the top row shifted to the left
    # 6: the peice that is a 2x2 with the top row shifted to the right
    def __init__(self, tileId):
        # tiles are kept track of in relative coordinates to the main peice position
        # this means that the coordinates in tiles are nor the actual coordinates on the tetris game,
        # but must be added to x and y
        self.x = 0
        self.y = 0

        self.tileId = tileId

        self.tiles = []
        # all tile types must consider (0, 0) as the center

        # OO
        # OO
        if tileId == 0:
            self.tiles.append(Point(-1, -1))
            self.tiles.append(Point(0, -1))
            self.tiles.append(Point(-1, 0))
            self.tiles.append(Point(0, 0))

        # OOOO
        elif tileId == 1:
            for i in range(4):
                self.tiles.append(Point(i - 2, -1))

        # OOO
        #  O
        elif tileId == 2:
            for i in range(3):
                self.tiles.append(Point(i - 1, 0))
            self.tiles.append(Point(0, 1))

        # OOO
        #   O
        elif tileId == 3:
            for i in range(3):
                self.tiles.append(Point(0, i - 1))
            self.tiles.append(Point(1, 1))

        # OOO
        # O
        elif tileId == 4:
            for i in range(3):
                self.tiles.append(Point(0, i - 1))
            self.tiles.append(Point(-1, 1))

        # OO
        #  OO
        elif tileId == 5:
            self.tiles.append(Point(-1, 0))
            self.tiles.append(Point(0, 0))
            self.tiles.append(Point(0, 1))
            self.tiles.append(Point(1, 1))

        #  OO
        # OO
        elif tileId == 6:
            self.tiles.append(Point(0, 0))
            self.tiles.append(Point(1, 0))
            self.tiles.append(Point(-1, 1))
            self.tiles.append(Point(0, 1))

        self.tlieId = tileId

    def getColor(self):
        # OO
        # OO
        if self.tileId == 0:
            return 255, 255, 0

        # OOOO
        elif self.tileId == 1:
            return 0, 255, 255

        # OOO
        #  O
        elif self.tileId == 2:
            return 200, 0, 255

        # OOO
        #   O
        elif self.tileId == 3:
            return 255, 0, 0

        # OOO
        # O
        elif self.tileId == 4:
            return 0, 0, 255

        # OO
        #  OO
        elif self.tileId == 5:
            return 255, 127, 0

        #  OO
        # OO
        elif self.tileId == 6:
            return 0, 200, 0

        return 0, 0, 0

    # get the x coordinate of the ith tile in the list
    def getX(self, i):
        return self.tiles[i].x + self.x

    # get the y coordinate of the ith tile in the list
    def getY(self, i):
        return self.tiles[i].y + self.y

    # rotates this currentt piece
    # use up = True to rotate counter clock wise
    # use up = False to rotate clock wise
    def rotatePiece(self, up):

        # center point is based on (0, 0) and size

        # if the piece is the square, then do nothing
        if self.tileId == 0:
            return

        # rotate around center
        for p in self.tiles:
            if up:
                old = p.x
                p.x = p.y
                p.y = -old
            else:
                old = p.y
                p.y = p.x
                p.x = -old
