__author__ = 'Zhiwei Han'

from actor import actor
import numpy as np
import random as rd
import operator

class SarsaZeroVrep(actor):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, actor, poppy, io, name, positionMatrix, errorAfterTrained, epsilonGreedy):

		actor.__init__(self, poppy, io, name, positionMatrix)

		self.positionMatrix = positionMatrix
		self.errorAfterTrained = errorAfterTrained
		self.epsilonGreedy = epsilonGreedy

		self.allStates = self.getAllStates()  		# Initialize the state list
		self.allActions = self.getAllActions()		# Initialize the action list
		self.qFunc = self.initializeQFunc()			# Initialize the Q function

	def getInitialState(self):
		actor.randMove()
		x, y = actor.getPosition()
		euclideanDis = np.sqrt(x ** 2 + y ** 2)
		return ((x, y), euclideanDis)

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
		qFunc = {}
		for i in self.allStates:
			qFunc[i] = {j:0 for j in self.allActions[i]}
		return qFunc

	def train(self):
		self.qFunc = self.initializeQFunc()

		count = 0
		while count < 3 * len(self.allStates):
			ifTerminal = lambda x: return list(x)[0] == (0, 0)

			qFuncBefor = self.qFunc
			currentState = self.getInitialState()

			while ifTerminal(currentState):
				currentState = self.getInitialState()

			actions = self.allActions(currentState)
			if rd.random < self.epsilonGreedy:
				action = actions[rd.randint(0, len(actions) + 1)]
			else:
				action = max(self.qFunc[currentState].iteritems(), key=operator.itemgetter(1))[0]

			while not ifTerminal(currentState):
				actor.takeAction(currentState, action)
				nextState = actor.getSuccessor(currentState, action)
				rewardValue = self.getReward(currentState, nextState)

				nextActions = self.allActions(nextState)
				if rd.random < self.epsilonGreedy:
					nextAction = nextActions[rd.randint(0, len(nextActions) + 1)]
				else:
					nextAction = max(self.qFunc[nextState].iteritems(), key=operator.itemgetter(1))[0]

				TDError = alpha * (rewardValue + gama * qFunc[nextState][nextAction] - qFunc[currentState][action])
				qFunc[currentState][action]  = qFunc[currentState][action] + TDError

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