class EntitySprite:

    def _create_image(self, color):
        """
        Create the first image of the ghost
        :param color: the color of the ghost
        """
        return NotImplementedError("Please implement this function")

    def convert_position_to_pygame(self):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """
        return NotImplementedError("Please implement this function")

    def draw(self, surface):
        """
        Draw the buster on the surface
        :param surface: the surface where to render the buster image
        """
        return NotImplementedError("Please implement this function")
