__author__ = 'Zhiwei Han'

from actor import actor
import numpy as np
import random
import operator

class SarsaZeroVrep(actor):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, actor, poppy, io, name, positionMatrix, errorAfterTrained, epsilonGreedy):
		actor.__init__(self, poppy, io, name, positionMatrix)
		self.errorAfterTrained = errorAfterTrained
		self.epsilonGreedy = epsilonGreedy
		self.positionMatrix
		self.allStates = self.getAllStates()  # Initialize the states
		self.allActions = self.getAllActions()

	def getAllStates(self):
		locations = actor.getAllLocations()

		allStates = []
		for i in locations:
			euclideanDis = np.sqrt(list(i)[0] ** 2 + list(i)[1] ** 2)
			allStates.append((i, euclideanDis))

	def getAllActions(self):
		allActions = {}
		for i in self.allStates:
			allActions.append(actor.getActions(i))
		return allActions


	def getSuccessor(self, currentState, action):
		diffX, diffY = action
		x, y = currentState
		newX, newY = x + diffX, y + diffY
		euclideanDis = np.sqrt(newX ** 2 + newY ** 2)
		return ((newX, newY), euclideanDis)

	def getReward(self, currentState, nextState):
		euclideanDisCur = list(currentState)[1]
		euclideanDisNext = list(nextState)[1]
		return euclideanDisCur - euclideanDisNext

	def initializeQFunc(self):
		for i in self.allStates:
			allActions = actor.getActions(i)
			self.qFunc[i] = {j:0 for j in allActions}

	def train(self):
		self.initializeQFunc()

		count = 0
		while count < 3 * len(self.allStates):
			ifTerminal = lambda x: return list(x)[0] == (0, 0)

			qFuncBefor = qFunc
			currentState = actor.getInitialState()
			while ifTerminal(currentState):
				currentState = actor.getInitialState()


			actions = actor.getActions(currentState)
			if random.random < self.epsilonGreedy:
				action = actions[random.randint(0, len(actions) + 1)]
			else:
				action = max(actions.iteritems(), key=operator.itemgetter(1))[0]

			while ifTerminal(currentState):
				nextState = actor.getSuccessor(currentState, action)
				rewardValue = self.getReward(currentState, nextState)

				nextActions = actor.getActions(nextState)
				if random.random < self.epsilonGreedy:
					nextAction = nextActions[random.randint(0, len(nextActions) + 1)]
				else:
					nextAction = max(nextActions.iteritems(), key=operator.itemgetter(1))[0]

				TDError = alpha * (rewardValue + gama * qFunc[(nextState, nextAction)] - qFunc[(currentState, action)])
				qFunc[(currentState, action)]  = qFunc[(currentState, action)] + TDError

				currentState = nextState
				action = nextAction


			if qError < self.errorAfterTrained:
				count += 1
			else:
				count = 0

	def derivePolicy(self):
		policy = {}
		for i in self.allStates:
			optimalAction = max(qFunc[i].iteritems(), key=operator.itemgetter(1))[0]
			policy[i] = optimalAction
		return policy

	def getPolicy(self):
		self.train()
		policy = self.derivePolicy()
		return policy