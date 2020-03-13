from GuiController.Graph import Graph

import pygame


# this handler is specifically for use with the tetris evo sim
class GraphHandler:

    # centralHandler the handler that will be used by the graph for acessing information to add to the graph
    def __init__(self, centralHandler):
        self.centralHandler = centralHandler

        # an integer determining which graph should be drawn
        #   0: fitness
        #   1: mutability
        #   2: Alive generations
        self.graph = 0

        lines = [
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((0, 0, 255), 1),
            Graph.GraphLine((255, 0, 0), 2),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((127, 0, 0), 2),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((0, 0, 0), 1),
            Graph.GraphLine((255, 0, 0), 2),
        ]
        self.fitnessGraph = Graph.LineGraph(lines)

        lines = [
            Graph.GraphLine((255, 0, 0), 2),
            Graph.GraphLine((127, 0, 0), 2),
            Graph.GraphLine((255, 0, 0), 2)
        ]

        self.mutabilityGraph = Graph.LineGraph(lines)

        lines = [
            Graph.GraphLine((255, 0, 0), 2),
            Graph.GraphLine((127, 0, 0), 2),
            Graph.GraphLine((0, 0, 255), 2)
        ]

        self.generationsGraph = Graph.LineGraph(lines)

    # draw the current
    def renderWithPygame(self):
        p = self.centralHandler.pyGui

        p.fill((255, 255, 255))

        font = pygame.font.SysFont('Impact', 20)

        # instructions for zooming/panning
        text = font.render("F: toggle game/graph view", False, (0, 0, 0))
        p.blit(text, (10, 10))
        text = font.render("Right click: drag graph", False, (0, 0, 0))
        p.blit(text, (10, 32))
        text = font.render("Left click: reset graph pos and zoom", False, (0, 0, 0))
        p.blit(text, (10, 54))
        text = font.render("Scroll wheel up/down: zoom graph in/out", False, (0, 0, 0))
        p.blit(text, (10, 76))
        text = font.render("Shift + scroll wheel: zoom only x axis", False, (0, 0, 0))
        p.blit(text, (10, 98))
        text = font.render("Ctrl + scroll wheel: zoom only y axis", False, (0, 0, 0))
        p.blit(text, (10, 120))

        if self.graph == 0:
            self.fitnessGraph.renderWithPygame(200, 150, 1400, 600, p)

            # info about lines
            text = font.render("Fitness graph:", False, (0, 0, 0))
            p.blit(text, (500, 10))
            text = font.render("Red: best and worst", False, (255, 0, 0))
            p.blit(text, (500, 32))
            text = font.render("Dark Red: median", False, (128, 0, 0))
            p.blit(text, (500, 54))
            text = font.render("Black: 90, 80, ... , 10 percentile", False, (0, 0, 0))
            p.blit(text, (500, 76))
            text = font.render("Blue: 99, 98, ... , 91 percentile", False, (0, 0, 255))
            p.blit(text, (500, 98))
            text = font.render("    and 9, 8, ... , 1 percentile", False, (0, 0, 255))
            p.blit(text, (500, 120))

            # instructions for pressing keys
            g = self.centralHandler.graphHandler.fitnessGraph.displayLines
            font = pygame.font.SysFont('Impact', 15)

            text = font.render(getOnOffString("Back quote: Toggle best (", g[18]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 10))
            text = font.render(getOnOffString("1: Toggle 10% percentile (", g[19]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 25))
            text = font.render(getOnOffString("2: Toggle 20% percentile (", g[20]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 40))
            text = font.render(getOnOffString("3: Toggle 30% percentile (", g[21]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 55))
            text = font.render(getOnOffString("4: Toggle 40% percentile (", g[22]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 70))
            text = font.render(getOnOffString("5: Toggle median (", g[23]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 85))
            text = font.render(getOnOffString("6: Toggle 60% percentile (", g[24]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 100))
            text = font.render(getOnOffString("7: Toggle 70% percentile (", g[25]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 115))
            text = font.render(getOnOffString("8: Toggle 80% percentile (", g[26]) + ")", False, (0, 0, 0))
            p.blit(text, (1020, 130))

            text = font.render(getOnOffString("9: Toggle 90% percentile (", g[27]) + ")", False, (0, 0, 0))
            p.blit(text, (1220, 10))
            text = font.render(getOnOffString("0: Toggle worst (", g[28]) + ")", False, (0, 0, 0))
            p.blit(text, (1220, 25))
            text = font.render("plus: Show all", False, (0, 0, 0))
            p.blit(text, (1220, 40))
            text = font.render("minus: Hide all", False, (0, 0, 0))
            p.blit(text, (1220, 55))
            text = font.render("ctrl + (1-9): Toggle percentile 1-9", False, (0, 0, 0))
            p.blit(text, (1220, 70))
            text = font.render("shift + (1-9): Toggle percentile 91-99", False, (0, 0, 0))
            p.blit(text, (1220, 85))
            text = font.render("ctrl + plus/minus: Show/hide percentile 1-9", False, (0, 0, 0))
            p.blit(text, (1220, 100))
            text = font.render("shift + plus/minus: Show/hide percentile 91-99", False, (0, 0, 0))
            p.blit(text, (1220, 115))

        elif self.graph == 1:
            self.mutabilityGraph.renderWithPygame(200, 150, 1400, 600, p)

            # info about lines
            text = font.render("Mutability graph:", False, (0, 0, 0))
            p.blit(text, (500, 10))
            text = font.render("Red: highest and lowest", False, (255, 0, 0))
            p.blit(text, (500, 32))
            text = font.render("Dark Red: median", False, (127, 0, 0))
            p.blit(text, (500, 54))

        elif self.graph == 2:
            self.generationsGraph.renderWithPygame(200, 150, 1400, 600, p)

            # info about lines
            text = font.render("Generations graph:", False, (0, 0, 0))
            p.blit(text, (500, 10))
            text = font.render("Red: Highest alive birth gen", False, (255, 0, 0))
            p.blit(text, (500, 32))
            text = font.render("Dark Red: Lowest alive birth gen", False, (127, 0, 0))
            p.blit(text, (500, 54))
            text = font.render("Blue: Difference in highest and lowest birth gen", False, (0, 0, 255))
            p.blit(text, (500, 76))

        # update display
        pygame.display.update()


# return the given string with either off or on depending on the given boolean b
def getOnOffString(s, b):
    if b:
        return s + "on"
    else:
        return s + "off"
