import pygame

from gym_buster.envs.game_classes.constants import Constants


class GameRendering:
    """
    Class that will handle every render object for the game
    """

    def __init__(self, window_width, window_height):
        """
        Constructor
        """
        self.window_width = window_width
        self.window_height = window_height

    def init_screen(self):
        """
        Function that will initialize the screen
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption('Ghost Buster')
        self._init_writings()

    def _init_writings(self):
        """
        Function called to render the writings on the screen
        """
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text_surface_obj = self.font.render("Team 1 = 0 | Team 2 = 0 | Step = 0", True, Constants.PYGAME_WHITE)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (
            round(Constants.PYGAME_WINDOW_WIDTH * 0.2), round(Constants.PYGAME_WINDOW_HEIGHT * 0.9))

    def render_writings(self):
        """
       Function where score is evolving and redering it in text on screen
       """
        return NotImplementedError("Please implement this function")

    def game_render(self):
        """
        Function called to render the game
        """
        return NotImplementedError("Please implement this function")
