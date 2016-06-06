__author__ = 'erik'

from abc import ABCMeta, abstractmethod

class LearningAlgorithm(object):
    """Implementation class of the Learning Algorithm"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_next_action(self, current_state):
        """Find out which is the next action given the state 'current_state'
                :return next_action : next action according to policy
                        """
        pass

    @abstractmethod
    def receive_reward(self, old_state, action, next_state, reward):
        """Perform things according to which reward was given"""
        pass