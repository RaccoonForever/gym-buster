import numpy as np
import argparse

import gym_buster.envs.buster_env as env

# For plotting metrics
all_epochs = []
all_penalties = []

class QAgent(object):
  """
  Class that will handle a QAgent
  """
  def __init__(self, action_space, observation_space):
    self.alpha = 0.1
    self.gamma = 0.6
    self.epsilon = 0.1
    self.action_space = action_space
    self.observation_space = observation_space
    self.all_episodes = []
    self.all_penalties = []
    self.q_state = np.zeros([observation_space.n,action_space.n])

  def act_randomly(self):
     return self.action_space.sample()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--max_steps', help="Number of maximum steps for each game", required=True)
  parser.add_argument('--max_episodes', help="Number of maximum games to play", required=True)
  parser.add_argument('--ghost_number', help="Number of ghosts for each game", required=True)
  parser.add_argument('--buster_number', help="Number of buster in each team", required=True)
  parser.add_argument('--rendering', help="Pygame rendering or only console (true or false), required=True"
  args = parser.parse_args()
  
  environment = env.BusterEnv(args.buster_number, args.ghost_number, args.max_episodes, args.max_steps, args.rendering)
  environment.seed(123)
  
  agent = QAgent(environment.action_space, environment.observation_space)
  
  episodes = 0
  
  while episodes < environment.episodes:
    state = environment.reset()
    
    penalties, reward = 0, 0
    done = False
    
    while not done:
      if random.uniform(0, 1) < agent.epsilon:
        action = agent.act_randomly() # Explore values
      else:
        action = np.argmax(agent.q_state[state])
      
      next_state, reward, done, info = env.step(action)
      
      old_value = agent.q_table[state, action]
      next_max = np.max(agent.q_table[next_state])
      
      new_value = (1 - agent.alpha) * old_value + agent.alpha * (reward + agent.gamma * next_max)
      
      q_table[state, action] = new_value
      
      if reward < 0:
        penalties += 1
        
      state = next_state
    
    episodes += 1
    if episodes % 100 == 0:
      print("Episode {} DONE".format(episodes))
  
  print("Training done. Saving Q-Table...")
  
  agent.q_state.to_file('q_table.dat')
  
  print("Q-Table saved in q_table.dat")
  
  
      
  
  

