import gym
from gym import spaces
import random, logging
import numpy as np
from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.game import Game

logger = logging.getLogger(__name__)


class BusterEnv(gym.Env):
    """
    Class that will handle a codebuster environment
    """
    metadata = {'render.modes': ['human', 'console']}

    def __init__(self, buster_number, ghost_number, episodes, max_steps):
        self.buster_number = int(buster_number)
        self.ghost_number = int(ghost_number)
        self.state = None
        self.observation = None
        self.previous_observation = None

        self.action_space = self._action_space()
        self.observation_space = self._observation_space()

        self.episodes = int(episodes)  # Number of games to do
        self.max_episodes_steps = int(max_steps)  # Number of max steps in a game
        self.episode_step = 0
        self.episodes_win = 0

        self.game = Game('human', self.ghost_number, self.buster_number, self.max_episodes_steps)

    def _action_space(self):
        """
        Action space for gym env

        For each buster : move_degree, move_distance, or bust or release

        :return: the space
        """
        action_low = []
        action_high = []
        for i in range(self.buster_number):
            action_low += [-1.0, -1.0, 0.0, 0.0]
            action_high += [1.0, 1.0, 1.0, 1.0]

        return spaces.Box(np.array(action_low), np.array(action_high))

    def _observation_space(self):
        """
        observation space for gym env

        team0 points, team 1 points

        for each buster : state(carrying or not), distance from closest ghost, number of ghosts in range,
        distance from closest ennemy, number of enemy in range

        :return: the space
        """
        obs_low = [0.0, 0.0]
        obs_high = [self.ghost_number, self.ghost_number]
        for i in range(self.buster_number):
            obs_low += [0.0, 0.0, 0.0, 0.0, 0.0]
            obs_high += [1.0, Constants.MAP_MAX_DISTANCE, self.ghost_number, Constants.MAP_MAX_DISTANCE,
                         self.buster_number]

        return spaces.Box(np.array(obs_low), np.array(obs_high))

    def _compute_reward(self):
        """
        Function that will compute reward for movement decided by the AI
        :return: the reward
        """
        # For now easy things

        # Battle over and won
        if self.state['battle_won']:
            return 4000
        # Battle over and lost
        if self.state['battle_ended'] and not self.state['battle_won']:
            return -4000
        # point + 1
        if self.observation[0] > self.previous_observation[0]:
            return 200
        # point - 1
        if self.observation[0] < self.previous_observation[0]:
            return -200

        return 0

    def _check_done(self):
        """
        Function that will say if a game is over
        :return: boolean
        """
        return self.state['battle_ended']

    def _get_info(self):
        """
        Function that will give some info for debugging
        :return: dictionnary with information
        """
        return {}  # TODO implement info

    def step(self, action):
        self.episode_step += 1

        # Run a step in the game
        actions = self._transform_action(action)
        self.game.run_step(actions)

        self.state = self.game.get_state()
        self.previous_observation = self.observation
        self.observation = self._make_observation()
        reward = self._compute_reward()
        done = self._check_done()
        info = self._get_info()

        return self.observation, reward, done, info

    def reset(self):

        if self.episode_step >= self.max_episodes_steps:
            # End it and start a new game
            self.game.exit()
            self.game = Game('human', self.ghost_number, self.buster_number, self.max_episodes_steps)

        self.episodes += 1
        self.episode_step = 0

        self.state = self.game.get_state()
        self.observation = self._make_observation()
        self.previous_observation = self.observation

        return self.observation

    def render(self, mode='human', close=False):
        pass

    def _transform_action(self, actions):
        """
        Transform actions fromm action space to commands
        :param actions: the actions
        :return: a list of 3 commands
        """
        result = ["" for i in range(self.buster_number)]
        for i in range(self.buster_number):
            # Privilege to bust then release then move
            if actions[i * 4 + 3] > 0.8:
                # Release
                result[i] = "RELEASE"
            elif actions[i * 4 + 2] > 0.8:
                # Bust the closest ghost
                ghost, dist = self.state['team0'][i].get_closest(self.state['ghostvisibleteam0'])
                if ghost:
                    result[i] = "BUST " + str(ghost.id)
                else:
                    result[i] = "MOVE " + str(self.state['team0'][i].x) + " " + str(self.state['team0'][i].y)
            else:
                # Move random for now
                x = random.randint(0, Constants.MAP_WIDTH)
                y = random.randint(0, Constants.MAP_HEIGHT)
                result[i] = "MOVE " + str(x) + " " + str(y)
        return result

    def _make_observation(self):
        """
        Compute the observation from the new state
        :return: an array with observations
        """
        observation = np.zeros(self.observation_space.shape)
        observation[0] = self.state['scoreteam0']
        observation[1] = self.state['scoreteam1']
        for i in range(self.buster_number):
            # state (carrying or not)
            observation[i * 5 + 2] = self.state['team0'][i].state
            # distance from closest ghost observable
            _, dist = self.state['team0'][i].get_closest(self.state['ghostvisibleteam0'])
            observation[i * 5 + 3] = dist
            # number of ghost in range
            observation[i * 5 + 4] = self.state['team0'][i].get_number_entities_in_range(
                self.state['ghostvisibleteam0'])
            # distance from closest ennemy
            _, dist = self.state['team0'][i].get_closest(self.state['ennemyvisibleteam0'])
            observation[i * 5 + 5] = dist
            # number of ennemy in range
            observation[i * 5 + 6] = self.state['team0'][i].get_number_entities_in_range(
                self.state['ennemyvisibleteam0'])

        return observation


if __name__ == '__main__':
    game = Game('human', Constants.GHOST_NUMBER, Constants.BUSTER_NUMBER_PER_TEAM, Constants.GAME_ROUND_NUMBER)
    game.loop()
