import unittest

from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.buster_env import BusterEnv


class GameTest(unittest.TestCase):

    def reset(self):
        Ghost.reset_ghost()

    def test_buster_busting(self):
        """
        Test one buster is busting a ghost in its range and move back to home
        """
        environment = BusterEnv()

        environment.reset()

        environment.buster_team0[0].x = 9000
        environment.buster_team0[0].y = 4500
        environment.ghosts[0].x = 9800
        environment.ghosts[0].y = 5500

        commands_0 = ["BUST 0", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "MOVE 9000 4500", "MOVE 9000 4500"]
        environment._run_step(commands_0, commands_1)

        self.assertTrue(environment.score_team0 == 1)
        self.assertTrue(environment.score_team1 == 0)
        self.assertTrue(environment.ghosts[0].x == environment.buster_team0[0].x)
        self.assertTrue(environment.ghosts[0].y == environment.buster_team0[0].y)
        self.assertTrue(environment.ghosts[0].captured)
        self.assertTrue(environment.ghosts[0].alive)
        self.assertTrue(environment.ghosts[0].value == 1)
        self.assertTrue(environment.buster_team0[0].state == Constants.STATE_BUSTER_CARRYING)
        self.assertTrue(environment.buster_team0[0].value == environment.ghosts[0].id)
        self.assertTrue(environment.buster_team0[0].action == Constants.ACTION_BUSTING)

        commands_0 = ["MOVE 50 50", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "MOVE 9000 4500", "MOVE 9000 4500"]

        environment._run_step(commands_0, commands_1)

        self.assertTrue(environment.score_team0 == 1)
        self.assertTrue(environment.score_team1 == 0)
        self.assertTrue(environment.ghosts[0].x == environment.buster_team0[0].x)
        self.assertTrue(environment.ghosts[0].y == environment.buster_team0[0].y)
        self.assertTrue(environment.ghosts[0].value == 1)
        self.assertTrue(environment.ghosts[0].captured)
        self.assertTrue(environment.ghosts[0].alive)
        self.assertTrue(environment.buster_team0[0].value == environment.ghosts[0].id)
        self.assertTrue(environment.buster_team0[0].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team0[0].state == Constants.STATE_BUSTER_CARRYING)

        self.reset()

    def test_buster_busting_same_range(self):
        """
        Test two busters busting same ghost at same distance
        """
        environment = BusterEnv()
        environment.reset()

        environment.buster_team0[0].x = 10100
        environment.buster_team0[0].y = 4500
        environment.buster_team1[1].x = 7900
        environment.buster_team1[1].y = 4500
        environment.ghosts[0].x = 9000
        environment.ghosts[0].y = 4500

        commands_0 = ["BUST 0", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "BUST 0", "MOVE 9000 4500"]
        environment._run_step(commands_0, commands_1)

        self.assertTrue(environment.score_team0 == 0)
        self.assertTrue(environment.score_team1 == 0)
        self.assertTrue(not (environment.ghosts[0].x == environment.buster_team0[0].x and environment.ghosts[0].y ==
                             environment.buster_team0[0].y))
        self.assertTrue(not (environment.ghosts[0].x == environment.buster_team1[1].x and environment.ghosts[0].y ==
                             environment.buster_team1[1].y))
        self.assertFalse(environment.ghosts[0].captured)
        self.assertTrue(environment.ghosts[0].alive)
        self.assertTrue(environment.ghosts[0].value == Constants.VALUE_GHOST_BASIC)
        self.assertTrue(environment.buster_team0[0].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[0].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[0].action == Constants.ACTION_NOTHING)
        self.assertTrue(environment.buster_team1[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[1].action == Constants.ACTION_NOTHING)

        self.reset()

    def test_buster_busting_captured_ghost(self):
        """
        One buster trying to bust the ghost carried by another buster
        """
        environment = BusterEnv()
        environment.reset()

        environment.buster_team0[0].x = 9000
        environment.buster_team0[0].y = 4500
        environment.ghosts[0].x = 9800
        environment.ghosts[0].y = 5500

        commands_0 = ["BUST 0", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "MOVE 9000 4500", "MOVE 9000 4500"]
        environment._run_step(commands_0, commands_1)

        environment.buster_team1[0].x = 7800
        environment.buster_team1[0].y = 3900

        commands_0 = ["MOVE 50 50", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "MOVE 9000 4500", "BUST 0"]
        environment._run_step(commands_0, commands_1)

        self.assertTrue(environment.score_team0 == 1)
        self.assertTrue(environment.score_team1 == 0)
        self.assertTrue(environment.ghosts[0].x == environment.buster_team0[0].x)
        self.assertTrue(environment.ghosts[0].y == environment.buster_team0[0].y)
        self.assertTrue(environment.ghosts[0].captured)
        self.assertTrue(environment.ghosts[0].alive)
        self.assertTrue(environment.ghosts[0].value == 1)
        self.assertTrue(environment.buster_team0[0].state == Constants.STATE_BUSTER_CARRYING)
        self.assertTrue(environment.buster_team0[0].value == environment.ghosts[0].id)
        self.assertTrue(environment.buster_team0[0].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[2].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[2].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[2].action == Constants.ACTION_NOTHING)

        self.reset()

    def test_buster_busting_his_own_ghost(self):
        """
        its own ghost and another same team trying busting
        """
        environment = BusterEnv()
        environment.reset()

        environment.buster_team0[0].x = 9000
        environment.buster_team0[0].y = 4500
        environment.ghosts[0].x = 9800
        environment.ghosts[0].y = 5500

        commands_0 = ["BUST 0", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "MOVE 9000 4500", "MOVE 9000 4500"]
        environment._run_step(commands_0, commands_1)

        self.assertTrue(environment.score_team0 == 1)
        self.assertTrue(environment.score_team1 == 0)

        self.assertTrue(environment.buster_team0[0].state == Constants.STATE_BUSTER_CARRYING)
        self.assertTrue(environment.buster_team0[0].value == environment.ghosts[0].id)
        self.assertTrue(environment.buster_team0[0].action == Constants.ACTION_BUSTING)
        self.assertTrue(environment.buster_team0[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[1].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team0[2].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[2].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[2].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[0].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[0].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[0].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[1].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[2].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[2].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[2].action == Constants.ACTION_MOVING)

        commands_0 = ["BUST 0", "MOVE 9000 4500", "MOVE 9000 4500"]
        commands_1 = ["MOVE 9000 4500", "MOVE 9000 4500", "MOVE 9000 4500"]
        environment._run_step(commands_0, commands_1)

        self.assertTrue(environment.score_team0 == 1)
        self.assertTrue(environment.score_team1 == 0)

        self.assertTrue(environment.ghosts[0].x == environment.buster_team0[0].x)
        self.assertTrue(environment.ghosts[0].y == environment.buster_team0[0].y)
        self.assertTrue(environment.ghosts[0].captured)
        self.assertTrue(environment.ghosts[0].alive)
        self.assertTrue(environment.ghosts[0].value == 1)

        self.assertTrue(environment.buster_team0[0].state == Constants.STATE_BUSTER_CARRYING)
        self.assertTrue(environment.buster_team0[0].value == environment.ghosts[0].id)
        self.assertTrue(environment.buster_team0[0].action == Constants.ACTION_NOTHING)
        self.assertTrue(environment.buster_team0[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[1].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team0[2].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[2].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team0[2].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[0].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[0].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[0].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[1].action == Constants.ACTION_MOVING)
        self.assertTrue(environment.buster_team1[2].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[2].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(environment.buster_team1[2].action == Constants.ACTION_MOVING)
