import gym
import random, string, logging, math, sys
import pygame

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

    BASE_RANGE_GHOST_VALIDATED = 1600

    GHOST_RUN_WAY = 220

    # TYPE
    TYPE_GHOST = -1
    TYPE_BUSTER_TEAM_0 = 0
    TYPE_BUSTER_TEAM_1 = 1

    # STATE
    STATE_GHOST = 0
    STATE_BUSTER_CARRYING = 1
    STATE_BUSTER_NOTHING = 0

    # VALUE
    VALUE_GHOST_BASIC = 0
    VALUE_BUSTER_NOTHING = -1

    # Rendering constants
    FPS = 30

    PYGAME_WINDOW_HEIGHT = 450  # pixels
    PYGAME_WINDOW_WIDTH = 800  # pixels
    PYGAME_WHITE = (255, 255, 255)
    PYGAME_GHOST_COLOR = (255, 255, 255)
    PYGAME_BUSTER_TEAM_0_COLOR = (0, 255, 0)
    PYGAME_BUSTER_TEAM_1_COLOR = (255, 0, 0)
    PYGAME_BLACK = (0, 0, 0)
    PYGAME_GHOST_RADIUS = 10  # pixels
    PYGAME_BUSTER_RADIUS = 10  # pixels
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

    @staticmethod
    def distance_from_base_0(ghost):
        """
        Function that tells if the ghost is in the base 0
        :param ghost: the ghost to check
        :return: a boolean true or false
        """
        return MathUtility.distance(0, 0, ghost.x, ghost.y) < Constants.BASE_RANGE_GHOST_VALIDATED

    @staticmethod
    def distance_from_base_1(ghost):
        """
        Function that tells if the ghost is in the base 1
        :param ghost: the ghost to check
        :return: a boolean true or false
        """
        return MathUtility.distance(Constants.MAP_WIDTH, Constants.MAP_HEIGHT, ghost.x,
                                    ghost.y) < Constants.BASE_RANGE_GHOST_VALIDATED


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


