import random
from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.math_utils import MathUtility


class Ghost(Entity):
    """
    Class that will handle the ghost entity
    """

    # Class variable to keep trace of all ghosts for performance
    ghosts = []

    # ------------- PRIVATE AND PROPERTY FUNCTIONS -------------#
    def __init__(self, id):
        """
        Constructor
        """
        super(Ghost, self).__init__(Constants.TYPE_GHOST)
        self.value = Constants.VALUE_GHOST_BASIC

        self.id = id
        self._generate_random_ghost_position()
        self.alive = True
        self.captured = False
        self._add_ghost(self)
    
    def _generate_random_ghost_position(self):
        """
        Function that generate a random position for the ghost
        """
        generated = False
        while not generated:
            self.x = random.randint(0, Constants.MAP_WIDTH)
            self.y = random.randint(0, Constants.MAP_HEIGHT)
            if not (self.is_in_team_0_base or self.is_in_team_1_base):
                generated = True

    # ------------- PRIVATE AND PROPERTY FUNCTIONS -------------#
     
    # -------------- CLASS METHODS ---------------- #

    @classmethod
    def _add_ghost(cls, obj):
        """
        Add the ghost to the list of the class
        :param obj: the ghost to add
        """
        cls.ghosts.append(obj)

    @classmethod
    def reset_ghost(cls):
        """
        Reset the class list
        """
        cls.ghosts = []

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

    # -------------- END CLASS METHODS ---------------- #

    # -------------- UPDATING ATTRIBUTES FUNCTIONS ----------------#
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
        # TODO handle barycenter
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
        self.updating_position(buster)
        self.captured = True
        self.value = 1

    def kill(self):
        """
        Function that will handle the kill of the ghost
        """
        self.alive = False

    def being_released(self, buster):
        """
        Function to call when releasing a ghost
        :param buster: the buster releasing the ghost
        """
        self.captured = False
        self.updating_position(buster)
        self.angle = buster.angle
        self.value = Constants.VALUE_GHOST_BASIC

    def busting_cancelled(self):
        """
        Function to call when same numbers of busters in each team tried to catch this ghost
        """
        print("Ghost {} cancelling busting".format(self.id))
        self.captured = False
        self.value = Constants.VALUE_GHOST_BASIC

    def updating_position(self, buster):
        """
        Function to call to update position of the ghost to be the same of the buster
        :param buster: the position to copy
        """
        self.x = buster.x
        self.y = buster.y

    # -------------- END UPDATING ATTRIBUTES FUNCTIONS ----------------#

    def __str__(self):
        """
        Display function
        """
        return 'Ghost {}, X: {}, Y: {}, Value: {}, State: {}, Captured: {}, Alive: {}'.format(self.id, self.x, self.y,
                                                                                              self.value, self.state,
                                                                                              self.captured, self.alive)
