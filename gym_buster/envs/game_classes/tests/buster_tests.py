import unittest

from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.game_classes.constants import Constants


class BusterTest(unittest.TestCase):

    def reset(self):
        Buster._reset_busters()
        Ghost._reset_ghost()

    def test_generate_buster_position(self):
        buster = Buster(Constants.TYPE_BUSTER_TEAM_1)
        self.assertTrue(buster.x == Constants.MAP_WIDTH - 50)
        self.assertTrue(buster.y == Constants.MAP_HEIGHT - 50)

        buster = Buster(Constants.TYPE_BUSTER_TEAM_0)
        self.assertTrue(buster.x == 50)
        self.assertTrue(buster.y == 50)
        self.reset()

    def test_get_buster(self):
        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_1)
        buster2 = Buster(Constants.TYPE_BUSTER_TEAM_1)
        buster3 = Buster(Constants.TYPE_BUSTER_TEAM_1)
        buster4 = Buster(Constants.TYPE_BUSTER_TEAM_1)

        entities = [buster1, buster2, buster3, buster4]
        self.assertTrue(Buster.get_buster(entities, 2, Constants.TYPE_BUSTER_TEAM_1) == buster2)

        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        buster2 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        buster3 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        buster4 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        entities = [buster1, buster2, buster3, buster4]
        self.assertTrue(Buster.get_buster(entities, 3, Constants.TYPE_BUSTER_TEAM_0) == buster3)
        self.reset()

    def test_can_bust(self):
        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        ghost = Ghost()
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
        ghost1 = Ghost()
        ghost2 = Ghost()  # To increase by 1 the counter in Ghost class

        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        buster1.value = ghost1.id
        buster1.state = Constants.STATE_BUSTER_CARRYING

        buster1.release()
        self.assertTrue(ghost1.x == buster1.x)
        self.assertTrue(ghost1.y == buster1.y)
        self.assertTrue(ghost1.angle == buster1.angle)
        self.assertTrue(ghost1.value == Constants.VALUE_GHOST_BASIC)
        self.assertTrue(buster1.value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(buster1.state == Constants.STATE_BUSTER_NOTHING)

        self.reset()

    def test_bust(self):
        ghost1 = Ghost()
        ghost2 = Ghost()
        ghost2.x = 3500
        ghost2.y = 3500

        buster1 = Buster(Constants.TYPE_BUSTER_TEAM_0)
        buster1.state = Constants.STATE_BUSTER_NOTHING
        buster1.x = 3600
        buster1.y = 3600

        buster1.bust(2)
        self.assertFalse(buster1.value == ghost2.id)
        self.assertFalse(ghost2.value == 1)

        buster1.x = 4300
        buster1.y = 4300
        buster1.bust(2)
        self.assertTrue(buster1.value == ghost2.id)
        self.assertTrue(ghost2.value == 1)

        buster2 = Buster(Constants.TYPE_BUSTER_TEAM_1)
        buster2.state = Constants.STATE_BUSTER_NOTHING
        buster2.x = 2500
        buster2.y = 2500
        buster2.bust(2)
        self.assertTrue(buster2.value == ghost2.id)
        self.assertTrue(ghost2.value == 2)
        self.assertTrue(buster1.value == ghost2.id)

        self.reset()
