import pygame

from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.game_classes.constants import Constants


class GhostSprite(Ghost):
    """
    Class that will handle everything about ghost rendering
    """

    def __init__(self):
        """
        Constructor
        """
        super(GhostSprite, self).__init__()
        self._create_image(Constants.PYGAME_GHOST_COLOR)
        print("Ghost image : " + str(self.image))

    def _create_image(self, color):
        """
        Create the first image of the ghost
        :param color: the color of the ghost
        """
        image = pygame.Surface((Constants.PYGAME_GHOST_RADIUS * 2, Constants.PYGAME_GHOST_RADIUS * 2)).convert_alpha()
        image.fill((0, 0, 0, 0))
        pygame.draw.circle(image, color,
                           (round(Constants.PYGAME_GHOST_RADIUS), round(Constants.PYGAME_GHOST_RADIUS)),
                           Constants.PYGAME_GHOST_RADIUS)
        self.image = image

    def _convert_position_to_pygame(self):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """
        return super(GhostSprite, self).convert_position_to_pygame(Constants.PYGAME_GHOST_RADIUS)

    def draw(self, surface):
        """
        Draw the buster on the surface
        :param surface: the surface where to render the buster image
        """
        if not self.alive or self.captured:
            self.image = pygame.Surface((1, 1)).convert_alpha()
            self.image.fill((0, 0, 0, 0))
        else:
            self.image = pygame.Surface(
                (Constants.PYGAME_GHOST_RADIUS * 2, Constants.PYGAME_GHOST_RADIUS * 2)).convert_alpha()
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, Constants.PYGAME_GHOST_COLOR,
                               (round(Constants.PYGAME_GHOST_RADIUS), round(Constants.PYGAME_GHOST_RADIUS)),
                               Constants.PYGAME_GHOST_RADIUS)

        a, b = self._convert_position_to_pygame()
        surface.blit(self.image, (a, b))
