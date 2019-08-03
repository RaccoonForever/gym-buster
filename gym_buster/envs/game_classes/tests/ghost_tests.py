import unittest

from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.ghost import Ghost


class GhostTest(unittest.TestCase):

    def reset(self):
        Buster._reset_busters()
        Ghost._reset_ghost()

