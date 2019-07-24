import random
from math import cos, sin, atan2, pi

from .math_utils import MathUtility
from .constants import Constants


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
        self.angle = random.randint(0, 360)
        self.direction = 0
        self.size = 10
        self.state = Constants.STATE_BUSTER_NOTHING

    def is_in_team_0_base(self):
        """
        Function that say if the entity is in team0 base
        :return: true or false
        """
        return MathUtility.distance(0, 0, self.x, self.y) < Constants.ENTITY_RANGE_VISION

    def is_in_team_1_base(self):
        """
        Function that say if the entity is in team1 base
        :return: true or false
        """
        return MathUtility.distance(Constants.MAP_WIDTH + 1, Constants.MAP_HEIGHT + 1, self.x,
                                    self.y) < Constants.ENTITY_RANGE_VISION

    def _compute_max_move(self, x, y):
        """
        Function that will give coordinates for a maximum move in a round
        :param x: the x coordinate wanted
        :param y: the y coordinate wanted
        :return: the tuple (x', y') of maximum coordinate if the original move is going to far
        """
        if MathUtility.distance(self.x, self.y, x, y) <= Constants.BUSTER_MAX_MOVE:
            return x, y
        else:
            return self.x + Constants.BUSTER_MAX_MOVE * cos(
                pi / 2 - self.angle), self.y + Constants.BUSTER_MAX_MOVE * sin(pi / 2 - self.angle)

    def move(self, x, y):
        """
        Function that move the entity to its new position
        :param x: the x coordinate
        :param y: the y coordinate
        """
        self.angle = atan2(y - self.y, x - self.x)
        print("Angle : " + str(self.angle))
        x_max, y_max = self._compute_max_move(x, y)
        print("X_Max : " + str(x_max) + ", Y_Max : " + str(y_max))
        self.x = int(x_max)
        self.y = int(y_max)

    def get_closest(self, entities):
        """
        Function that gives the closest ghost of the buster from the ghosts list in his vision or of its friends
        :param entities: entities list
        :return: an entity
        """
        dist = Constants.MAP_MAX_DISTANCE
        closest = None
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x, entity.y) < dist:
                closest = entity
                dist = MathUtility.distance(self.x, self.y, entity.x, entity.y)

        return closest

    def get_closest_distance(self, entities):
        """
        Function that give the smallest distance from the entity to entities
        :param entities: entities to loop over
        :return: a distance
        """
        dist = Constants.MAP_MAX_DISTANCE
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x, entity.y) < dist:
                dist = MathUtility.distance(self.x, self.y, entity.x, entity.y)

        return dist

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
