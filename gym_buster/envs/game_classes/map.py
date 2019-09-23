from .constants import Constants


class Map:
    """
    Class that will handle the map
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: the width of the map
        :param height: the height of the map
        """
        self.width = width
        self.height = height
        self.map = [[Constants.MAP_EMPTY_CELL] * self.height for i in range(self.width)]
