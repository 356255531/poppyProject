__author__ = 'erik'

from abc import ABCMeta, abstractmethod


class Reward(object):
    """Implementation of the rewards"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_reward(self, state, action, next_state, next_action=None):
        """Return the reward for the prev/next action/state combination"""
        pass
