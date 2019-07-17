import gym
from gym import spaces
import random, logging, sys, re
import pygame
import numpy as np
from math import sqrt, pow, pi, cos, sin, radians, degrees, atan2

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
    GAME_ROUND_NUMBER = 250

    BASE_RANGE_GHOST_VALIDATED = 1600

    GHOST_RUN_WAY = 220
    BUSTER_MAX_MOVE = 800
    BUSTER_BUST_MAX_RANGE = 1760
    BUSTER_BUST_MIN_RANGE = 900

    ACTION_MOVE_REGEX = r'MOVE (\d{0,5}) (\d{0,5})'
    ACTION_RELEASE_REGEX = r'RELEASE'
    ACTION_BUST_REGEX = r'BUST (\d+)'

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
    PYGAME_SPEED = 20  # pixels

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
                pi / 2 - radians(self.angle)), self.y + Constants.BUSTER_MAX_MOVE * sin(pi / 2 - radians(self.angle))

    def move(self, x, y):
        """
        Function that move the entity to its new position
        :param x: the x coordinate
        :param y: the y coordinate
        """
        self.angle = degrees(atan2(y - self.y, x - self.x))
        x_max, y_max = self._compute_max_move(x, y)
        self.x = int(x_max)
        self.y = int(y_max)


class Ghost(Entity):
    """
    Class that will handle the ghost entity
    """

    ghost_id = 1
    ghosts = []

    def __init__(self, type_entity):
        """
        Constructor
        """
        super(Ghost, self).__init__(type_entity)
        self.value = Constants.VALUE_GHOST_BASIC
        self.id = self._generate_id()
        self._add_ghost(self)
        self._generate_random_ghost_position()
        self.create_image(Constants.PYGAME_GHOST_COLOR)
        self.alive = True
        self.captured = False
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

    @classmethod
    def _add_ghost(cls, obj):
        """
        Add the ghost to the list of the class
        :param obj: the ghost to add
        """
        cls.ghosts.append(obj)

    @classmethod
    def _remove_ghost(cls, obj):
        """
        Remove the ghost from the class list
        :param obj: the ghost to remove
        """
        cls.ghosts.remove(obj)

    @classmethod
    def _reset_ghost(cls):
        """
        Reset the class list
        """
        cls.ghosts = []
        cls.ghost_id = 1

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
            self.x = new_x
            self.y = new_y

    @classmethod
    def get_ghost(cls, ids):
        """
        Return the ghost with the id
        :param ids: the ghost to return
        :return: a ghost
        """
        for ghost in cls.ghosts:
            if ghost.id == ids:
                return ghost


