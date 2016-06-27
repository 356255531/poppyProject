__author__ = 'Zhiwei Han'

from CodeFramework.IfTerminal import IfTerminal


class isTerminal(IfTerminal):
    """Goes from virtual actions to real ones"""

    def is_terminal(self, state):
        """Execute some code to actually do the abstract action 'action' """
    	return state == (0, 0)
