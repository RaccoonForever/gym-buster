import unittest

from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.constants import Constants

class EntityTest(unittest.TestCase):
    
    def __init__(self):
        self.entity = Entity(Constants.TYPE_BUSTER_TEAM_0)
    
    def test_is_in_team_0_base(self):
        self.entity.x = 0
        self.entity.y = 0
        self.assertTrue(self.entity.is_in_team_0_base())
        
        self.entity.x = 1000
        self.entity.y = 1000
        self.assertTrue(self.entity.is_in_team_0_base())
        
        self.entity.x = 2000
        self.entity.y = 2000
        self.assertFalse(self.entity.is_in_team_0_base())
    
    def test_is_in_team_1_base(self):
        self.entity.x = 0
        self.entity.y = 0
        self.assertTrue(self.entity.is_in_team_0_base())
        
