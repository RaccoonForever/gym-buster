import random
import copy

from .entity import Entity
from .constants import Constants
from .math_utils import MathUtility


class Ghost(Entity):
    """
    Class that will handle the ghost entity
    """

    ghost_id = 1
    ghosts = []

    def __init__(self):
        """
        Constructor
        """
        super(Ghost, self).__init__(Constants.TYPE_GHOST)
        self.value = Constants.VALUE_GHOST_BASIC
        self.id = self._generate_id()
        self._add_ghost(self)
        self._generate_random_ghost_position()
        self.alive = True
        self.captured = False
        print("Ghost : " + str(self.id) + ", position : " + str(self.x) + " " + str(self.y))

    @classmethod
    def _generate_id(cls):
        """
        Generate ghosts id
        :return: the ghost id
        """
        ids = copy.copy(cls.ghost_id)
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
        return None

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

    def being_captured(self, buster):
        """
        Function that will change the state of the ghost when captured
        :param buster: the buster that captured him
        """
        self.x = buster.x
        self.y = buster.y
        self.captured = True
        self.value = Constants.VALUE_GHOST_BASIC

    def kill(self):
        """
        Function that will handle the kill of the ghost
        """
        self.alive = False
        self._remove_ghost(self)