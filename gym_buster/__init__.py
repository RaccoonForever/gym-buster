import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Buster-v0',
    entry_point='gym_buster.envs:BusterEnv'
)
