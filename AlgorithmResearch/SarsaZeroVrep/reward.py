__author__ = 'Zhiwei Han'

from CodeFramwork.rewardAb import rewardAb
import numpy as np

class reward(rewardAb):
	"""docstring for reward"""
	def __init__(self):
		super(reward, self).__init__()

	def getReward(self, currentState, action, nextState, problemType='capture'):
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
				return absReward
			else:
				return 2 * absReward
		else:
			if len(list(currentState)) == 0:
				if len(list(nextState)) != 0:
					return -100
			if len(list(currentState)) != 0:
				if len(list(nextState)) == 0:
					return 100
			euclideanDis1 = list(currentState)[0] ** 2 + list(currentState)[1] ** 2
			euclideanDis2 = list(nextState)[0] ** 2 + list(nextState)[1] ** 2
			return np.sqrt(euclideanDis2) - np.sqrt(euclideanDis1)

if __name__ == '__main__':
	a = reward()
	print a.getReward((1, 2), (1, 0), (1, 1), 'capture')
