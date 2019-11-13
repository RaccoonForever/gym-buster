import unittest
import gym_buster.envs.buster_env as env


class EnvTest(unittest.TestCase):

    def test_run_1_game_random_action(self):
        """
        Run one game from the env from random sampled action
        """
        buster_number = 3  # per team
        ghost_number = 15
        max_episodes = 1
        max_steps = 250
        rendering = True

        environment = env.BusterEnv(buster_number, ghost_number, max_episodes, max_steps, rendering)
        environment.seed(130)

        episodes = 0
        while episodes < environment.episodes:
            state = environment.reset()
            self.assertTrue(environment.episode_step == 0)

            done = False
            steps = 0
            while not done:
                action = environment.action_space.sample()
                next_state, reward, done, _ = environment.step(action)
                steps += 1

            episodes += 1

            self.assertTrue(environment.game.score_team_0 + environment.game.score_team_1 <= ghost_number)

        self.assertTrue(episodes == 1)
        self.assertTrue(environment.episodes == 1)
        self.assertTrue(environment.max_episodes_steps == 250)

    def test_run_5_games_random_action(self):
        """
        Run 5 games from same environment with random sampled action
        """

        environment = env.BusterEnv()

        episodes = 0
        while episodes < 5:
            state = environment.reset()
            environment.render()
            self.assertTrue(environment.current_step == 0)

            total_reward = 0
            steps = 0
            done = False
            while not done:
                action = environment.action_space.sample()
                next_state, reward, done, _ = environment.step(action)
                total_reward += reward
                print("Reward : {}, Total Reward : {}".format(reward, total_reward))
                print("Game over : {}".format(done))
                environment.render()
                steps += 1

            episodes += 1
            environment.close()

            self.assertTrue(environment.score_team0 + environment.score_team1 <= environment.ghost_number)

        self.assertTrue(episodes == 5)
        self.assertTrue(environment.max_steps == 250)
