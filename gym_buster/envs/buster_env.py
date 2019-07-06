import gym
import random
import string
import logging
import math

logger = logging.getLogger(__name__)


class Constants:
    """
    Class that will handle all constants needed
    """
    # MAP Coonstants
    MAP_WIDTH = 16000
    MAP_HEIGHT = 9000

    # ENTITIES Constants
    ENTITY_ID_LENGTH = 16
    ENTITY_RANGE_VISION = 2200

    # GHOSTS Constants
    GHOST_NUMBER = 9


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
        return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))


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


class Entity:
    """
    Class that will handle any entity
    """

    def __init__(self):
        self.id = self._generate_id(Constants.ENTITY_ID_LENGTH)

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

    @staticmethod
    def _generate_id(length):
        """
        Function that will generate the id for entities
        :param length: the length of IDs
        :return:
        """
        result = ""
        for i in range(length):
            result += str(random.choice(string.ascii_letters))
        return result


class Ghost(Entity):
    """
    Class that will handle the ghost entity
    """

    def __init__(self):
        Entity.__init__(self)
        self._generate_ghost_position()

    def _generate_ghost_position(self):
        """
        Function that generate a random position for the ghost
        :return: a tuple (x, y) randomly generated
        """
        generated = False
        while not generated:
            self.x = random.randint(0, Constants.MAP_WIDTH)
            self.y = random.randint(0, Constants.MAP_HEIGHT)
            if not(self.is_in_team_0_base() or self.is_in_team_1_base()):
                generated = True


class Game:
    """
    Class that will handle a game
    """

    def __init__(self):
        """
        Constructor
        """
        self.map = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        self.ghosts = self._generate_ghosts(Constants.GHOST_NUMBER)

    def _generate_ghosts(self, ghost_number):
        return 1


class BusterEnv(gym.Env):
    """
    Class that will handle a codebuster environment
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass
