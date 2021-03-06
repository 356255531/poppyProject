__author__ = 'erik'
from abc import ABCMeta, abstractmethod


class StateActionSpace(object):
    """Manager for states and actions available"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_list_of_states(self):
        """Returns a list of all states available"""
        pass

    @abstractmethod
    def get_list_of_actions(self):
        """Returns a list of all actions available"""
        pass


    @abstractmethod
    def get_eligible_actions(self, state):
        """Returns eligible actions for state state"""
        pass

    def is_terminal_state(self, state):
        """
        returns if the current state is terminal
        :param state: state inquired about
        :return: is_terminal: boolean
        """
        return bool(state)


    def get_terminal_state(self):
        """
        Gets the representation of the terminal state

        :return: terminal state
        """
        return []