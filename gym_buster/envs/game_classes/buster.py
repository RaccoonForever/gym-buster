import re
from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.constants import Constants

from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.game_classes.math_utils import MathUtility


class Buster(Entity):

    def __init__(self, team, id):
        super(Buster, self).__init__(team)
        self.id = id
        self._generate_buster_position()
        self.action = Constants.ACTION_NOTHING
        self.value = Constants.VALUE_BUSTER_NOTHING

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
            raise ValueError("Entity neither in team 0 or team 1")

    @property
    def is_in_team_base(self):
        """
        Function that gives us true if the buster is in team base
        :return: true or false
        """
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            return self.is_in_team_0_base
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            return self.is_in_team_1_base

    #
    #     # -------------- PRIVATE FUNCTIONS AND PROPERTIES ----------------#
    #
    # -------------- CAN PERFORM ACTION FUNCTIONS ----------------#

    def can_bust(self, ghost):
        """
        Function that will tell if you can bust the ghost
        :param ghost: the ghost to bust
        :return: true or false
        """
        distance = MathUtility.distance(ghost.x, ghost.y, self.x, self.y)
        return Constants.BUSTER_BUST_MIN_RANGE <= distance <= Constants.BUSTER_BUST_MAX_RANGE

    # -------------- END CAN PERFORM ACTION FUNCTIONS ----------------#

    # -------------- ACTION FUNCTIONS ----------------#

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
                return 0
            elif release:
                return self.release()
            elif bust:
                self.bust(int(bust.group(1)))
                return 0
            else:
                raise Exception(
                    "Wrong command for buster : " + str(self) + " , x : " + str(self.x) + ", y : " + str(self.y))
        except Exception as exc:
            raise exc

    def move(self, x, y):
        """
        Execute the moving action
        :param x: x coordinate
        :param y: y coordinate
        """
        super(Buster, self).move(x, y)
        self.action = Constants.ACTION_MOVING
        print("Buster team {} with id {} moving to X: {}, Y: {}".format(self.type, self.id, self.x, self.y))

    def release(self):
        """
        Execute the action to release the ghost
        """
        if self.value != Constants.VALUE_BUSTER_NOTHING and self.state == Constants.STATE_BUSTER_CARRYING:
            ghost = Ghost.get_ghost(self.value)
            ghost.being_released(self)

            self.value = Constants.VALUE_BUSTER_NOTHING
            self.state = Constants.STATE_BUSTER_NOTHING
            self.action = Constants.ACTION_RELEASING

            print("Buster team {} with id {} releasing ghost id : {} at X: {}, Y: {}".format(self.type, self.id,
                                                                                             ghost.id, self.x, self.y))

            return -1
        else:
            self.action = Constants.ACTION_NOTHING
            print("Buster team {} with id {} has nothing to release".format(self.type, self.id))

            return 0

    def bust(self, ids):
        """
        Execute the action to catch a ghost with id ids
        :param ids: the ghost to catch
        """
        ghost = Ghost.get_ghost(ids)
        if self.state == Constants.STATE_BUSTER_NOTHING and ghost and self.can_bust(ghost) and not ghost.captured:
            ghost.value += 1
            self.value = ids
            self.action = Constants.ACTION_BUSTING
            print("Buster team {} with id {} busting ghost id : {}".format(self.type, self.id, ids))
        else:
            self.action = Constants.ACTION_NOTHING
            print("Buster team {} with id {} failed busting".format(self.type, self.id))

    def cancelling_bust(self):
        """
        Cancel the busting when another buster won the ghost
        """
        self.action = Constants.ACTION_NOTHING
        self.value = Constants.VALUE_BUSTER_NOTHING
        self.state = Constants.STATE_BUSTER_NOTHING
        print("Buster team {} with id {} cancelled busting".format(self.type, self.id))

    def capturing_ghost(self):
        """
        Function that will change the state of the buster
        """
        self.state = Constants.STATE_BUSTER_CARRYING
        print("Buster team {} with id {} captured ghost id : {}".format(self.type, self.id, self.value))

    # -------------- END ACTION FUNCTIONS ----------------#

    def __str__(self):
        """
        Display function
        """
        return 'Buster team {}, Id: {}, X: {}, Y: {}, Action: {}, Value: {}, State: {}'.format(
            self.type, self.id, self.x, self.y, self.action, self.value, self.state)
