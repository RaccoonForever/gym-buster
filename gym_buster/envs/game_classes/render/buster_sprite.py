import pygame

from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.constants import Constants

class BusterSprite(Buster):
  """
  Class that will handle everything used by Pygame for busters
  """
  
  def __init__(self, type_entity):
    """
    Constructor
    """
    super(BusterSprite, self).__init__(type_entity)
    self._create_image()
    print("Image : " + str(self.image))
  
  def _create_image(self):
    """
    Create the first image of the buster
    """
    image = pygame.Surface((Constants.PYGAME_BUSTER_RADIUS * 2, Constants.PYGAME_BUSTER_RADIUS * 2)).convert_alpha()
    image.fill((0, 0, 0, 0))
    if self.type == Constants.TYPE_BUSTER_TEAM_0:
        self.color = Constants.PYGAME_BUSTER_TEAM_0_COLOR
    else:
        self.color = Constants.PYGAME_BUSTER_TEAM_1_COLOR
    pygame.draw.circle(image, self.color,
                       (round(Constants.PYGAME_BUSTER_RADIUS), round(Constants.PYGAME_BUSTER_RADIUS)),
                       Constants.PYGAME_BUSTER_RADIUS)
    self.image = image
    
  def _convert_position_to_pygame(self):
    """
    Function that will convert x,y position of the entity to pygame pixel
    :return: a tuple of converted coordinates
    """
    super(GhostSprite, self)._convert_position_to_pygame(Constants.PYGAME_BUSTER_RADIUS)
    
  def draw(self, surface):
    """
    Draw the buster on the surface
    :param surface: the surface where to render the buster image
    """
    surface.blit(self.image, self._convert_position_to_pygame())
  
