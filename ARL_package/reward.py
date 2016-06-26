__author__ = 'Zhiwei Han'

from Modules.CodeFramework.Reward import Reward
import numpy as np

class reward(Reward):
	""" The class gives the setting of reward """
	def __init__(self):
		super(reward, self).__init__()

	def get_rewards(self, currentState, action, nextState=None, problemType='capture'):
		"""This method give back the reward value according to given current
			state, action, next state and if it's a greeting or avoiding case(optional).
			By default is greeting. """
		if problemType == 'capture':
			if nextState == (0, 0):
				return 10
			if nextState == ():
				return -100
			return -1
if __name__ == '__main__':
	a = reward()
	print a.get_rewards((1, 2), (1, 0), (1, 1), 'capture')
