import gym
import random, string, logging, math, copy
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
    MAP_MAX_DISTANCE = 99999
    MAP_EMPTY_CELL = 0

    # ENTITIES Constants
    ENTITY_ID_LENGTH = 16
    ENTITY_RANGE_VISION = 2200

    GHOST_NUMBER = 9
    BUSTER_NUMBER_PER_TEAM = 3

    GHOST_RUN_WAY = 220

    # TYPE
    TYPE_GHOST = -1
    TYPE_BUSTER_TEAM_0 = 0
    TYPE_BUSTER_TEAM_1 = 1

    # Rendering constants
    PYGAME_WINDOW_HEIGHT = 450  # pixels
    PYGAME_WINDOW_WIDTH = 800  # pixels
    PYGAME_WHITE = (255, 255, 255)
    PYGAME_GHOST_COLOR = (255, 255, 255)
    PYGAME_BUSTER_TEAM_0_COLOR = (0, 255, 0)
    PYGAME_BUSTER_TEAM_1_COLOR = (255, 0, 0)
    PYGAME_BLACK = (0, 0, 0)
    PYGAME_GHOST_RADIUS = 10  # pixels
    PYGAME_BUSTER_LENGTH = 10  # pixels
    PYGAME_SPEED = 1  # pixels

    PYGAME_RATIO_HEIGHT = PYGAME_WINDOW_HEIGHT / MAP_HEIGHT
    PYGAME_RATIO_WIDTH = PYGAME_WINDOW_WIDTH / MAP_WIDTH


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
        dist_ratio = length / dist
        return x1 - dist_ratio * (x2 - x1), y1 - dist_ratio * (y2 - y1)


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