class Buster(Entity):
    """
    Class that will handle busters
    """
    entity_type_0_id = 1
    entity_type_1_id = 1
    busters_1 = []
    busters_0 = []

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
            self.id = self._generate_id(Constants.TYPE_BUSTER_TEAM_0, self)
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            self.x = Constants.MAP_WIDTH - 50
            self.y = Constants.MAP_HEIGHT - 50
            self.id = self._generate_id(Constants.TYPE_BUSTER_TEAM_1, self)
        else:
            raise Exception("Entity neither in team 0 or team 1")

    @classmethod
    def _generate_id(cls, team, obj):
        """
        Function that will generate the id for the buster
        :param team: the entity team
        :return: the id
        """
        if team == Constants.TYPE_BUSTER_TEAM_0:
            ids = cls.entity_type_0_id
            cls.entity_type_0_id += 1
            cls.busters_0.append(obj)
            return ids
        elif team == Constants.TYPE_BUSTER_TEAM_1:
            ids = cls.entity_type_1_id
            cls.entity_type_1_id += 1
            cls.busters_1.append(obj)
            return ids

    @classmethod
    def _reset_busters(cls):
        """
        Function that will reset both class list
        """
        cls.busters_1 = []
        cls.busters_0 = []
        cls.entity_type_1_id = 1
        cls.entity_type_0_id = 1

    def is_in_team_base(self):
        """
        Function that gives us true if the buster is in team base
        :return: true or false
        """
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            return self.is_in_team_0_base()
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            return self.is_in_team_1_base()

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

    def can_bust(self, ghost):
        """
        Function that will tell if you can bust the ghost
        :param ghost: the ghost to bust
        :return: true or false
        """
        return MathUtility.distance(ghost.x, ghost.y, self.x, self.y) <= Constants.BUSTER_BUST_MAX_RANGE \
               and MathUtility.distance(ghost.x, ghost.y, self.x, self.y) >= Constants.BUSTER_BUST_MIN_RANGE

    def buster_command(self, command):
        """
        Parse the buster command and execute the command
        :param command: the command to check and execute
        """
        try:
            move = re.match(Constants.ACTION_MOVE_REGEX, command)
            release = re.match(Constants.ACTION_RELEASE_REGEX, command)
            bust = re.match(Constants.ACTION_BUST_REGEX, command)
            if move:
                self.move(int(move.group(1)), int(move.group(2)))
                print(str(self.id) + " moving to " + str(self.x) + " " + str(self.y))
                return 0
            elif release:
                self.release()
                print(str(self.id) + " releasing")
                return -1
            elif bust:
                self.bust(int(bust.group(1)))
                print(str(self.id) + " busting " + bust.group(1))
                return 0
            else:
                raise Exception("Wrong command for buster : " + str(self))
        except Exception as exc:
            raise exc

    def release(self):
        """
        Execute the action to release the ghost
        """
        if self.value != Constants.VALUE_BUSTER_NOTHING and self.state == Constants.STATE_BUSTER_CARRYING:
            ghost = Ghost.get_ghost(self.value)
            ghost.captured = False
            ghost.x = self.x
            ghost.y = self.y
            ghost.angle = self.angle
            ghost.value = Constants.VALUE_GHOST_BASIC

            self.value = Constants.VALUE_BUSTER_NOTHING
            self.state = Constants.STATE_BUSTER_NOTHING

    def bust(self, ids):
        """
        Execute the action to catch a ghost with id ids
        :param ids: the ghost to catch
        """
        ghost = Ghost.get_ghost(ids)
        if self.state == Constants.STATE_BUSTER_NOTHING and MathUtility.distance(ghost.x, ghost.y, self.x,
                                                                                 self.y) <= Constants.BUSTER_BUST_MAX_RANGE and MathUtility.distance(
            ghost.x, ghost.y, self.x, self.y) >= Constants.BUSTER_BUST_MIN_RANGE:
            ghost.value += 1
            self.value = ids


class Aibehaviour:
    """
    Class that will handle an easy / medium IA
    """

    def __init__(self):
        pass

    @staticmethod
    def next_command(busters, ghosts):
        """
        Function that will return commands to do for the next round
        :param busters: the busters belonging to the AI
        :param ghosts: the ghosts busters can see
        :return: a list of commands
        """
        busters_already_treated = dict(zip(busters, [None, None, None]))
        ghosts_already_treated = []
        commands = []
        if len(busters) == 3:
            for buster in busters:
                # If a buster is carrying a ghost then go back to base or release if in distance
                if buster.state == Constants.STATE_BUSTER_CARRYING and busters_already_treated[buster] is None:
                    print("Buster " + str(buster.id) + " carrying a ghost.")
                    # Verify if in base else go back to base
                    if buster.is_in_team_base():
                        busters_already_treated[buster] = "RELEASE"
                    else:
                        busters_already_treated[buster] = "MOVE 1000 1000"
                    continue

                # If a busters can see a ghost then go on it (only one)
                for ghost in ghosts:
                    if buster.can_bust(ghost) and busters_already_treated[buster] is None:
                        busters_already_treated[buster] = "BUST " + ghost.id
                        ghosts_already_treated.append(ghost)
                        continue

                # if busters can see a ghost go for it
                for ghost in ghosts:
                    if not buster.can_bust(ghost) and ghost not in ghosts_already_treated and \
                            busters_already_treated[buster] is None:
                        busters_already_treated[buster] = "MOVE " + str(ghost.x) + " " + str(ghost.y)
                        ghosts_already_treated.append(ghost)
                        continue

                # move randomly if nothing good
                if busters_already_treated[buster] is None:
                    x = random.randint(1500, 14500)
                    y = random.randint(1000, 8000)
                    busters_already_treated[buster] = "MOVE " + str(x) + " " + str(y)

        for buster in busters:
            commands.append(busters_already_treated[buster])

        return commands


