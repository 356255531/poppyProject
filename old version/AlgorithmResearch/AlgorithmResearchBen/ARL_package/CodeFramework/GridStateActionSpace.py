__author__ = 'erik'
from . import StateActionSpace


class GridStateActionSpace2D(StateActionSpace):
    """Grid-based state-action space

    Grid based state-action space. Each state and action is a tuple of two
    integers. Constructed with the dimensions of the thing."""

    def __init__(self, dimensions = (3,1), allow_diag_actions = True):
        """Initialise state space with dimensions.

        :rtype : GridStateActionSpace2D
        :param dimensions: Tuple of size in each direction.
        :param allow_diag_actions: Whether to allow diagonal actions or not
        :return:
        """

        import numpy as np

        half_dimensions = (np.array(dimensions)/2).astype(int)

        self.min_indices = -half_dimensions
        self.max_indices = self.min_indices + dimensions - (1, 1)

        """All States"""
        self.states = [(i-half_dimensions[0], j-half_dimensions[1]) for i, j in np.ndindex(dimensions)]

        def __generate_possible_actions(dims, state_index, allow_diag=True):
            if state_index == (0, 0):
                return [(0, 0)]  # is terminal state => can only stay there!

            min_indices = -(np.array(dims)/2).astype(int)
            max_indices = (min_indices + dims) - (1, 1)

            # disallow going out of edges
            min_action = -(np.less(min_indices, state_index)).astype(int)
            max_action = np.less(state_index, max_indices).astype(int)

            # have same actions everywhere
            # min_action = -(np.less(min_indices, (0, 0))).astype(int)
            # max_action = np.less((0, 0), max_indices).astype(int)

            actions = []
            for i in range(min_action[0], max_action[0] + 1):
                for j in range(min_action[1], max_action[1] + 1):
                    if (i*j == 0 or allow_diag) and (i, j) != (0, 0):
                        actions.append((i, j))
            return actions

        self.eligible_actions = dict()

        for state in self.states:
            self.eligible_actions[state] = __generate_possible_actions(
                dimensions, state_index=state, allow_diag=allow_diag_actions)

        self.actions = self.eligible_actions[(1, 0)]  # kind of all eligible actions unless your space is only 2 wide

    def get_list_of_states(self):
        """Returns a list of all states available"""
        return self.states

    def get_list_of_actions(self):
        """Returns a list of all actions available"""
        return self.actions

    def get_eligible_actions(self, state):
        """Returns eligible actions for state state"""
        assert isinstance(state, tuple)
        return self.eligible_actions[state]

    def is_terminal_state(self, state):
        """returns if the current state is terminal

        Current implementation: (0,0) is terminal

        :param state: state inquired about
        :return: is_terminal: boolean
        """
        return state == (0, 0)