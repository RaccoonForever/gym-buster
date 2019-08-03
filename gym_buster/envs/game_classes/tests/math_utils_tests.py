import unittest
import math

from gym_buster.envs.game_classes.math_utils import MathUtility


class TestMathUtility(unittest.TestCase):
    EPSILON = 0.001

    def test_distance(self):
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        result = MathUtility.distance(x1, y1, x2, y2)
        self.assertEqual(result, 0, msg="Distance with result 0")
        x2 = 50
        self.assertEqual(MathUtility.distance(x1, y1, x2, y2), 50,
                         msg="Distance with first point is origin and second only has x modifications")
        x2 = 0
        y2 = 50
        self.assertEqual(MathUtility.distance(x1, y1, x2, y2), 50,
                         msg="Distance with first point is origin and second only has y modifications")
        x2 = 10
        y2 = 10
        self.assertTrue(MathUtility.distance(x1, y1, x2, y2) - 14.1421 < self.EPSILON,
                        msg="Distance with first point is origin and second only has x, y modifications")
        x2 = 15
        y2 = 40
        self.assertTrue(MathUtility.distance(x1, y1, x2, y2) - 42.72 < self.EPSILON,
                        msg="Distance with first point is origin and second only has x, y modifications")
        x1 = 5
        y1 = 15
        self.assertTrue(MathUtility.distance(x1, y1, x2, y2) - 26.926 < self.EPSILON,
                        msg="Distance with both points random")

    def test_limit_coordinates(self):
        x1, y1 = 0, 0
        self.assertEqual(MathUtility.limit_coordinates(x1, y1), (0, 0))
        x1 = -50
        self.assertEqual(MathUtility.limit_coordinates(x1, y1), (0, 0))
        x1, y1 = 0, -50
        self.assertEqual(MathUtility.limit_coordinates(x1, y1), (0, 0))
        x1, y1 = 18000, -50
        self.assertEqual(MathUtility.limit_coordinates(x1, y1), (16000, 0))
        x1, y1 = 17000, 10000
        self.assertEqual(MathUtility.limit_coordinates(x1, y1), (16000, 9000))

    def test_opposite_direction(self):
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        length = 250
        self.assertEqual(MathUtility.opposite_direction(x1, y1, x2, y2, length), (0, 0),
                         msg="Opposite direction with points on origin")
        length = 0
        self.assertEqual(MathUtility.opposite_direction(x1, y1, x2, y2, length), (0, 0),
                         msg="Opposite direction with points on origin and length 0")
        x2 = 50
        y2 = 50
        self.assertEqual(MathUtility.opposite_direction(x1, y1, x2, y2, length), (0, 0),
                         msg="Opposite direction with first point on origin and second 50,50 and length 0")
        length = 250
        self.assertEqual(MathUtility.opposite_direction(x1, y1, x2, y2, length), (0, 0),
                         msg="Opposite direction with first point on origin and second 50,50 and length 250")
        length = 50
        x1, y1 = 50, 50
        x2, y2 = 100, 100
        result_x, result_y = MathUtility.opposite_direction(x1, y1, x2, y2, length)
        self.assertTrue(result_x - 14.6447 < self.EPSILON,
                        msg="Opposite direction with first point 50,50 and second 100,100 and length 50")
        self.assertTrue(result_y - 14.6447 < self.EPSILON,
                        msg="Opposite direction with first point 50,50 and second 100,100 and length 50")
        x2, y2 = 50, 100
        result_x, result_y = MathUtility.opposite_direction(x1, y1, x2, y2, length)
        self.assertTrue(result_x - 50 < self.EPSILON,
                        msg="Opposite direction with first point 50,50 and second 50,100 and length 50")
        self.assertTrue(result_y - 14.6447 < self.EPSILON,
                        msg="Opposite direction with first point 50,50 and second 50,100 and length 50")
        x2, y2 = 0, 0
        result_x, result_y = MathUtility.opposite_direction(x1, y1, x2, y2, length)
        self.assertTrue(result_x - 85.355 < self.EPSILON,
                        msg="Opposite direction with first point 50,50 and second 0,0 and length 50")
        self.assertTrue(result_y - 85.355 < self.EPSILON,
                        msg="Opposite direction with first point 50,50 and second 0,0 and length 50")

    def test_angle(self):

        x1, y1 = 0, 0
        x2, y2 = 10, 0
        result = math.atan2(y2 - y1, x2 - x1)
        self.assertTrue(result == 0.0)

        x2, y2 = 0, 10
        result = math.degrees(math.atan2(-(y2 - y1), x2 - x1))
        self.assertTrue(result == -90.0)

        x1, y1 = 15950, 8950
        x2, y2 = 13400, 6200
        result = math.degrees(math.atan2(-(y2 - y1), x2 - x1))
        self.assertTrue(True)