class Game:
    """
    Class that will handle a game
    """

    def __init__(self, mode, ghost_number, buster_number, round_number):
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
        self.round_number = round_number

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

    def _get_commands_from_console(self):
        """
        Function that will get commands of each buster from console
        :return: the tuple of each list of command for each team
        """
        print("Enter commands for team 0 (top left)")
        commands_0 = []
        for i in range(self.buster_number):
            commands_0.append(str(input()))

        commands_1 = []
        print("Enter commands for team 1 (bot right)")
        for i in range(self.buster_number):
            commands_1.append(str(input()))

        return commands_0, commands_1

    def _get_command_from_console(self):
        """
        Function that will get commands of each buster from console for one team
        :return: the list of commands
        """
        print("Enter commands for team 0 (top left)")
        commands_0 = []
        for i in range(self.buster_number):
            commands_0.append(str(input()))

        return commands_0

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
        """
        Main function that handle every rounds
        """
        self.game_render()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # commands_team_0, commands_team_1 = self._get_commands_from_console()
            # Lets say that they can see every ghosts
            commands_team_1 = Aibehaviour.next_command(Buster.busters_1, self.ghosts)
            commands_team_0 = self._get_command_from_console()
            self._run_round(commands_team_0, commands_team_1)
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

    def _run_round(self, commands_team_0, commands_team_1):
        """
        Function that will run a round and execute each event triggered
        """
        # First execute automatic actions

        remove_ghosts = []
        # Ghost released in a base
        for ghost in self.ghosts:
            if MathUtility.distance_from_base_0(ghost):
                self.score_team_0 += 1
                ghost.alive = False
                remove_ghosts.append(ghost)
            elif MathUtility.distance_from_base_1(ghost):
                self.score_team_1 += 1
                ghost.alive = False
                remove_ghosts.append(ghost)
            ghost.value = Constants.VALUE_GHOST_BASIC

        # Remove ghosts not available anymore
        for ghost in remove_ghosts:
            self.ghosts.remove(ghost)
            Ghost._remove_ghost(ghost)

        # Execute for each buster his tasks
        for i in range(1, self.buster_number + 1):
            # Retrieve busters i to execute their action at the same moment (almost)
            buster_team_0 = Buster.get_buster(self.busters, i, Constants.TYPE_BUSTER_TEAM_0)
            buster_team_1 = Buster.get_buster(self.busters, i, Constants.TYPE_BUSTER_TEAM_1)

            command_0 = commands_team_0[i - 1]
            command_1 = commands_team_1[i - 1]

            print("Buster team 0 | id : " + str(buster_team_0.id) + " | Command : " + command_0)
            self.score_team_0 += buster_team_0.buster_command(command_0)
            print("Buster team 1 | id : " + str(buster_team_1.id) + " | Command : " + command_1)
            self.score_team_1 += buster_team_1.buster_command(command_1)

        for ghost in self.ghosts:
            # Get all busters with the id of the ghost
            if ghost.value != Constants.VALUE_GHOST_BASIC:
                nb_buster_team_0_busting_this_ghost = []
                nb_buster_team_1_busting_this_ghost = []
                for buster in Buster.busters_0:
                    if buster.value == ghost.id:
                        nb_buster_team_0_busting_this_ghost.append(buster)
                for buster in Buster.busters_1:
                    if buster.value == ghost.id:
                        nb_buster_team_1_busting_this_ghost.append(buster)

                closest = None

                # If list length != 0 and same value then draw nobody take the ghost
                if len(nb_buster_team_0_busting_this_ghost) == len(nb_buster_team_1_busting_this_ghost) and len(
                        nb_buster_team_1_busting_this_ghost) > 0:
                    ghost.captured = False
                elif len(nb_buster_team_0_busting_this_ghost) > len(nb_buster_team_1_busting_this_ghost):
                    # Find closest team 0 buster and give it to him
                    closest = nb_buster_team_0_busting_this_ghost[0]
                    dist = MathUtility.distance(ghost.x, ghost.y, closest.x, closest.y)
                    for buster in nb_buster_team_0_busting_this_ghost:
                        new_dist = MathUtility.distance(ghost.x, ghost.y, buster.x, buster.y)
                        if new_dist < dist:
                            dist = new_dist
                            closest = buster

                elif len(nb_buster_team_0_busting_this_ghost) < len(nb_buster_team_1_busting_this_ghost):
                    # Find closest team 1 buster and give it to him
                    closest = nb_buster_team_1_busting_this_ghost[0]
                    dist = MathUtility.distance(ghost.x, ghost.y, closest.x, closest.y)
                    for buster in nb_buster_team_0_busting_this_ghost:
                        new_dist = MathUtility.distance(ghost.x, ghost.y, buster.x, buster.y)
                        if new_dist < dist:
                            dist = new_dist
                            closest = buster

                # Reset all busters with this ghost id except
                if closest:
                    if closest.type == Constants.TYPE_BUSTER_TEAM_0:
                        self.score_team_0 += 1
                    if closest.type == Constants.TYPE_BUSTER_TEAM_1:
                        self.score_team_1 += 1
                    for buster in nb_buster_team_0_busting_this_ghost + nb_buster_team_1_busting_this_ghost:
                        if buster != closest:
                            buster.value = Constants.VALUE_BUSTER_NOTHING
                            buster.state = Constants.STATE_BUSTER_NOTHING

            else:
                ghost.captured = False

        # make ghost run away
        for ghost in self.ghosts:
            ghost.run_away(self.busters)

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

    def __init__(self, buster_number, ghost_number, episodes, max_steps):
        self.buster_number = buster_number
        self.ghost_number = ghost_number
        self.state = None
        self.observation = None
        self.previous_observation = None

        self.action_space = self._action_space()
        self.observation_space = self._observation_space()

        self.episodes = episodes # Number of games to do
        self.episode_maximum_step = max_steps # Number of max steps in a game
        self.episode_step = 0
        self.episodes_win = 0

        self.game = Game('human', self.ghost_number, self.buster_number, self.episode_maximum_step)

    def _action_space(self):
        """
        Action space for gym env

        For each buster : move_degree, move_distance, or bust or release

        :return: the space
        """
        action_low = []
        action_high = []
        for i in range(self.buster_number):
            action_low += [-1.0, -1.0, 0.0, 0.0]
            action_high += [1.0, 1.0, 1.0, 1.0]

        return spaces.Box(np.array(action_low), np.array(action_high))

    def _observation_space(self):
        """
        observation space for gym env

        team0 points, team 1 points

        for each buster : state(carrying or not), distance from closest ghost, number of ghosts in range,
        distance from closest ennemy, number of enemy in range

        :return: the space
        """
        obs_low = [0.0, 0.0]
        obs_high = [self.ghost_number, self.ghost_number]
        for i in range(self.buster_number):
            obs_low += [0.0, 0.0, 0.0, 0.0, 0.0]
            obs_high += [1.0, Constants.MAP_MAX_DISTANCE, self.ghost_number, Constants.MAP_MAX_DISTANCE, self.buster_number]

        return spaces.Box(np.array(obs_low), np.array(obs_high))

    def _compute_reward(self):
        """
        Function that will compute reward for movement decided by the AI
        :return: the reward
        """
        # For now easy things

        # Battle over and won
        if self.state['battle_won']:
            return 1000
        # Battle over and lost
        if self.state['battle_ended'] and not self.state['battle_won']:
            return -1000
        # point + 1
        if self.observation['points_team_0'] > self.previous_observation['points_team_0']:
            return 200
        # point - 1
        if self.observation['points_team_0'] < self.previous_observation['points_team_0']:
            return -200

        return 0

    def _check_done(self):
        """
        Function that will say if a game is over
        :return: boolean
        """
        return self.state['battle_ended']

    def _get_info(self):
        """
        Function that will give some info for debugging
        :return: dictionnary with information
        """
        return {} # TODO implement info

    def step(self, action):
        self.episode_step += 1

        self.state = self.game.get_state()
        self.previous_observation = self.observation
        self.observation = self._make_observation()
        reward = self._compute_reward()
        done = self._check_done()
        info = self._get_info()

        return self.observation, reward, done, info


    def reset(self):

        if self.episode_step >= self.episode_maximum_step:
            # End it and start a new game
            pass

        self.episodes += 1
        self.episode_step = 0

        # TODO Init a new game and give the state to self.state
        #self.state =

        self.observation = self._make_observation()
        self.previous_observation = self.observation

        return self.observation


    def render(self, mode='human', close=False):
        pass


if __name__ == '__main__':
    game = Game('human', Constants.GHOST_NUMBER, Constants.BUSTER_NUMBER_PER_TEAM, Constants.GAME_ROUND_NUMBER)
    game.loop()
