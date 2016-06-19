__author__ = 'Zhiwei Han'

from Modules.CodeFramework.rewardAb import rewardAb
import numpy as np

class reward(rewardAb):
	""" The class gives the setting of reward """
	def __init__(self):
		super(reward, self).__init__()

	def getReward(self, currentState, action, nextState, problemType='capture'):
		"""This method give back the reward value according to given current
			state, action, next state and if it's a greeting or avoiding case(optional).
			By default is greeting. """
		if len(list(currentState)) == 0 and len(list(nextState)) == 0:
			return 0

		if problemType == 'capture':
			if len(list(currentState)) == 0:
				if len(list(nextState)) != 0:
					return 0
			if len(list(currentState)) != 0:
				if len(list(nextState)) == 0:
					return -100
			euclideanDis1 = list(currentState)[0] ** 2 + list(currentState)[1] ** 2
			euclideanDis2 = list(nextState)[0] ** 2 + list(nextState)[1] ** 2
			absReward = np.sqrt(euclideanDis1) - np.sqrt(euclideanDis2)
			if absReward > 0:
				return round(absReward, 3)
			else:
				return round(absReward, 3) - 1
		else:
			if len(list(currentState)) == 0:
				if len(list(nextState)) != 0:
					return -100
			if len(list(currentState)) != 0:
				if len(list(nextState)) == 0:
					return 100
			euclideanDis1 = list(currentState)[0] ** 2 + list(currentState)[1] ** 2
			euclideanDis2 = list(nextState)[0] ** 2 + list(nextState)[1] ** 2
			if absReward < 0:
				return -round(absReward, 3)
			else:
				return -round(absReward, 3) - 1
if __name__ == '__main__':
	a = reward()
	print a.getReward((1, 2), (1, 0), (1, 1), 'capture')
