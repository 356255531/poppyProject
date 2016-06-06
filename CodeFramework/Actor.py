__author__ = 'erik'

from abc import ABCMeta, abstractmethod


class Actor(object):
    """Goes from virtual actions to real ones"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def perform_action(self, action):
        """Execute some code to actually do the abstract action 'action' """
        pass
