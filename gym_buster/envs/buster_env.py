import gym
import random, string, logging, math
import pygame
import pygame.gfxdraw
from pygame.locals import *

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

    GHOST_NUMBER = 9
    BUSTER_NUMBER_PER_TEAM = 3

    # TYPE
    TYPE_GHOST = -1
    TYPE_BUSTER_TEAM_0 = 0
    TYPE_BUSTER_TEAM_1 = 1


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


class Entity(pygame.sprite.Sprite):
    """
    Class that will handle any entity
    """

    def __init__(self, type_entity):
        """
        Constructor
        """
        pygame.sprite.Sprite.__init__(self)

        self.id = self._generate_id(Constants.ENTITY_ID_LENGTH)
        self.x = Constants.MAP_WIDTH / 2
        self.y = Constants.MAP_HEIGHT / 2
        self.type = type_entity

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

    def __init__(self, type_entity):
        """
        Constructor
        """
        super(Ghost, self).__init__(type_entity)
        self._generate_ghost_position()

    def _generate_ghost_position(self):
        """
        Function that generate a random position for the ghost
        """
        generated = False
        while not generated:
            self.x = random.randint(0, Constants.MAP_WIDTH)
            self.y = random.randint(0, Constants.MAP_HEIGHT)
            if not(self.is_in_team_0_base() or self.is_in_team_1_base()):
                generated = True


class Buster(Entity):
    """
    Class that will handle busters
    """

    def __init__(self, type_entity):
        """
        Constructor
        """
        super(Buster, self).__init__(type_entity)
        self._generate_buster_position()

    def _generate_buster_position(self):
        """
        Function that handle the initial position for busters
        """
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            self.x = 0
            self.y = 0
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            self.x = Constants.MAP_WIDTH
            self.y = Constants.MAP_HEIGHT
        else:
            raise Exception("Entity neither in team 0 or team 1")


class Game:
    """
    Class that will handle a game
    """

    def __init__(self):
        """
        Constructor
        """
        self.map = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        self._generate_ghosts(Constants.GHOST_NUMBER)
        self._generate_busters(Constants.BUSTER_NUMBER_PER_TEAM)

    def _generate_busters(self, buster_number):
        """
        Function that will generate all busters
        :param buster_number: the number of buster in each team
        """
        self.busters = []
        for i in range(buster_number):
            self.busters.append(Buster(Constants.TYPE_BUSTER_TEAM_0))

        for i in range(buster_number):
            self.busters.append(Buster(Constants.TYPE_BUSTER_TEAM_1))

    def _generate_ghosts(self, ghost_number):
        """
        Function that will generate all ghosts
        :param ghost_number: the number of ghosts to generate
        """
        self.ghosts = []
        for i in range(ghost_number):
            self.ghosts.append(Ghost(Constants.TYPE_GHOST))


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


if __name__ == '__main__':
    game = Game()

