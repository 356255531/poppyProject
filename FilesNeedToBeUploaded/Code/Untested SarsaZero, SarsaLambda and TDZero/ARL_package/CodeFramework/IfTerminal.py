__author__ = 'Zhiwei Han'

from abc import ABCMeta, abstractmethod


class IfTerminal(object):
    """Goes from virtual actions to real ones"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def is_terminal(self, state):
        """Execute some code to actually do the abstract action 'action' """
    pass
