import unittest
import pygame

from gym_buster.envs.game_classes.game import Game
from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.ghost import Ghost


class GameTest(unittest.TestCase):

    def reset(self):
        Buster._reset_busters()
        Ghost._reset_ghost()

    def test_buster_busting(self):
        """
        Test one buster is busting a ghost in its range and move back to home
        """
        game = Game('human', 1, 1, 1)

        game.busters[0].x = 9000
        game.busters[0].y = 4500
        game.ghosts[0].x = 9800
        game.ghosts[0].y = 5500

        game.game_render()
        commands_0 = ["BUST 1"]
        commands_1 = ["MOVE 9000 4500"]
        game._run_round(commands_0, commands_1)

        game.game_render()
        pygame.display.flip()
        game.clock.tick(Constants.FPS)

        self.assertTrue(game.score_team_0 == 1)
        self.assertTrue(game.score_team_1 == 0)
        self.assertTrue(game.ghosts[0].x == game.busters[0].x)
        self.assertTrue(game.ghosts[0].y == game.busters[0].y)
        self.assertTrue(game.ghosts[0].captured)
        self.assertTrue(game.ghosts[0].alive)
        self.assertTrue(game.ghosts[0].value == 1)
        self.assertTrue(game.busters[0].state == Constants.STATE_BUSTER_CARRYING)
        self.assertTrue(game.busters[0].value == game.ghosts[0].id)
        self.assertTrue(game.busters[0].action == Constants.ACTION_BUSTING)

        commands_0 = ["MOVE 50 50"]
        game._run_round(commands_0, commands_1)
        game.game_render()
        pygame.display.flip()

        self.assertTrue(game.score_team_0 == 1)
        self.assertTrue(game.score_team_1 == 0)
        self.assertTrue(game.ghosts[0].x == game.busters[0].x)
        self.assertTrue(game.ghosts[0].y == game.busters[0].y)
        self.assertTrue(game.ghosts[0].value == 1)
        self.assertTrue(game.ghosts[0].captured)
        self.assertTrue(game.ghosts[0].alive)
        self.assertTrue(game.busters[0].value == game.ghosts[0].id)
        self.assertTrue(game.busters[0].action == Constants.ACTION_MOVING)
        self.assertTrue(game.busters[0].state == Constants.STATE_BUSTER_CARRYING)

        self.reset()

    def test_buster_busting_same_range(self):
        """
        Test two busters busting same ghost at same distance
        """
        game = Game('human', 1, 1, 1)

        game.busters[0].x = 10100
        game.busters[0].y = 4500
        game.busters[1].x = 7900
        game.busters[1].y = 4500
        game.ghosts[0].x = 9000
        game.ghosts[0].y = 4500

        game.game_render()
        commands_0 = ["BUST 1"]
        commands_1 = ["BUST 1"]
        game._run_round(commands_0, commands_1)

        self.assertTrue(game.score_team_0 == 0)
        self.assertTrue(game.score_team_1 == 0)
        self.assertTrue(not(game.ghosts[0].x == game.busters[0].x and game.ghosts[0].y == game.busters[0].y))
        self.assertTrue(not(game.ghosts[0].x == game.busters[1].x and game.ghosts[0].y == game.busters[1].y))
        self.assertFalse(game.ghosts[0].captured)
        self.assertTrue(game.ghosts[0].alive)
        self.assertTrue(game.ghosts[0].value == 2)
        self.assertTrue(game.busters[0].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(game.busters[0].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(game.busters[0].action == Constants.ACTION_BUSTING)
        self.assertTrue(game.busters[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(game.busters[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(game.busters[1].action == Constants.ACTION_BUSTING)

        self.reset()

    def test_buster_busting_captured_ghost(self):
        """
        One buster trying to bust the ghost carried by another buster
        """
        game = Game('human', 1, 1, 1)

        game.busters[0].x = 9000
        game.busters[0].y = 4500
        game.busters[0].state = Constants.STATE_BUSTER_CARRYING
        game.busters[0].value = game.ghosts[0].id

        game.ghosts[0].x = game.busters[0].x
        game.ghosts[0].y = game.busters[0].y
        game.ghosts[0].value = 1
        game.ghosts[0].captured = True
        game.score_team_0 = 1

        game.busters[1].x = 7800
        game.busters[1].y = 3900

        game.game_render()
        commands_0 = ["MOVE 50 50"]
        commands_1 = ["BUST 1"]
        game._run_round(commands_0, commands_1)

        self.assertTrue(game.score_team_0 == 1)
        self.assertTrue(game.score_team_1 == 0)
        self.assertTrue(game.ghosts[0].x == game.busters[0].x)
        self.assertTrue(game.ghosts[0].y == game.busters[0].y)
        self.assertTrue(game.ghosts[0].captured)
        self.assertTrue(game.ghosts[0].alive)
        self.assertTrue(game.ghosts[0].value == 1)
        self.assertTrue(game.busters[0].state == Constants.STATE_BUSTER_CARRYING)
        self.assertTrue(game.busters[0].value == game.ghosts[0].id)
        self.assertTrue(game.busters[0].action == Constants.ACTION_MOVING)
        self.assertTrue(game.busters[1].state == Constants.STATE_BUSTER_NOTHING)
        self.assertTrue(game.busters[1].value == Constants.VALUE_BUSTER_NOTHING)
        self.assertTrue(game.busters[1].action == Constants.ACTION_BUSTING)

        self.reset()
