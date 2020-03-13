import pygame

import SaveLoader


# the higest the absolute value of a zoom can be
MAX_ZOOM_X = 30
MAX_ZOOM_Y = 30


class LineGraph:

    # lines: the lines that should be used to render this graph, should be a list
    def __init__(self, lines):
        self.lines = lines

        # a list of boolean values that determine if the data line with the corresponding index shoudl be rendered
        self.displayLines = []
        for i in range(len(lines)):
            self.displayLines.append(True)

        # last time where grpah was rendered
        self.lastX = 0
        self.lastY = 0
        self.lastWidth = 0
        self.lastHeight = 0

        # the coordinates of where the graph is currently rendered on the screen, relative to the (x, y) coordniates
        # that are sent by the renderWithPyGame method
        self.renderPos = (0, 0)

        # the coordinates of what is added to the render position given as parameters to the renderWithPygame method
        self.renderAdd = (0, 0)

        # keeps track of where the mouse was pressed last for moving graph around
        self.anchorPos = (0, 0)
        # true if the mouse has been pressed since the anchor position was set
        self.anchored = False

        # the variable put into an exponential equation to zoom in and out
        # negative numbers zoom in, positive numbers zoom out, zero is default position
        self.xZoomFactor = 0
        self.yZoomFactor = 0

    # moves the graph based on how the mouse is
    def moveWithPygame(self):

        # if left click is pressed, reste graph and quit
        if pygame.mouse.get_pressed()[0]:
            self.anchored = False
            self.anchorPos = (0, 0)
            self.renderPos = (0, 0)
            self.renderAdd = (0, 0)
            self.xZoomFactor = 0
            self.yZoomFactor = 0

        # if the mouse is pressed
        if pygame.mouse.get_pressed()[2]:
            # anchord the mouse if it isn't anchored
            if not self.anchored:
                self.anchorPos = pygame.mouse.get_pos()
                self.anchored = True

            # if the mouse is anchord, move the render pos based on the mouse position
            if self.anchored:
                pos = pygame.mouse.get_pos()
                self.renderAdd = (pos[0] - self.anchorPos[0],
                                  pos[1] - self.anchorPos[1])

        # if the mouse is not pressed, release the anchor
        else:
            self.anchored = False
            self.renderPos = (self.renderPos[0] + self.renderAdd[0],
                              self.renderPos[1] + self.renderAdd[1])
            self.renderAdd = (0, 0)

        # see if the mouse wheel was moved
        pressed = pygame.key.get_pressed()
        shift = pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]
        ctrl = pressed[pygame.K_RCTRL] or pressed[pygame.K_LCTRL]

        zoomed = False
        # the position, in graph coordinates, of the mouse before any zooming
        mouse = pygame.mouse.get_pos()
        graphPos = (
            (mouse[0] - (self.renderAdd[0] + self.renderPos[0]) - self.lastX) / getScale(self.xZoomFactor),
            (mouse[1] - (self.renderAdd[1] + self.renderPos[1]) - self.lastY) / getScale(self.yZoomFactor)
        )

        # zoom in and out
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # zoom in
                if event.button == 4:
                    if not ctrl:
                        self.xZoomFactor += 1
                        zoomed = True
                    if not shift:
                        self.yZoomFactor += 1
                        zoomed = True

                # zoom out
                elif event.button == 5:
                    if not ctrl:
                        self.xZoomFactor -= 1
                        zoomed = True
                    if not shift:
                        self.yZoomFactor -= 1
                        zoomed = True

        if zoomed:
            # reset anchor
            self.anchored = False
            self.anchorPos = (0, 0)
            self.renderAdd = (0, 0)

            # adjust render pos based on mouse position during zoom
            self.renderPos = (
                mouse[0] - graphPos[0] * getScale(self.xZoomFactor) - self.lastX,
                mouse[1] - graphPos[1] * getScale(self.yZoomFactor) - self.lastY
            )

        # keep zoom factors to managable levels
        self.xZoomFactor = max(-MAX_ZOOM_X, min(MAX_ZOOM_X, self.xZoomFactor))
        self.yZoomFactor = max(-MAX_ZOOM_Y, min(MAX_ZOOM_Y, self.yZoomFactor))

        # ensure the render pos doesn't get out of the screen
        x = self.renderPos[0]
        y = self.renderPos[1]
        size = pygame.display.get_surface().get_size()

        xScale = getScale(self.xZoomFactor)
        yScale = getScale(self.yZoomFactor)

        x = max(10 - self.lastWidth * xScale, min(size[0] - 10, x))
        y = max(10 - self.lastHeight * yScale, min(size[1] - 10, y))

        self.renderPos = (x, y)

    # draw this graph on the given pygame gui at the specificied coordinates (x, y)
    # x: the lefthand side of the graph
    # y: the upper leftHand corner
    # width: the horizontal space the grpah should be streched in its rendering on the screen
    # height: the vertical space the grpah should be streched in its rendering on the screen
    def renderWithPygame(self, x, y, width, height, pyGui):

        self.lastX = x
        self.lastY = y
        self.lastWidth = width
        self.lastHeight = height

        x += self.renderPos[0] + self.renderAdd[0]
        y += self.renderPos[1] + self.renderAdd[1]

        width *= getScale(self.xZoomFactor)
        height *= getScale(self.yZoomFactor)

        # draw a box that the graph should stay in
        pygame.draw.rect(pyGui, (230, 230, 230), (x, y, width, height))

        # the amount of horizontal space the graph will display, numerical space, not the space that is displayed
        highData = 0

        # find the highest and lowest data values on the graph, finding the bounds of the graphs values
        # find the line with the most data points
        high = 0
        low = 0
        started = False
        for l in self.lines:
            for d in l.data:
                if started:
                    high = max(high, d)
                    low = min(low, d)
                else:
                    high = d
                    low = d
                    started = True

            highData = max(highData, len(l.data))

        # if no data is present, indecated that no lines have any data points, then draw nothing else
        if highData == 0:
            return

        # if only one data point is present ensure that the graph will render that point relative to the origin
        if high == low:
            if high > 0:
                low = 0
            else:
                high = 0

        # the amount of vertical space the graph will display, numerical space, not the space that is displayed
        numHeight = abs(high - low)

        # if there is only one point, make a default height

        # the space between x coordinate points
        xSpace = width / highData

        # the number that is multiplied by data points to find their relative position on the screen, not accounting
        # for the change in the space that the graph is chosen to display at
        if not numHeight == 0:
            yScale = height / numHeight
        else:
            yScale = 1

        # the yPosition of the origin as displayed on the screen
        # the origin is not always displayed, depending on where data points are show
        # this coordinate is relative to the x and y positions that the graph should be rendered at

        if not numHeight == 0:
            yOrigin = (high + low) * yScale - height * (low / numHeight)
        else:
            yOrigin = y + height / 2
        if high < 0:
            yOrigin = high * yScale
        elif low > 0:
            yOrigin = low * yScale + height

        # font for the graph numbers
        font = pygame.font.SysFont('Impact', 15)

        # the number of missing vertical lines between each vertical line, assuming initially one line for each integer
        modNum = int(max(1, 40 / xSpace))

        # draw vertical lines representing the different indexes of the data points
        for i in range(highData + 1):
            if i % modNum == 0:
                # x coordinate of the line
                lineX = i / highData * width + x
                # draw the line
                pygame.draw.line(pyGui, (150, 150, 150), (lineX, y), (lineX, y + height), 1)

                # draw the text
                textY = min(pyGui.get_size()[1] - 20, y + height)

                if 0 < lineX < pyGui.get_size()[0]:
                    text = font.render(str(i), False, (0, 0, 0))
                    pyGui.blit(text, (lineX, textY))

        # the space between lines on the screen
        yLineSpace = 30

        # the number of lines that will be rendered that show values of data points
        horizontalLines = int(height / yLineSpace)

        # the indexes away from the origin line that the highest line on the screen will be rendered
        # first the space above the origin the high value is in pixel coordinates
        # that pixel value is divided by the number pixels in between spaces, giving the number of lines
        highIndex = int((high * yScale) / yLineSpace)

        # draw horizontal lines showing the values of the data points
        i = 0
        while i < horizontalLines:
            # the y coordinate of the line on the graph
            graphY = (highIndex - i) * (yLineSpace / yScale)

            # the y coorindate of the pixel that the line is drawn
            pixY = yOrigin - graphY * yScale

            # the weight of the line, thicker if it is the origin line
            if graphY == 0:
                stroke = 2
            else:
                stroke = 1

            pygame.draw.line(pyGui, (150, 150, 150),
                             (x - 60, y + pixY), (x + width, y + pixY),
                             stroke)

            # draw the text label
            textX = max(x - 60, 0)
            textY = y + pixY - 18
            # only render the text if it will be on screen
            if 0 < textY < pyGui.get_size()[1]:
                text = font.render(str(round(graphY,
                                             max(2, (min(6, int(2 + self.yZoomFactor))))
                                             )),
                                   False, (0, 0, 0))
                pyGui.blit(text, (textX, textY))

            i += 1

        # draw each graph line, the data point lines that is
        for index in range(len(self.lines)):
            if self.displayLines[index]:
                line = self.lines[index]

                d = line.data

                # variables to keep track of where the lines will be drawn
                # these are pixel coordinates, not mathematical ones
                # data points in d are the absolute positions on the graph

                # the coordinates of the left point of the line
                drawX1 = 0
                drawY1 = yOrigin

                # go through each data point, starting the first point at y = 0
                i = 0
                while i < len(d):
                    # calculate the coordinates of the left right of the line
                    drawX2 = drawX1 + xSpace
                    drawY2 = yOrigin - d[i] * yScale

                    # draw the line
                    pygame.draw.line(pyGui, line.color, (drawX1 + x, drawY1 + y), (drawX2 + x, drawY2 + y), line.stroke)

                    # the old coordinates for the righthand point become the new coordinates for the lefthand
                    drawX1 = drawX2
                    drawY1 = drawY2

                    i += 1

    # add a piece of data a line on the graph
    # index: the index of the line
    # num: the new piece of data to add to the graph
    def addData(self, index, num):
        self.lines[index].data.append(num)

    # fileWriter: an opened fileWriter in write mode
    # this should print all of the settings to the text file of that writer
    def save(self, fileWriter):
        # save lines
        fileWriter.write(str(len(self.lines)) + '\n')
        for l in self.lines:
            l.save(fileWriter)

    # fileWriter: an opened fileReader in read mode
    # this should load in all the data from the given file reader
    # the file must be at a valid line to load in the settings
    def load(self, fileReader):
        self.lines = []
        numLines = SaveLoader.intLine(fileReader.readline())
        for i in range(numLines):
            line = GraphLine((0, 0, 0), 0)
            line.load(fileReader)
            self.lines.append(line)


