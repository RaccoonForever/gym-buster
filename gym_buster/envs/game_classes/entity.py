import random
from math import cos, sin, atan2, degrees, radians

from gym_buster.envs.game_classes.math_utils import MathUtility
from gym_buster.envs.game_classes.constants import Constants


class Entity:
    """
    Class that will handle any entity
    """

    def __init__(self, type_entity):
        """
        Constructor
        """

        self.id = 9999999999
        self.x = Constants.MAP_WIDTH / 2
        self.y = Constants.MAP_HEIGHT / 2
        self.type = type_entity
        self.angle = 0
        self.direction = 0
        self.size = 10
        self.state = Constants.STATE_BUSTER_NOTHING

    @property
    def is_in_team_0_base(self):
        """
        Function that say if the entity is in team0 base
        :return: true or false
        """
        return MathUtility.distance(0, 0, self.x, self.y) < Constants.ENTITY_RANGE_VISION

    @property
    def is_in_team_1_base(self):
        """
        Function that say if the entity is in team1 base
        :return: true or false
        """
        return MathUtility.distance(Constants.MAP_WIDTH, Constants.MAP_HEIGHT, self.x,
                                    self.y) < Constants.ENTITY_RANGE_VISION

    def _compute_max_move(self, x, y):
        """
        Function that will give coordinates for a maximum move in a round
        :param x: the x coordinate wanted
        :param y: the y coordinate wanted
        :return: the tuple (x', y') of maximum coordinate if the original move is going to far
        """
        self.angle = degrees(atan2(-(y - self.y), x - self.x))

        if MathUtility.distance(self.x, self.y, x, y) <= Constants.BUSTER_MAX_MOVE:
            return MathUtility.limit_coordinates(x, y)
        else:
            return MathUtility.limit_coordinates(int(self.x + Constants.BUSTER_MAX_MOVE * cos(
                radians(self.angle))), self.y - int(Constants.BUSTER_MAX_MOVE * sin(radians(self.angle))))

    def move(self, x, y):
        """
        Function that move the entity to its new position
        :param x: the x coordinate
        :param y: the y coordinate
        """
        x_max, y_max = self._compute_max_move(x, y)
        print("Angle : " + str(self.angle))
        print("X_Max : " + str(x_max) + ", Y_Max : " + str(y_max))
        self.x = x_max
        self.y = y_max

    def get_closest(self, entities):
        """
        Function that gives the closest ghost of the buster from the ghosts list in his vision or of its friends
        :param entities: entities list
        :return: an entity and the distance
        """
        dist = Constants.MAP_MAX_DISTANCE
        closest = None
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x, entity.y) < dist:
                closest = entity
                dist = MathUtility.distance(self.x, self.y, entity.x, entity.y)

        return closest, dist

    def get_number_entities_in_range(self, entities):
        """
        Function that will give the number of entities in range of this entity
        :param entities: entities list
        :return: a number
        """
        result = 0
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x, entity.y) < Constants.ENTITY_RANGE_VISION:
                result += 1

        return result

    def convert_position_to_pygame(self, radius):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """
        return (round(self.x * Constants.PYGAME_RATIO_WIDTH - radius),
                round(self.y * Constants.PYGAME_RATIO_HEIGHT - radius))

    @staticmethod
    def get_entities_visible(entities, targets):
        """
        Function that will return all entities that can be seen by entities over targets
        :param entities: the entities from which we compute
        :param targets: the targets we want to know which are in range of entities
        :return: a entity list
        """
        result = []
        for entity in entities:
            for target in targets:
                if MathUtility.distance(entity.x, entity.y, target.x,
                                        target.y) < Constants.ENTITY_RANGE_VISION and target not in result:
                    result.append(target)

        return result
