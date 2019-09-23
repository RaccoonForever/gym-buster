from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.constants import Constants


class TestUtils:

    @staticmethod
    def generate_entities():
        entity1 = Entity(Constants.TYPE_BUSTER_TEAM_1)
        entity1.x = 8000 + 200
        entity1.y = 4500 + 200
        entity1.id = 1
        entity2 = Entity(Constants.TYPE_BUSTER_TEAM_1)
        entity2.x = 8000 - 200
        entity2.y = 4500 + 200
        entity2.id = 2
        entity3 = Entity(Constants.TYPE_BUSTER_TEAM_1)
        entity3.x = 8000 - 200
        entity3.y = 4500 - 200
        entity3.id = 3
        entity4 = Entity(Constants.TYPE_BUSTER_TEAM_1)
        entity4.x = 8000 + 800
        entity4.y = 4500 - 3500
        entity4.id = 4

        return [entity1, entity2, entity3, entity4]

    @staticmethod
    def generate_ghosts():
        ghost1 = Entity(Constants.TYPE_GHOST)
        ghost1.x = 8300
        ghost1.y = 4500
        ghost1.id = 1
        ghost2 = Entity(Constants.TYPE_GHOST)
        ghost2.x = 9300
        ghost2.y = 1500
        ghost2.id = 2
        ghost3 = Entity(Constants.TYPE_GHOST)
        ghost3.x = 0
        ghost3.y = 0
        ghost3.id = 3

        return [ghost1, ghost2, ghost3]
