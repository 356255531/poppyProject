__author__ = 'Zhiwei Han'

from CodeFramework.Reward import Reward
from isTerminal import isTerminal
import numpy as np

class reward(Reward, isTerminal):
	""" The class gives the setting of reward """
	def __init__(self):
		super(reward, self).__init__()

	def get_rewards(self, currentState, action, nextState=None, problemType='capture'):
		"""This method give back the reward value according to given current
			state, action, next state and if it's a greeting or avoiding case(optional).
			By default is greeting. """
		if problemType == 'capture':
			if super(reward, self).is_terminal(nextState):
				return 10
			elif len(list(nextState)) == 0:
				return -100
			else:
				return -1
		# else:
if __name__ == '__main__':
	a = reward()
	print a.get_rewards((1, 2), (1, 0), (0, 0), 'capture')
