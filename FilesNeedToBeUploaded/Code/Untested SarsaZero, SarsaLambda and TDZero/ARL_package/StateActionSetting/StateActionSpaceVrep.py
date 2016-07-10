__author__ = 'Zhiwei Han'
from ..CodeFramework import StateActionSpace
from itertools import product
from math import floor

class StateActionSpaceVrep(StateActionSpace):
    """Grid-based state-action space

    Grid based state-action space. Each state and action is a tuple of two
    integers. Constructed with the dimensions of the thing."""

    def __init__(self, dimensions = (3,1)):
        """Initialise state space with dimensions.

        :rtype : StateActionSpaceVrep
        :param dimensions: Tuple of size in each direction.
        :param allow_diag_actions: Whether to allow diagonal actions or not
        :return:
        """
        self.dimensions = dimensions
        self.states = self.__init_states()
        self.actions = self.__init_actions()

    def __init_actions(self):
        actionOneDim = [-1, 0, 1]
        actions = [(i, j) for i, j in product(actionOneDim, repeat=2)]
        actions.remove((0, 0))
        return actions

    def __init_states(self):
        m, n = self.dimensions
        indices_x = int(floor(m / 2))
        indices_y = int(floor(n / 2))
        stateOneDimX = range(-indices_x, indices_x + 1)
        stateOneDimY = range(-indices_y, indices_y + 1)
        states = [(i, j) for i, j in product(stateOneDimX, stateOneDimY)]
        return states

    def get_list_of_states(self):
        """Returns a list of all states available"""
        return self.states

    def get_list_of_actions(self):
        """Returns a list of all actions available"""
        return self.actions

    def get_eligible_actions(self, state):
        return self.actions

    def is_terminal_state(self, state):
        if state == ():
            return -1
        if state == (0, 0):
            return 1
        return False

if __name__ == '__main__':
    stateActionSpace = StateActionSpaceVrep((3, 2))
    print stateActionSpace.get_list_of_states()