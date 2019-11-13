import argparse

import gym_buster.envs.buster_env as env


class RandomAgent(object):
    """
    Class that will handle an agent that do random actions each step
    """
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self):
        return self.action_space.sample()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_steps', help="Number of maximum steps for each game", required=True)
    parser.add_argument('--max_episodes', help="Number of maximum games to play", required=True)
    parser.add_argument('--ghost_number', help="Number of ghosts for each game", required=True)
    parser.add_argument('--buster_number', help="Number of buster in each team", required=True)
    args = parser.parse_args()

    environment = env.BusterEnv(args.buster_number, args.ghost_number, args.max_episodes, args.max_steps, True)
    environment.seed(123)
    agent = RandomAgent(environment.action_space)

    episodes = 0

    while episodes < int(args.max_episodes):
        obs = environment.reset()
        print("Observable shape" + str(obs.shape))
        done = False
        step = 0
        while not done and step < int(args.max_steps):
            action = agent.act()
            print("Action shape" + str(action.shape))
            obs, reward, done, info = environment.step(action)
            step += 1
        episodes += 1

    environment.close()