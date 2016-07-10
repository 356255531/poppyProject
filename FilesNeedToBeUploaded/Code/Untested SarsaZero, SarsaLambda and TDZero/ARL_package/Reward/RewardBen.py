__author__ = 'Ben'

from ..CodeFramework import Reward
from ..StateActionSetting import StateActionSpaceFull
import numpy as np

class RewardBen(Reward):
	""" The class gives the setting of Reward """
	def __init__(self, stateActionSpace):
		super(RewardBen, self).__init__()
		self.stateActionSpace = stateActionSpace

	def get_rewards(self, currentState, action, nextState=None, problemType='capture'):
		"""This method give back the RewardBen value according to given current
			state, action, next state and if it's a greeting or avoiding case(optional).
			By default is greeting. """
		if problemType == 'capture':
			ifTerminal = self.stateActionSpace.is_terminal_state(nextState)
			if not ifTerminal:
				return 0
			elif ifTerminal == 1:
				return 10
			else:
				return -10
if __name__ == '__main__':
	a = RewardBen()
	print a.get_rewards((1, 2), (1, 0), (1, 1), 'capture')
