import random
import pygame

from .entity import Entity
from .constants import Constants
from .math_utils import MathUtility


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
