# gym-buster (an OpenAI environment)

I tried to play a coding game few months ago : https://www.codingame.com/multiplayer/bot-programming/codebusters. The goal of this simulation is to catch more ghosts than the ennemy team using a better strategy algorithm.
It came to me that I wanted to see if we can use some Reinforcement Learning to beat game.
To do so, I recreated a game with same abilities, size and more.

Feel free to use it and try to beat the ennemy team !


# Versions
## V0.0.2
New version using gym.rendering for graphics. Lighter and faster than Pygame.
Adding position for ghost and ennemies in observation space.
Some refactoring. Code lighter and cleaner.
Some documentation.

## V0.0.1
This first version was using Pygame to implement graphic effects.
Trouble on my own computer to run more than 3 episodes: wrong allocation memory
The game was working well for one episode but it was not enough for RL.
Code architecture was not optimized and too complicated for what I wanted.
