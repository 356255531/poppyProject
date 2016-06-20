__author__ = 'Zhiwei Han'

from CodeFramework.StateActionSpace import StateActionSpace
import numpy as np
import itertools

class stateActionSpace(StateActionSpace):
	""" This class return the action and state space """
	def __init__(self, positionMatrix):
		super(stateActionSpace, self).__init__()
		self.positionMatrix = positionMatrix
		self.stateSpace, self.actionSpace = self.initSpace()

	def initSpace(self):
		""" Initialize the state space and action space 
			used in constuctor """
		m, n = list(self.positionMatrix)[0], list(self.positionMatrix)[1]
		list1 = np.arange(-m , m + 1)
		list2 = np.arange(-n , n + 1)
		stateSpace = []
		for i, j in itertools.product(list1, list2):
			stateSpace.append((i, j))

		validActions = []
		list1 = [-1, 0, 1]
		for i, j in itertools.product(list1, list1):
			if i == j == 0:
				continue
			validActions.append((i, j))
		actionSpace = {}
		for i in stateSpace:
			acceptActions = []
			for j in validActions:
				xDiff, yDiff = j
				x, y = i
				x, y = x + xDiff, y + yDiff
				if abs(x) <= m and abs(y) <= n:
					acceptActions.append(j)
			actionSpace[i] = acceptActions

		return stateSpace, actionSpace

	def get_list_of_states(self):
		"""Returns a list of all states available"""
		return self.stateSpace

	def get_list_of_actions(self):
		"""Returns a list of all actions available"""
		return self.actionSpace

	def get_eligible_actions(self, state):
		""" Not implemented """
		pass

if __name__ == '__main__':
	a = stateActionSpace((25, 20))
	print a.get_list_of_actions()