def getScale(num):
    return pow(1.3, num)


class GraphLine:

    # color should be a touple (r, g, b) like in pygame
    # color: the color of the line
    # stroke: the width of the line
    def __init__(self, color, stroke):
        self.color = color
        self.stroke = stroke
        # a list of numbers, the data that this line contains
        # the index that the data is in represents its x coordinate
        # this type of line should only be used when x axis is meant to be in integers
        self.data = []

    # fileWriter: an opened fileWriter in write mode
    # this should print all of the settings to the text file of that writer
    def save(self, fileWriter):
        # save general data
        fileWriter.write(str(self.color[0]) + ' ' + str(self.color[1]) + ' ' + str(self.color[2]) + '\n')
        fileWriter.write(str(self.stroke) + '\n')

        # save data points
        for d in self.data:
            fileWriter.write(str(d) + ' ')
        fileWriter.write('\n')

    # fileWriter: an opened fileReader in read mode
    # this should load in all the data from the given file reader
    # the file must be at a valid line to load in the settings
    def load(self, fileReader):
        line = fileReader.readline()
        c = [int(s) for s in line.split()]
        self.color = (c[0], c[1], c[2])
        self.stroke = SaveLoader.intLine(fileReader.readline())
        line = fileReader.readline()
        self.data = [float(s) for s in line.split()]
