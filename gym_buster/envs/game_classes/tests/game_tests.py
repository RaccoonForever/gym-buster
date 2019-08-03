import unittest
import pygame

from gym_buster.envs.game_classes.game import Game
from gym_buster.envs.game_classes.constants import Constants


class GameTest(unittest.TestCase):

    def test_buster_busting(self):
        """
        Test one buster is busting a ghost in its range
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

        commands_0 = ["MOVE 50 50"]
        game._run_round(commands_0, commands_1)
        game.game_render()
        pygame.display.flip()

        self.assertTrue(game.score_team_0 == 1)
        self.assertTrue(game.score_team_1 == 0)
        self.assertTrue(game.ghosts[0].x == game.busters[0].x)
        self.assertTrue(game.ghosts[0].y == game.busters[0].y)
