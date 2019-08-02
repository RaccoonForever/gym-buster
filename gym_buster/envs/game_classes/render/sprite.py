from gym_buster.envs.game_classes.constants import Constants

class Sprite():
  """
  Class that will handle sprite method in common for every sprites
  """
  
  def _create_image(self):
    """
    Create the first image
    """
    raise NotImplementedError("Not allowed to call this function")
  
  def _convert_position_to_pygame(self, radius):
    """
    Function that will convert x,y position of the entity to pygame pixel
    :return: a tuple of converted coordinates
    """
    return (round(self.x * Constants.PYGAME_RATIO_WIDTH - radius),
(self.y * Constants.PYGAME_RATIO_HEIGHT - radius))

  def draw(self, surface):
    """
    Draw the sprite on the surface
    :param surface: the surface where to render
    """
    raise NotImplementedError("Not allowed to call this function")
  

  
