__author__ = 'Zhiwei Han'

from problem import problem
import numpy as np
import random as rd
import operator

class SarsaZeroVrep(object):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, problem, errorAfterTrained, epsilonGreedy):
		self.errorAfterTrained = errorAfterTrained
		self.epsilonGreedy = epsilonGreedy

		self.problem = problem

		self.stateSpace = self.problem.getStateSpace()  		# Initialize the state list
		self.actionSpace = self.problem.getActionSpace()		# Initialize the action list
		self.qFunc = self.initializeQFunc()			# Initialize the Q function

	def initializeQFunc(self):
		qFunc = {}
		for i in self.stateSpace:
			qFunc[i] = {j:0 for j in self.actionSpace[i]}
		return qFunc

	def train(self):
		self.qFunc = self.initializeQFunc()

		count = 0
		while count < 3 * len(self.problem.getStateSpace):
			ifTerminal = lambda x: list(x)[0] == (0, 0)

			qFuncBefor = self.qFunc
			currentState = self.problem.getInitialState()

			while ifTerminal(currentState):
				currentState = self.problem.getInitialState()

			actions = self.problem.getActionSpace(currentState)
			if rd.random < self.epsilonGreedy:
				action = actions[rd.randint(0, len(actions) + 1)]
			else:
				action = max(self.qFunc[currentState].iteritems(), key=operator.itemgetter(1))[0]

			while not ifTerminal(currentState):
				self.problem.takeAction(currentState, action)
				nextState = self.problem.getSuccessor(currentState, action)
				reward = self.problem.getReward(currentState, nextState, nextState)

				nextActions = self.problem.getActionSpace(nextState)
				if rd.random < self.epsilonGreedy:
					nextAction = nextActions[rd.randint(0, len(nextActions) + 1)]
				else:
					nextAction = max(self.qFunc[nextState].iteritems(), key=operator.itemgetter(1))[0]

				TDError = alpha * (reward + gama * qFunc[nextState][nextAction] - qFunc[currentState][action])
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