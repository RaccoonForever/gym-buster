import unittest

from gym_buster.envs.game_classes.ghost import Ghost


class GhostTest(unittest.TestCase):

    def reset(self):
        Ghost.reset_ghost()

