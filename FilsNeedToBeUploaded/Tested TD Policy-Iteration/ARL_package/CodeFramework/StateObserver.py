__author__ = 'erik'

from abc import ABCMeta, abstractmethod


class StateObserver(object):
    """This is where you are told which state it is"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_current_state(self):
        """Method that extracts from somewhere which state it is.
        :return current_state
        """
        pass