class Ghost(Entity):
    """
    Class that will handle the ghost entity
    """

    ghost_id = 1

    def __init__(self, type_entity):
        """
        Constructor
        """
        super(Ghost, self).__init__(type_entity)
        self.value = Constants.VALUE_GHOST_BASIC
        self.id = self._generate_id()
        self._generate_random_ghost_position()
        self.create_image(Constants.PYGAME_GHOST_COLOR)
        self.alive = True
        print("Ghost : " + str(self.id) + ", position : " + str(self.x) + " " + str(self.y) + ", image : " + str(
            self.image))

    def _generate_random_ghost_position(self):
        """
        Function that generate a random position for the ghost
        """
        generated = False
        while not generated:
            self.x = random.randint(0, Constants.MAP_WIDTH)
            self.y = random.randint(0, Constants.MAP_HEIGHT)
            if not (self.is_in_team_0_base() or self.is_in_team_1_base()):
                generated = True

    @classmethod
    def _generate_id(cls):
        """
        Generate ghosts id
        :return: the ghost id
        """
        ids = cls.ghost_id
        cls.ghost_id += 1
        return ids

    def draw(self, surface):
        """
        Draw the buster on the surface
        :param surface: the surface where to render the buster image
        """
        if self.alive:
            surface.blit(self.image, self.convert_position_to_pygame())
        else:
            self.image = pygame.Surface((1, 1)).convert_alpha()
            self.image.fill((0, 0, 0, 0))
            surface.blit(self.image, self.convert_position_to_pygame())

    def convert_position_to_pygame(self):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """

        return (round(self.x * Constants.PYGAME_RATIO_WIDTH - Constants.PYGAME_GHOST_RADIUS),
                round(self.y * Constants.PYGAME_RATIO_HEIGHT - Constants.PYGAME_GHOST_RADIUS))

    def create_image(self, color):
        """
        Create the first image of the ghost
        :param color: the color of the ghost
        """
        image = pygame.Surface((Constants.PYGAME_GHOST_RADIUS * 2, Constants.PYGAME_GHOST_RADIUS * 2)).convert_alpha()
        image.fill((0, 0, 0, 0))
        pygame.draw.circle(image, color,
                           (round(Constants.PYGAME_GHOST_RADIUS), round(Constants.PYGAME_GHOST_RADIUS)),
                           Constants.PYGAME_GHOST_RADIUS)
        self.image = image

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
    entity_type_0_id = 1
    entity_type_1_id = 1

    def __init__(self, type_entity):
        """
        Constructor
        """
        super(Buster, self).__init__(type_entity)
        self.value = Constants.VALUE_BUSTER_NOTHING
        self._generate_buster_position()
        self.create_image()
        print(
            "Buster : " + str(self.id) + ", position : " + str(self.x) + " " + str(self.y) + ", image : " + str(
                self.image))

    def _generate_buster_position(self):
        """
        Function that handle the initial position for busters
        """
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            self.x = 50
            self.y = 50
            self.id = self._generate_id(Constants.TYPE_BUSTER_TEAM_0)
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            self.x = Constants.MAP_WIDTH - 50
            self.y = Constants.MAP_HEIGHT - 50
            self.id = self._generate_id(Constants.TYPE_BUSTER_TEAM_1)
        else:
            raise Exception("Entity neither in team 0 or team 1")

    @classmethod
    def _generate_id(cls, team):
        """
        Function that will generate the id for the buster
        :param team: the entity team
        :return: the id
        """
        if team == Constants.TYPE_BUSTER_TEAM_0:
            ids = cls.entity_type_0_id
            cls.entity_type_0_id += 1
            return ids
        elif team == Constants.TYPE_BUSTER_TEAM_1:
            ids = cls.entity_type_1_id
            cls.entity_type_1_id += 1
            return ids

    def draw(self, surface):
        """
        Draw the buster on the surface
        :param surface: the surface where to render the buster image
        """
        surface.blit(self.image, self.convert_position_to_pygame())

    def convert_position_to_pygame(self):
        """
        Function that will convert x,y position of the entity to pygame pixel
        :return: a tuple of converted coordinates
        """

        return (self.x * Constants.PYGAME_RATIO_WIDTH - Constants.PYGAME_BUSTER_RADIUS,
                self.y * Constants.PYGAME_RATIO_HEIGHT - Constants.PYGAME_BUSTER_RADIUS)

    def create_image(self):
        """
        Create the first image of the buster
        :param color: the color
        """
        image = pygame.Surface((Constants.PYGAME_BUSTER_RADIUS * 2, Constants.PYGAME_BUSTER_RADIUS * 2)).convert_alpha()
        image.fill((0, 0, 0, 0))
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            self.color = Constants.PYGAME_BUSTER_TEAM_0_COLOR
        else:
            self.color = Constants.PYGAME_BUSTER_TEAM_1_COLOR
        pygame.draw.circle(image, self.color,
                           (round(Constants.PYGAME_BUSTER_RADIUS), round(Constants.PYGAME_BUSTER_RADIUS)),
                           Constants.PYGAME_BUSTER_RADIUS)
        self.image = image

    @staticmethod
    def get_buster(busters, number, team):
        """
        Retrieve the buster of ID number of team team
        :param busters: the buster list
        :param number: the ID number
        :param team: the team
        :return: the buster
        """
        for buster in busters:
            if buster.id == number and buster.type == team:
                return buster

class Game:
    """
    Class that will handle a game
    """

    def __init__(self, mode, ghost_number, buster_number):
        """
        Constructor
        :param mode: the mode used for the game (console or human)
        """
        self.mode = mode
        self.ghost_number = ghost_number
        self.buster_number = buster_number
        self.window_height = Constants.PYGAME_WINDOW_HEIGHT
        self.window_width = Constants.PYGAME_WINDOW_WIDTH
        self._init_screen()
        self._generate_ghosts(Constants.GHOST_NUMBER)
        self._generate_busters(Constants.BUSTER_NUMBER_PER_TEAM)
        self.board = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        self.speed = Constants.PYGAME_SPEED
        self.running = True
        self.clock = pygame.time.Clock()
        self.score_team_0 = 0
        self.score_team_1 = 0

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
        pygame.display.set_caption('Ghost Buster')
        self._init_writings()

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

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.game_render()
            pygame.display.flip()
            self.clock.tick(Constants.FPS)

        pygame.quit()
        sys.exit()

    # RENDERING FUNCTIONS

    def game_render(self):
        """
        Function called to render the game
        """

        self.screen.fill(Constants.PYGAME_BLACK)

        for buster in self.busters:
            buster.draw(self.screen)

        for ghost in self.ghosts:
            ghost.draw(self.screen)

        self._render_writings()

        pygame.display.update()

    def _init_writings(self):
        """
        Function called to render the writings on the screen
        """
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text_surface_obj = self.font.render("Team 1 = 0 | Team 2 = 0", True, Constants.PYGAME_WHITE)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (
            round(Constants.PYGAME_WINDOW_WIDTH * 0.2), round(Constants.PYGAME_WINDOW_HEIGHT * 0.9))

    def _render_writings(self):
        """
        Function where score is evolving and redering it in text on screen
        """
        self.text_surface_obj = self.font.render(
            "Team 1 = " + str(self.score_team_0) + " | Team 2 = " + str(self.score_team_1), True,
            Constants.PYGAME_WHITE)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (
            round(Constants.PYGAME_WINDOW_WIDTH * 0.2), round(Constants.PYGAME_WINDOW_HEIGHT * 0.9))
        self.screen.blit(self.text_surface_obj, self.text_rect_obj)

    # GAME FUNCTIONS

    def _run_round(self):
        """
        Function that will run a round and execute each event triggered
        """
        # First execute automatic actions

        # Ghost released in a base
        for ghost in self.ghosts:
            if MathUtility.distance_from_base_0(ghost):
                self.score_team_0 += 1
                ghost.alive = False
            elif MathUtility.distance_from_base_1(ghost):
                self.score_team_1 += 1
                ghost.alive = False

        # Execute for each buster his tasks
        for i in range(1, self.buster_number + 1):
            # Retrieve busters i to execute their action at the same moment (almost)
            buster_team_0 = Buster.get_buster(self.busters, i, Constants.TYPE_BUSTER_TEAM_0)
            buster_team_1 = Buster.get_buster(self.busters, i, Constants.TYPE_BUSTER_TEAM_1)

    def _update_entities_position(self):
        """
        Function that will update entities position on the map
        """
        for ghost in self.ghosts:
            self.board.map[ghost.x][ghost.y] = Constants.TYPE_GHOST

        for buster in self.busters:
            self.board.map[buster.x][buster.y] = buster.type


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
    game = Game('human', Constants.GHOST_NUMBER, Constants.BUSTER_NUMBER_PER_TEAM)
    game.loop()
