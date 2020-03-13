import pygame

from NeuralNet import NeuralNetHandler


# a class that handles the calculations and rendering for a gui that displays the Tetris game and neural net
class GameGui:

    def __init__(self, centralHandler):
        pygame.init()
        pygame.font.init()

        self.centralHandler = centralHandler

        self.gui = pygame.display.set_mode((1800, 1000))

        pygame.display.set_caption("Tetris game and neural net")

        # create the initial surface
        self.neuralNetSurface = pygame.image.load("empty.png").convert()

    # call this to redraw the NeuralNet based on its current state
    def updateNeuralNetSurface(self, neuralNet):
        neuralNet.renderWithPygame(self.neuralNetSurface, self.centralHandler)

    # render the given tetris and neuralNet to the GUI
    # tetirs is a Tetris object
    # neuralnet is a NeuralNet object
    def render(self, tetris):
        self.centralHandler.pyGui.fill((255, 255, 255))

        self.centralHandler.pyGui.blit(self.neuralNetSurface, (0, 0))

        tetris.renderWithPygame(self.centralHandler.pyGui, self.centralHandler)
        pygame.display.update()

    # updates the given tetris game based on the given neuralNet
    # use None for neuralNet if no move should be made
    def tick(self, tetris, neuralNet):
        if neuralNet is not None:
            # only send the central handler for rendering if the sim is not looping
            s = self.centralHandler.simMenu
            if s is not None and (s.testing or s.looping):
                handle = None
            else:
                handle = self.centralHandler

            NeuralNetHandler.makeNeuralNetMove(neuralNet, tetris, handle)

        tetris.nextLine()

