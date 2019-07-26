from math import sqrt, pow

from .constants import Constants


class MathUtility:
    """
    Class that will handle every functions needed with mathematics
    """

    @staticmethod
    def distance(x1, y1, x2, y2):
        """
        Compute the distance between two points
        :param x1: the x coordinate for point1
        :param y1: the y coordinate for point1
        :param x2: the x coordinate for point2
        :param y2: the y coordinate for point2
        :return: the distance between two points
        """
        return sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

    @staticmethod
    def opposite_direction(x1, y1, x2, y2, length):
        """
        Compute the opposite point of point2 through point 1 but with a different length
        :param x1: the x coordinate from point 1
        :param y1: the y coordinate from point 1
        :param x2: the x coordinate from point 2
        :param y2: the y coordinate from point 2
        :param length: the length from point1 to new point
        :return: a new point opposite to point2 of length length from this new point to point 1
        """
        dist = MathUtility.distance(x1, y1, x2, y2)
        if dist == 0:
            return x1, y1
        else:
            new_x = (x1 - x2)/dist
            new_y = (y1 - y2)/dist

            return MathUtility.limit_coordinates(x1 + new_x * length, y1 + new_y * length)

    @staticmethod
    def distance_from_base_0(entity):
        """
        Function that tells if an entity is in the base 0
        :param entity: the entity to check
        :return: a boolean true or false
        """
        return MathUtility.distance(0, 0, entity.x, entity.y) < Constants.BASE_RANGE_GHOST_VALIDATED

    @staticmethod
    def distance_from_base_1(entity):
        """
        Function that tells if an entity is in the base 1
        :param entity: the entity to check
        :return: a boolean true or false
        """
        return MathUtility.distance(Constants.MAP_WIDTH, Constants.MAP_HEIGHT, entity.x,
                                    entity.y) < Constants.BASE_RANGE_GHOST_VALIDATED

    @staticmethod
    def limit_coordinates(x1, y1):
        """
        Function that will return the coordinates to stay on the map
        :param x1: the x coordinate
        :param y1: the y coordinate
        :return: a tuple
        """
        if x1 < 0:
            x = 0
        elif x1 > Constants.MAP_WIDTH:
            x = Constants.MAP_WIDTH
        else:
            x = x1

        if y1 < 0:
            y = 0
        elif y1 > Constants.MAP_HEIGHT:
            y = Constants.MAP_HEIGHT
        else:
            y = y1
        return x, y
