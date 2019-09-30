import unittest

from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.game_classes.constants import Constants


class BusterTest(unittest.TestCase):

    def reset(self):
        Ghost.reset_ghost()

    def test_generate_buster_position(self):
        buster = Buster(Constants.TYPE_BUSTER_TEAM_1, 1)
        self.assertTrue(buster.x == Constants.MAP_WIDTH - 50)
        self.assertTrue(buster.y == Constants.MAP_HEIGHT - 50)

        buster = Buster(Constants.TYPE_BUSTER_TEAM_0, 1)
        self.assertTrue(buster.x == 50)
        self.assertTrue(buster.y == 50)

    def test_can_bust(self):
        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0, 1)
        ghost = Ghost(1)
        ghost.x = 3000
        ghost.y = 3000
        self.assertFalse(buster1.can_bust(ghost))

        ghost.x = 250
        ghost.y = 250
        self.assertFalse(buster1.can_bust(ghost))

        ghost.x = 1100
        ghost.y = 1100
        self.assertTrue(buster1.can_bust(ghost))

        self.reset()

    def test_release(self):
        ghost1 = Ghost(1)
        ghost2 = Ghost(2)

        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0, 1)
        buster1.value = ghost1.id
        buster1.state = Constants.STATE_BUSTER_CARRYING
        buster1.action = Constants.ACTION_MOVING

        buster1.release()
        self.assertTrue(ghost1.x == buster1.x)
        self.assertTrue(ghost1.y == buster1.y)
        self.assertTrue(ghost1.angle == buster1.angle)
        self.assertTrue(ghost1.value == Constants.VALUE_GHOST_BASIC)
        self.assertTrue(buster1.value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(buster1.state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(buster1.action == Constants.ACTION_RELEASING)

        self.reset()

    def test_bust(self):
        ghost1 = Ghost(1)
        ghost2 = Ghost(2)
        ghost2.x = 3500
        ghost2.y = 3500

        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0, 1)
        buster1.x = 3600
        buster1.y = 3600

        buster1.bust(2)
        self.assertTrue(buster1.value == Constants.VALUE_BUSTER_NOTHING)
        self.assertFalse(ghost2.value == 1)
        self.assertTrue(buster1.action == Constants.ACTION_NOTHING)
        self.assertTrue(buster1.state == Constants.STATE_BUSTER_NOTHING)

        buster1.x = 4300
        buster1.y = 4300
        buster1.bust(2)
        self.assertTrue(buster1.value == ghost2.id)
        self.assertTrue(ghost2.value == 1)
        self.assertTrue(buster1.action == Constants.ACTION_BUSTING)
        self.assertTrue(buster1.state == Constants.STATE_BUSTER_NOTHING)

        buster2 = Buster(Constants.TYPE_BUSTER_TEAM_1, 1)
        buster2.x = 2500
        buster2.y = 2500
        buster2.bust(2)
        self.assertTrue(buster2.value == ghost2.id)
        self.assertTrue(ghost2.value == 2)
        self.assertTrue(buster1.value == ghost2.id)
        self.assertTrue(buster1.action == Constants.ACTION_BUSTING)
        self.assertTrue(buster2.action == Constants.ACTION_BUSTING)
        self.assertTrue(buster1.state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(buster2.state == Constants.STATE_BUSTER_NOTHING)

        self.reset()
