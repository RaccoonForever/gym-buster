import unittest

from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.math_utils import MathUtility
from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.tests.tests_utils import TestUtils


class EntityTest(unittest.TestCase):
    EPSILON = 1

    def __init__(self, *args, **kwargs):
        super(EntityTest, self).__init__(*args, **kwargs)
        self.entity = Entity(Constants.TYPE_BUSTER_TEAM_0)
        self.entity.x = 0
        self.entity.y = 0

    def test_is_in_team_0_base(self):
        self.assertTrue(self.entity.is_in_team_0_base())

        self.entity.x = 1000
        self.entity.y = 1000
        self.assertTrue(self.entity.is_in_team_0_base())

        self.entity.x = 2000
        self.entity.y = 2000
        self.assertFalse(self.entity.is_in_team_0_base())

    def test_is_in_team_1_base(self):
        self.entity.x = Constants.MAP_WIDTH
        self.entity.y = Constants.MAP_HEIGHT
        self.assertTrue(self.entity.is_in_team_1_base())

        self.entity.x = Constants.MAP_WIDTH - 1000
        self.entity.y = Constants.MAP_HEIGHT - 1000
        self.assertTrue(self.entity.is_in_team_1_base())

        self.entity.x = Constants.MAP_WIDTH - 2500
        self.entity.y = Constants.MAP_HEIGHT - 2500
        self.assertFalse(self.entity.is_in_team_1_base())

    def test_compute_max_move(self):
        res_x, res_y = self.entity._compute_max_move(Constants.BUSTER_MAX_MOVE - 200, 0)
        self.assertTrue(res_x == Constants.BUSTER_MAX_MOVE - 200)
        self.assertTrue(res_y == 0)

        res_x, res_y = self.entity._compute_max_move(Constants.BUSTER_MAX_MOVE, 0)
        self.assertTrue(res_x == Constants.BUSTER_MAX_MOVE)
        self.assertTrue(res_y == 0)

        res_x, res_y = self.entity._compute_max_move(Constants.BUSTER_MAX_MOVE * 2, 0)
        self.assertTrue(res_x == Constants.BUSTER_MAX_MOVE)
        self.assertTrue(res_y == 0)

        res_x, res_y = self.entity._compute_max_move(0, Constants.BUSTER_MAX_MOVE * 2)
        self.assertTrue(res_x == 0)
        self.assertTrue(res_y == Constants.BUSTER_MAX_MOVE)

        self.entity.x = 2000
        self.entity.y = 2000
        res_x, res_y = self.entity._compute_max_move(self.entity.x + Constants.BUSTER_MAX_MOVE - 200, self.entity.y)
        self.assertTrue(res_x == (self.entity.x + Constants.BUSTER_MAX_MOVE - 200))
        self.assertTrue(res_y == self.entity.y)

        res_x, res_y = self.entity._compute_max_move(self.entity.x, self.entity.y + Constants.BUSTER_MAX_MOVE - 200)
        self.assertTrue(res_x == self.entity.x)
        self.assertTrue(res_y == (self.entity.y + Constants.BUSTER_MAX_MOVE - 200))

        res_x, res_y = self.entity._compute_max_move(self.entity.x - Constants.BUSTER_MAX_MOVE + 200, self.entity.y)
        self.assertTrue(res_x == (self.entity.x - Constants.BUSTER_MAX_MOVE + 200))
        self.assertTrue(res_y == self.entity.y)

        res_x, res_y = self.entity._compute_max_move(self.entity.x, self.entity.y - Constants.BUSTER_MAX_MOVE + 200)
        self.assertTrue(res_x == self.entity.x)
        self.assertTrue(res_y == (self.entity.y - Constants.BUSTER_MAX_MOVE + 200))

        res_x, res_y = self.entity._compute_max_move(self.entity.x + Constants.BUSTER_MAX_MOVE,
                                                     self.entity.y + Constants.BUSTER_MAX_MOVE)
        self.assertTrue((res_x <= 2565 + self.EPSILON) and (res_x >= 2565 - self.EPSILON))
        self.assertTrue((res_y <= 2565 + self.EPSILON) and (res_y >= 2565 - self.EPSILON))

        res_x, res_y = self.entity._compute_max_move(self.entity.x - Constants.BUSTER_MAX_MOVE,
                                                     self.entity.y - Constants.BUSTER_MAX_MOVE)
        self.assertTrue((res_x <= 1435 + self.EPSILON) and (res_x >= 1435 - self.EPSILON))
        self.assertTrue((res_y <= 1435 + self.EPSILON) and (res_y >= 1435 - self.EPSILON))

        res_x, res_y = self.entity._compute_max_move(self.entity.x - Constants.BUSTER_MAX_MOVE * 2,
                                                     self.entity.y - Constants.BUSTER_MAX_MOVE)
        self.assertTrue((res_x <= 1284 + self.EPSILON) and (res_x >= 1284 - self.EPSILON))
        self.assertTrue((res_y <= 1643 + self.EPSILON) and (res_y >= 1643 - self.EPSILON))

    def test_get_closest(self):
        self.entity.x = 8000
        self.entity.y = 4500

        entities = TestUtils.generate_entities()
        result_ent, dist = self.entity.get_closest(entities)
        self.assertTrue(result_ent.id == 1)
        self.assertTrue(dist == MathUtility.distance(self.entity.x, self.entity.y, entities[0].x, entities[0].y))

        result, dist = self.entity.get_closest([])
        self.assertTrue(result is None)
        self.assertTrue(dist == Constants.MAP_MAX_DISTANCE)

    def test_number_of_entities_in_range(self):
        self.entity.x = 8000
        self.entity.y = 4500

        entities = TestUtils.generate_entities()
        result = self.entity.get_number_entities_in_range(entities)
        self.assertTrue(result == 3)

        result = self.entity.get_number_entities_in_range([])
        self.assertTrue(result == 0)

    def test_entities_visible(self):
        entities = TestUtils.generate_entities()
        ghosts = TestUtils.generate_ghosts()

        result = Entity.get_entities_visible(entities, ghosts)
        self.assertTrue(len(result) == 2)
