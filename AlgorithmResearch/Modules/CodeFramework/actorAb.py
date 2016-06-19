__author__ = 'erik'

from abc import ABCMeta, abstractmethod


class actorAb(object):
    """Goes from virtual actions to real ones"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def takeAction(self, action):
        """Execute some code to actually do the abstract action 'action' """
        pass