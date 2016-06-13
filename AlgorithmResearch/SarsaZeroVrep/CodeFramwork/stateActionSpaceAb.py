__author__ = 'erik'
from abc import ABCMeta, abstractmethod


class stateActionSpaceAb(object):
    """Manager for states and actions available"""

    __metaclass__ = ABCMeta
            
    @abstractmethod
    def getStateSpace(self):
        """Returns a list of all states available"""
        pass

    @abstractmethod
    def getActionSpace(self):
        """Returns a list of all actions available"""
        pass


    @abstractmethod
    def getEligibleAction(self, state):
        """Returns eligible actions for state state"""
        pass

if __name__ == '__main__':
    import numpy as np
    m, n =2, 2
    list1 = np.linspace(- m // 2, m // 2 + 1)
    print list1
