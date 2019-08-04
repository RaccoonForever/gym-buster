import re
import copy

from .entity import Entity
from .constants import Constants
from .ghost import Ghost
from .math_utils import MathUtility


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
        self.action = Constants.ACTION_NOTHING
        self._generate_buster_position()
        print(
            "Buster : " + str(self.id) + ", position : " + str(self.x) + " " + str(self.y))

    @classmethod
    def _generate_id(cls, team, obj):
        """
        Function that will generate the id for the buster
        :param team: the entity team
        :return: the id
        """
        if team == Constants.TYPE_BUSTER_TEAM_0:
            ids = copy.copy(cls.entity_type_0_id)
            cls.entity_type_0_id += 1
            cls.busters_0.append(obj)
            return ids
        elif team == Constants.TYPE_BUSTER_TEAM_1:
            ids = copy.copy(cls.entity_type_1_id)
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
        return None

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
            raise ValueError("Entity neither in team 0 or team 1")

    def is_in_team_base(self):
        """
        Function that gives us true if the buster is in team base
        :return: true or false
        """
        if self.type == Constants.TYPE_BUSTER_TEAM_0:
            return self.is_in_team_0_base()
        elif self.type == Constants.TYPE_BUSTER_TEAM_1:
            return self.is_in_team_1_base()

    def can_bust(self, ghost):
        """
        Function that will tell if you can bust the ghost
        :param ghost: the ghost to bust
        :return: true or false
        """
        distance = MathUtility.distance(ghost.x, ghost.y, self.x, self.y)
        return Constants.BUSTER_BUST_MIN_RANGE <= distance <= Constants.BUSTER_BUST_MAX_RANGE

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
                self.action = Constants.ACTION_MOVING
                print(str(self.id) + " moving to " + str(self.x) + " " + str(self.y))
                return 0
            elif release:
                result = self.release()
                self.action = Constants.ACTION_RELEASING
                return result
            elif bust:
                self.bust(int(bust.group(1)))
                self.action = Constants.ACTION_BUSTING
                return 0
            else:
                raise Exception(
                    "Wrong command for buster : " + str(self.id) + " , x : " + str(self.x) + ", y : " + str(self.y))
        except Exception as exc:
            raise exc

    def release(self):
        """
        Execute the action to release the ghost
        """
        if self.value != Constants.VALUE_BUSTER_NOTHING and self.state == Constants.STATE_BUSTER_CARRYING:
            ghost = Ghost.get_ghost(self.value)
            ghost.being_released(self)

            print(str(self.id) + " releasing " + str(self.value))

            self.value = Constants.VALUE_BUSTER_NOTHING
            self.state = Constants.STATE_BUSTER_NOTHING

            return -1

        return 0

    def bust(self, ids):
        """
        Execute the action to catch a ghost with id ids
        :param ids: the ghost to catch
        """
        ghost = Ghost.get_ghost(ids)
        if self.state == Constants.STATE_BUSTER_NOTHING and ghost and self.can_bust(ghost):
            ghost.value += 1
            self.value = ids
            print(str(self.id) + " busting " + str(ids))

    def capturing_ghost(self):
        """
        Function that will change the state of the buster
        :param ghost: the captured ghost
        """
        self.state = Constants.STATE_BUSTER_CARRYING
