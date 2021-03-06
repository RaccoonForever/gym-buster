import random
from math import cos, sin, atan2, degrees, radians
from gym_buster.envs.game_classes.math_utils import MathUtility
from gym_buster.envs.game_classes.constants import Constants


class Entity:
    """
    Class that will handle any entity
    """

    # ---------------- PRIVATE FUNCTIONS AND PROPERTY ------------#
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
        self.render_img = None
        self.render_trans = None

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

    # ---------------- END PRIVATE FUNCTIONS AND PROPERTY ------------#
    
    # ---------------- ACTION FUNCTIONS -------------- #
    def move(self, x, y):
        """
        Function that move the entity to its new position
        :param x: the x coordinate
        :param y: the y coordinate
        """
        x_max, y_max = self._compute_max_move(x, y)
        self.x = x_max
        self.y = y_max

    # --------------- END ACTION FUNCTIONS ------------- #
    
    # --------------- UTIL FUNCTIONS FOR ENTITIES --------#
    def get_closest(self, entities, position):
        """
        Function that gives the closest ghost of the buster from the ghosts list in his vision or of its friends
        :param entities: entities list
        :param position: the position of the closest to return
        :return: an entity and the distance
        """
        dist0 = Constants.MAP_MAX_DISTANCE
        closest0 = None
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x, entity.y) < dist0:
                closest0 = entity
                dist0 = MathUtility.distance(self.x, self.y, entity.x, entity.y)

        closest1 = None
        dist1 = Constants.MAP_MAX_DISTANCE
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x, entity.y) < dist1 and entity != closest0:
                closest1 = entity
                dist1 = MathUtility.distance(self.x, self.y, entity.x, entity.y)

        closest2 = None
        dist2 = Constants.MAP_MAX_DISTANCE
        for entity in entities:
            if MathUtility.distance(self.x, self.y, entity.x,
                                    entity.y) < dist2 and entity != closest0 and entity != closest1:
                closest2 = entity
                dist2 = MathUtility.distance(self.x, self.y, entity.x, entity.y)

        closest = [closest0, closest1, closest2]
        dist = [dist0, dist1, dist2]

        return closest[position], dist[position]

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
    
    # --------------- END UTIL FUNCTIONS FOR ENTITIES --------#
