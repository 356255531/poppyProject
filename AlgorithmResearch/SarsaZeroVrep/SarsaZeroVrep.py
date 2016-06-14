__author__ = 'Zhiwei Han'

from problem import problem
import numpy as np
import random as rd
import operator

class SarsaZeroVrep(object):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, problem, epsilonGreedy, numEpisoid, alpha, gamma):
		self.epsilonGreedy = epsilonGreedy
		self.numEpisoid = numEpisoid
		self.alpha = alpha
		self.gamma = gamma

		self.problem = problem

		self.stateSpace = self.problem.getStateSpace()  		# Initialize the state list
		self.actionSpace = self.problem.getActionSpace()		# Initialize the action list
		self.qFunc = self.initializeQFunc()			# Initialize the Q function

	def initializeQFunc(self):
		qFunc = {}
		for i in self.stateSpace:
			qFunc[i] = {j:0 for j in self.actionSpace[i]}
		return qFunc

	def epsilonGreedySelection(self, currentState):
		if rd.random() > self.epsilonGreedy:
			actions = list(self.actionSpace[currentState])
			action = actions[rd.randint(0, len(actions) - 1)]
			return action
		else:
			actions = self.qFunc[currentState]
			action = max(actions.iteritems(), key=operator.itemgetter(1))[0]
			return action

	def updateQFunc(self, currentState, action, reward, nextState, nextAction):
		if len(list(nextState)) != 0:
			tdError = reward + self.gamma * self.qFunc[nextState][nextAction] - self.qFunc[currentState][action]
			self.qFunc[currentState][action] = self.qFunc[currentState][action] + self.alpha * tdError
		else:
			tdError = reward + self.gamma * -100 - self.qFunc[currentState][action]
			self.qFunc[currentState][action] = self.qFunc[currentState][action] + self.alpha * tdError

	def trainEpisoid(self):
		ifTerminal = lambda x: list(x)[0] == list(x)[1] == 0

		visitedStates = []
		currentState = self.problem.getInitialState()
		print 'Initial state get'
		visitedStates.append(currentState)
		step = 0
		totalReward = 0

		action = self.epsilonGreedySelection(currentState)
		while len(list(currentState)) != 0 and not ifTerminal(currentState):
			self.problem.takeAction(currentState, action)
			nextState = self.problem.getCurrentState()
			visitedStates.append(nextState)
			reward = self.problem.getReward(currentState, action, nextState)
			totalReward += reward

			if len(list(nextState)) == 0:
				nextAction = ()
			else:
				nextAction = self.epsilonGreedySelection(nextState)

			self.updateQFunc(currentState, action, reward, nextState, nextAction)

			currentState = nextState
			visitedStates.append(currentState)
			action = nextAction

			step += 1
		print visitedStates
		print 'step', step
		return step, totalReward, visitedStates

	def trainModel(self):
		for i in xrange(self.numEpisoid):
			print 'Trace', i + 1, ':'
			self.trainEpisoid()
			for j in self.qFunc:
				print j, ':', self.qFunc[j]
			self.epsilonGreedy *= 0.99



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