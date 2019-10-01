import random
import numpy as np
import gym

from gym import spaces
from gym.utils import seeding
from gym.envs.classic_control import rendering

from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.ai_behaviour import Aibehaviour
from gym_buster.envs.game_classes.math_utils import MathUtility


class BusterEnv(gym.Env):
    """
    Class that will handle a codebuster environment
    """
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'videos.frames_per_second': 30
    }

    def __init__(self):
        """
        Initialize the environment
        """
        print("Initializing environment ...")
        self.ghosts = []
        self.buster_team0 = []
        self.buster_team1 = []
        self.ghost_number = 15
        self.buster_number = 3
        self.max_steps = 250
        self.current_step = 0

        # Rendering objects
        self.render_entities = []
        self.viewer = rendering.Viewer(Constants.PYGAME_WINDOW_WIDTH, Constants.PYGAME_WINDOW_HEIGHT)

        # Game state
        self.score_team0 = 0
        self.score_team1 = 0
        self.observation = None
        self.previous_observation = None
        self.state = None
        self.game_over = False

        # Observation and action space
        self.observation_space = self._observation_space()
        self.action_space = self._action_space()

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        """
        Function to call to reset environment to a new game
        """
        print("Resetting environment...")
        self.ghosts = []
        Ghost.reset_ghost()
        self.buster_team0 = []
        self.buster_team1 = []
        self.current_step = 0

        self.score_team0 = 0
        self.score_team1 = 0

        self.game_over = False

        # Create busters both team
        for i in range(self.buster_number):
            self.buster_team0.append(Buster(Constants.TYPE_BUSTER_TEAM_0, i))
            self.buster_team1.append(Buster(Constants.TYPE_BUSTER_TEAM_1, i))

        # Create ghosts
        for i in range(self.ghost_number):
            self.ghosts.append(Ghost(i))

        # Init rendering images for each entity
        self._init_rendering_entities()

        self.state = self._get_state()
        self.previous_observation = self._make_observation()
        self.observation = self.previous_observation

        return self.observation

    def step(self, action):
        """
        Function to call to move forward one step in the environment
        """
        self.current_step += 1
        print("--------- STEP {} -----------".format(self.current_step))
        print("Action : {}".format(action))

        # Convert commands given by NN or sampling on action space
        commands = self._transform_action(action)
        self._run_step(commands, None)

        # Check if the game is over
        if len(self.ghosts) == 0:
            self.game_over = True

        print("Score team 0 : {}".format(self.score_team0))
        print("Score team 1 : {}".format(self.score_team1))

        # Check alive and captured ghosts
        captured = 0
        alive = 0
        for ghost in self.ghosts:
            if ghost.captured:
                captured += 1
            if ghost.alive:
                alive += 1

        print("Captured : {}".format(captured))
        print("Alive : {}".format(alive))

        self.previous_observation = self.observation
        self.observation = self._make_observation()

        print("New observation : {}".format(self.observation))

        return self.observation, self._compute_reward(), self._check_done() or alive == 0, {}

    def _run_step(self, commands_0, commands_1):
        """
        Function called by step(...) with both commands for each team
        If commands_1 is null then it will use a simple AI (class Aibehaviour)
        """
        if commands_1:
            commands_team_1 = commands_1
        else:
            commands_team_1 = Aibehaviour.next_command(self.buster_team1, self.ghosts)
        commands_team_0 = commands_0

        # Apply action for each buster and save new state in a variable to resolve everything at the end
        for i in range(self.buster_number):
            buster_team0 = self.buster_team0[i]
            buster_team1 = self.buster_team1[i]

            command_0 = commands_team_0[i]
            command_1 = commands_team_1[i]

            self.score_team0 += buster_team0.buster_command(command_0)
            self.score_team1 += buster_team1.buster_command(command_1)

        # Resolve states conflicting Buster that bust same ghost
        for ghost in self.ghosts:
            if ghost.value != Constants.VALUE_GHOST_BASIC and ghost.alive:
                # Retrieve all busters that tried to bust this ghost
                buster_team_0_busting_this_ghost = []
                buster_team_1_busting_this_ghost = []
                for buster in self.buster_team0:
                    if buster.value == ghost.id:
                        buster_team_0_busting_this_ghost.append(buster)
                for buster in self.buster_team1:
                    if buster.value == ghost.id:
                        buster_team_1_busting_this_ghost.append(buster)

                # Check number of each team ghost
                # 1. If same number of buster for each team are busting a ghost then the busing is cancelled for the ghost
                # and the busters
                # 2. If different number of buster busting the ghost. The team with most buster win the ghost and it is
                # captured by the buster of the wnning team the closest. Only the buster with the captured ghost is in a
                # state carrying with the ghost id as value. The ghost take the position of the buster
                if len(buster_team_0_busting_this_ghost) == len(buster_team_1_busting_this_ghost) and len(
                        buster_team_1_busting_this_ghost) > 0:
                    ghost.busting_cancelled()
                    for buster in buster_team_0_busting_this_ghost + buster_team_1_busting_this_ghost:
                        buster.cancelling_bust()
                elif len(buster_team_0_busting_this_ghost) != len(buster_team_1_busting_this_ghost):
                    # Find closest buster in team with most buster
                    if len(buster_team_0_busting_this_ghost) > len(buster_team_1_busting_this_ghost):
                        closest = buster_team_0_busting_this_ghost[0]
                        winner_busters = buster_team_0_busting_this_ghost
                    else:
                        closest = buster_team_1_busting_this_ghost[0]
                        winner_busters = buster_team_1_busting_this_ghost

                    dist = MathUtility.distance(ghost.x, ghost.y, closest.x, closest.y)
                    for buster in winner_busters:
                        new_dist = MathUtility.distance(ghost.x, ghost.y, buster.x, buster.y)
                        if new_dist < dist:
                            dist = new_dist
                            closest = buster

                    # Reset all busters with this ghost id except closest
                    if closest and len(buster_team_0_busting_this_ghost) + len(buster_team_1_busting_this_ghost) >= 1:
                        if closest.action == Constants.ACTION_BUSTING:
                            ghost.being_captured(closest)
                            closest.capturing_ghost()
                            if closest.type == Constants.TYPE_BUSTER_TEAM_0:
                                self.score_team0 += 1
                            elif closest.type == Constants.TYPE_BUSTER_TEAM_1:
                                self.score_team1 += 1
                        else:
                            ghost.updating_position(closest)

                        for buster in buster_team_0_busting_this_ghost + buster_team_1_busting_this_ghost:
                            if buster != closest:
                                buster.cancelling_bust()

        # make ghost run away for those who are not being busted
        for ghost in self.ghosts:
            if not ghost.captured and ghost.alive:
                ghost.run_away(self.buster_team0 + self.buster_team1)

        # Compute score
        for ghost in self.ghosts:
            if ghost.is_in_team_0_base and not ghost.captured and ghost.alive:
                self.score_team0 += 1
                ghost.kill()
            elif ghost.is_in_team_1_base and not ghost.captured and ghost.alive:
                self.score_team1 += 1
                ghost.kill()

    def _init_rendering_entities(self):
        """
        Function to be called to init rendering entities and initialize the viewer
        """
        if self.viewer is None:
            self.viewer = rendering.Viewer(Constants.PYGAME_WINDOW_WIDTH, Constants.PYGAME_WINDOW_HEIGHT)

        for ghost in self.ghosts:
            g = rendering.make_circle(Constants.PYGAME_GHOST_RADIUS)
            g.set_color(0, 0, 255)
            g_trans = rendering.Transform()
            g.add_attr(g_trans)
            ghost.render_img = g
            ghost.render_trans = g_trans
            self.viewer.add_geom(g)

        for buster in self.buster_team0:
            b = rendering.make_circle(Constants.PYGAME_BUSTER_RADIUS)
            b.set_color(255, 0, 0)
            b_trans = rendering.Transform()
            b.add_attr(b_trans)
            buster.render_img = b
            buster.render_trans = b_trans
            self.viewer.add_geom(b)

        for buster in self.buster_team1:
            b = rendering.make_circle(Constants.PYGAME_BUSTER_RADIUS)
            b.set_color(0, 255, 0)
            b_trans = rendering.Transform()
            b.add_attr(b_trans)
            buster.render_img = b
            buster.render_trans = b_trans
            self.viewer.add_geom(b)

    def render(self, mode='human'):
        """
        Function to call to render the state of the game
        """
        screen_width = Constants.PYGAME_WINDOW_WIDTH
        screen_height = Constants.PYGAME_WINDOW_HEIGHT

        scale_x = screen_width / Constants.MAP_WIDTH
        scale_y = screen_height / Constants.MAP_HEIGHT

        for ghost in self.ghosts:
            if not ghost.captured and ghost.alive:
                ghost.render_img.set_color(0, 0, 255)
                ghost.render_trans.set_translation(ghost.x * scale_x, ghost.y * scale_y)
            else:
                ghost.render_img.set_color(255, 255, 255)

        for entity in self.buster_team0 + self.buster_team1:
            if entity.state == Constants.STATE_BUSTER_CARRYING:
                entity.render_img.set_color(255, 255, 0)
            else:
                if entity.type == Constants.TYPE_BUSTER_TEAM_0:
                    entity.render_img.set_color(255, 0, 0)
                elif entity.type == Constants.TYPE_BUSTER_TEAM_1:
                    entity.render_img.set_color(0, 255, 0)
            entity.render_trans.set_translation(entity.x * scale_x, entity.y * scale_y)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        """
        Function to call to end the episode before resetting the environment
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def _action_space(self):
        """
        Action space for gym env

        For each buster : move_X, move_Y, or bust or release

        :return: the space
        """
        action_low = []
        action_high = []
        for i in range(self.buster_number):
            action_low += [0.0, 0.0, 0.0, 0.0]
            action_high += [float(Constants.MAP_WIDTH), float(Constants.MAP_HEIGHT), 1.0, 1.0]

        return spaces.Box(np.array(action_low), np.array(action_high))

    def _observation_space(self):
        """
        observation space for gym env

        team0 points, team 1 points
        
        for each buster : state(carrying or not), ghost_inrange1_X, ghost_inrange1_Y, ghost_inrange2_X, ghost_inrange2_Y,
        ghost_inrange3_X, ghost_inrange3_Y

        For now we don't need to know anything from enemies

        :return: the space
        """
        obs_low = [0.0, 0.0]
        obs_high = [self.ghost_number, self.ghost_number]
        for i in range(self.buster_number):
            obs_low += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            obs_high += [1.0, Constants.MAP_MAX_DISTANCE, Constants.MAP_MAX_DISTANCE, Constants.MAP_MAX_DISTANCE, Constants.MAP_MAX_DISTANCE,
                         Constants.MAP_MAX_DISTANCE, Constants.MAP_MAX_DISTANCE]

        return spaces.Box(np.array(obs_low), np.array(obs_high))

    def _compute_reward(self):
        """
        Function that will compute reward for movement decided by the AI
        :return: the reward
        """
        # For now easy things

        # Battle over and won
        if self.score_team0 > self.score_team1:
            return 4000
        # Battle over and lost
        if self.game_over and self.score_team1 > self.score_team0:
            return -4000
        # point + 1
        if self.observation[0] > self.previous_observation[0]:
            return 200
        # point - 1
        if self.observation[0] < self.previous_observation[0]:
            return -200

        return 0

    def _get_state(self):
        """
        Function that will return the state of the game
        :return: a dictionnary with the game state
        """
        state = {}

        state['scoreteam0'] = self.score_team0
        state['scoreteam1'] = self.score_team1
        state['game_over'] = self.game_over
        state['ghosts'] = self.ghosts
        state['team0'] = self.buster_team0
        state['team1'] = self.buster_team1

        state['ghostvisibleteam0'] = Entity.get_entities_visible(self.buster_team0, self.ghosts)
        state['ghostvisibleteam1'] = Entity.get_entities_visible(self.buster_team1, self.ghosts)
        state['ennemyvisibleteam0'] = Entity.get_entities_visible(self.buster_team0, self.buster_team1)
        state['ennemyvisibleteam1'] = Entity.get_entities_visible(self.buster_team1, self.buster_team0)

        return state

    def _make_observation(self):
        """
        Compute the observation from the new state
        :return: an array with observations
        """
        print("Making observation")
        observation = np.zeros(self.observation_space.shape)
        observation[0] = self.state['scoreteam0']
        observation[1] = self.state['scoreteam1']
        for i in range(self.buster_number):
            # state (carrying or not)
            observation[i * 6 + 2] = self.state['team0'][i].state
            # coordinates of closest ghost visible
            ghost0, dist0 = self.state['team0'][i].get_closest(self.state['ghostvisibleteam0'], 0)
            ghost1, dist1 = self.state['team0'][i].get_closest(self.state['ghostvisibleteam0'], 1)
            ghost2, dist2 = self.state['team0'][i].get_closest(self.state['ghostvisibleteam0'], 2)
            
            observation[i * 6 + 3] = ghost0.x if ghost0 else Constants.MAP_MAX_DISTANCE
            observation[i * 6 + 4] = ghost0.y if ghost0 else Constants.MAP_MAX_DISTANCE
            observation[i * 6 + 5] = ghost1.x if ghost1 else Constants.MAP_MAX_DISTANCE
            observation[i * 6 + 6] = ghost1.y if ghost1 else Constants.MAP_MAX_DISTANCE
            observation[i * 6 + 7] = ghost2.x if ghost2 else Constants.MAP_MAX_DISTANCE
            observation[i * 6 + 8] = ghost2.y if ghost2 else Constants.MAP_MAX_DISTANCE
            
        return observation

    def _check_done(self):
        """
        Function that will say if a game is over
        :return: boolean
        """
        return self.game_over or self.current_step > self.max_steps

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
                ghost, dist = self.state['team0'][i].get_closest(self.state['ghostvisibleteam0'], 0) #TODO adapt position
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