class Entity:
    """
    Class that will handle any entity
    """

    def __init__(self, type_entity):
        """
        Constructor
        """

        self.id = self._generate_id(Constants.ENTITY_ID_LENGTH)
        self.x = Constants.MAP_WIDTH / 2
        self.y = Constants.MAP_HEIGHT / 2
        self.type = type_entity
        self.angle = random.randint(0, 360)
        self.direction = 0
        self.size = 10
        self.timer = TickTimer(20)

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
        self.image = pygame.transform.rotate(
            Ghost.create_image(Constants.PYGAME_GHOST_RADIUS, Constants.PYGAME_GHOST_COLOR), self.angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.convert_position_to_pygame()
        print("Ghost : " + self.id + ", position : " + str(self.x) + " " + str(self.y) + ", rect : " + str(
            self.rect) + ", image : " + str(self.image))

    def _generate_ghost_position(self):
        """
        Function that generate a random position for the ghost
        """
        generated = False
        while not generated:
            self.x = random.randint(0, Constants.MAP_WIDTH)
            self.y = random.randint(0, Constants.MAP_HEIGHT)
            if not (self.is_in_team_0_base() or self.is_in_team_1_base()):
                generated = True

    def draw(self, surface):
        """
        Draw the buster on the surface
        :param surface: the surface where to render the buster image
        """
        surface.blit(self.image, self.rect)

    def convert_position_to_pygame(self):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """

        return (self.x * Constants.PYGAME_RATIO_WIDTH - Constants.PYGAME_GHOST_RADIUS,
                self.y * Constants.PYGAME_RATIO_HEIGHT - Constants.PYGAME_GHOST_RADIUS)

    @staticmethod
    def create_image(size, color):
        image = pygame.Surface((size*2, size*2))
        image = image.convert_alpha()
        image.fill((0, 0, 0, 0))
        pygame.draw.circle(image, color, (round((size - 1) / 2), round((size - 1) / 2)), round(size / 2))
        return image

    def run_away(self, busters):
        """
        Function that will make the ghost run away from the closest buster
        or the mean direction if more than one buster are equal distance from the ghost
        :param busters: the list of busters on the map
        :return: the ghost himself and the new coordinates for him
        """
        closest = []
        max_distance = Constants.MAP_MAX_DISTANCE
        for buster in busters:
            temp_dist = MathUtility.distance(self.x, self.y, buster.x, buster.y)
            if temp_dist < max_distance and temp_dist < Constants.ENTITY_RANGE_VISION:
                closest = [buster]
                max_distance = temp_dist
            elif temp_dist == max_distance and temp_dist < Constants.ENTITY_RANGE_VISION:
                closest.append(buster)

        # For now run away from the first but we will need to compute the run away from multiple busters same distance
        if closest:
            new_x, new_y = MathUtility.opposite_direction(self.x, self.y, closest[0].x, closest[0].y,
                                                          Constants.GHOST_RUN_WAY)
            return self, new_x, new_y


class Buster(Entity):
    """
    Class that will handle busters
    """

    def __init__(self, type_entity, color):
        """
        Constructor
        """
        super(Buster, self).__init__(type_entity)
        self._generate_buster_position()
        self.image = pygame.transform.rotate(
            Buster.create_image(Constants.PYGAME_BUSTER_LENGTH, color), self.angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.convert_position_to_pygame()
        print("Buster : " + self.id + ", position : " + str(self.x) + " " + str(self.y) + ", rect : " + str(
            self.rect) + ", image : " + str(self.image))

    def _generate_buster_position(self):
        """
        Function that handle the initial position for busters
        """
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            self.x = 50
            self.y = 50
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            self.x = Constants.MAP_WIDTH - 50
            self.y = Constants.MAP_HEIGHT - 50
        else:
            raise Exception("Entity neither in team 0 or team 1")

    def draw(self, surface):
        """
        Draw the buster on the surface
        :param surface: the surface where to render the buster image
        """
        surface.blit(self.image, self.rect)

    def convert_position_to_pygame(self):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """

        return (self.x * Constants.PYGAME_RATIO_WIDTH - Constants.PYGAME_BUSTER_LENGTH/2,
                self.y * Constants.PYGAME_RATIO_HEIGHT - Constants.PYGAME_BUSTER_LENGTH/2)

    @staticmethod
    def create_image(size, color):
        image = pygame.Surface((size, size))
        image = image.convert_alpha()
        image.fill((0, 0, 0, 0))
        pygame.draw.rect(image, color, (1, 1, size - 1, size - 1))
        return image


class TickTimer:
    """
    Class that will handle ticks for rendering
    """
    ticks = 0

    @classmethod
    def tick(cls):
        """
        Function that initialize ticks
        """
        cls.ticks = pygame.time.get_ticks()

    def __init__(self, interval):
        """
        Constructor
        :param interval: the interval between ticks
        """
        self.interval = interval
        self.next_tick = TickTimer.ticks + interval

    def elapse(self):
        """
        Function that say if next tick is reached
        :return: a boolean true or false
        """
        if TickTimer.ticks > self.next_tick:
            self.next_tick += self.interval
            if TickTimer.ticks > self.next_tick:
                self.next_tick = TickTimer.ticks + self.interval
            return True
        return False


class Game:
    """
    Class that will handle a game
    """

    def __init__(self, mode):
        """
        Constructor
        :param mode: the mode used for the game (console or human)
        """
        self.mode = mode
        self.window_height = Constants.PYGAME_WINDOW_HEIGHT
        self.window_width = Constants.PYGAME_WINDOW_WIDTH
        self._init_screen()
        self._generate_ghosts(Constants.GHOST_NUMBER)
        self._generate_busters(Constants.BUSTER_NUMBER_PER_TEAM)
        self.board = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        self.speed = Constants.PYGAME_SPEED
        self.running = True
        self.clock = pygame.time.Clock()

    def reset(self):
        """
        Function that will reset the game
        """
        self.window_height = Constants.PYGAME_WINDOW_HEIGHT
        self.window_width = Constants.PYGAME_WINDOW_WIDTH
        self.board = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        self.speed = Constants.PYGAME_SPEED

    def _init_screen(self):
        """
        Function that will initialize the pygame screen
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            TickTimer.tick()
            self.game_render()
            pygame.display.flip()

        pygame.quit()

    def game_render(self):
        """
        Function called to render the game
        """

        self.screen.fill(Constants.PYGAME_BLACK)

        for buster in self.busters:
            buster.draw(self.screen)

        for ghost in self.ghosts:
            ghost.draw(self.screen)

        pygame.display.update()

    def _update_entities_position(self):
        """
        Function that will update entities position on the map
        """
        for ghost in self.ghosts:
            self.board.map[ghost.x][ghost.y] = Constants.TYPE_GHOST

        for buster in self.busters:
            self.board.map[buster.x][buster.y] = buster.type

    def _generate_busters(self, buster_number):
        """
        Function that will generate all busters
        :param buster_number: the number of buster in each team
        """
        self.busters = []
        for i in range(buster_number):
            self.busters.append(Buster(Constants.TYPE_BUSTER_TEAM_0, Constants.PYGAME_BUSTER_TEAM_0_COLOR))

        for i in range(buster_number):
            self.busters.append(Buster(Constants.TYPE_BUSTER_TEAM_1, Constants.PYGAME_BUSTER_TEAM_1_COLOR))

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
    metadata = {'render.modes': ['human', 'console']}

    def __init__(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass


if __name__ == '__main__':
    game = Game('human')
    game.loop()
