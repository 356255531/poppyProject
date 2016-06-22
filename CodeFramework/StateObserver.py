__author__ = 'erik'

from abc import ABCMeta, abstractmethod

class StateObserver(object):
    """This is where you are told which state it is"""

    @abstractmethod
    def get_current_state(self):
        """Method that extracts from somewhere which state it is.
        :return current_state
        """
        pass

    def is_terminal_state(self, state):
        """Check if current state is terminal"""
        return False