__author__ = 'erik'

from .. import CodeFramework.StateObserver


class MathematicalObserver(CodeFramework.StateObserver):
    """docstring"""

    def __init__(self, state_action_space):
        assert isinstance(state_action_space, CodeFramework.GridStateActionSpace2D)

        self.state_action_space = state_action_space
        self.current_state = (0, 0)

    def get_current_state(self):
        """
        docstring
        :return: current_state
        """
        return self.current_state