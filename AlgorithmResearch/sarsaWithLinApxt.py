__author__ = 'Zhiwei Han'

import numpy as np
import random as rd
import operator
import itertools
from collections import deque

class sarsaWithLinApxt(object):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, problem, epsilonGreedy, numEpisoid, alpha, gamma, lambdaDiscount):
		self.epsilonGreedy = epsilonGreedy
		self.numEpisoid = numEpisoid
		self.alpha = alpha
		self.gamma = gamma
		self.lambdaDiscount = lambdaDiscount

		self.problem = problem

		self.stateSpace = self.problem.getStateSpace()  				# Initialize the state list
		self.actionSpace = self.problem.getActionSpace()				# Initialize the action list
		self.qFunc = self.initQFfunc()									# Initialize the Q function
		self.featureTransitionDict, self.apxtParas= self.featureTransition()		# Initialize the features used in gradient descent
		self.eligibility = self.initEligibility()						# Initialize the Eligibility

	def initQFfunc(self):
		""" Initialize the Q function 
			used in constructor """
		qFunc = {}
		for i in self.stateSpace:
			qFunc[i] = {j:0 for j in self.actionSpace[i]}
		return qFunc

	def initEligibility(self):
		return np.zeros(len(self.apxtParas))

	def featureTransition(self):
		""" Including feature set up and nomalization """
		featureSet = set()

		for state in self.stateSpace:
			for action in self.actionSpace[state]:
				i, j = state
				euclideanDist1 = np.sqrt(i ** 2 + j ** 2)
				x, y = action
				euclideanDist2 = np.sqrt((i + x) ** 2 + (j + y) ** 2)				
				featureSet.add((euclideanDist1, euclideanDist2))

		featureSet = list(featureSet)

		featureTransMatrix = {}
		for state in self.stateSpace:
			featureTransMatrix[state] = {}
			for action in self.actionSpace[state]:
				x, y = state 
				i, j = action
				euclideanDist1 = np.sqrt(x ** 2 + y ** 2)
				euclideanDist2 = np.sqrt((i + x) ** 2 + (j + y) ** 2)	
				element = (euclideanDist1, euclideanDist2)
				featureTransMatrix[state][action] = featureSet.index(element)

		for state in self.stateSpace:
			for action in self.actionSpace[state]:
				emptyArray = np.zeros(len(featureSet))
				emptyArray[featureTransMatrix[state][action]] = 1
				featureTransMatrix[state][action] = emptyArray

		paras = [round(rd.random(), 3) for i in xrange(len(featureSet))]
		return featureTransMatrix, np.array(paras)

	def epsilonGreedySelection(self, currentState):
		""" Pick the action from action space with given state by 
			using epsilon greedy method """
		if rd.random() > self.epsilonGreedy:
			actions = list(self.actionSpace[currentState])
			action = actions[rd.randint(0, len(actions) - 1)]
			return action
		else:
			actions = self.qFunc[currentState]
			action = max(actions.iteritems(), key=operator.itemgetter(1))[0]
			return action

	def updateQFunc(self, currentState, action, reward, nextState, nextAction):
		""" Update the Q function with given current state and 
				next state by weighted TD error """
		if len(list(nextState)) != 0:
			tdError = reward + self.gamma * self.qFunc[nextState][nextAction] - self.qFunc[currentState][action]
		else:
			tdError = reward + self.gamma * -100 - self.qFunc[currentState][action]
		self.eligibility[currentState][action] += 1
		for i in self.stateSpace:
			for j in self.actionSpace:
				self.qFunc[currentState][action] += self.alpha * self.delta * self.eligibility[currentState][action]
				self.eligibility[currentState][action] = self.gamma * self.lambdaDiscount * self.eligibility[currentState][action]
		self.qFunc[currentState][action] = round(self.qFunc[currentState][action] + self.alpha * tdError, 3)

	def trainEpisoid(self):
		""" Train the model with only one episoid and 
			use the predefined function update the Q
			function in every step """
		ifTerminal = lambda x: list(x)[0] == list(x)[1] == 0

		visitedStates = []

		currentState = self.problem.getInitialState()
		visitedStates.append(currentState)

		self.initEligibility()

		step = 0
		totalReward = 0

		actions = self.actionSpace[currentState]
		action = actions[rd.randint(0, len(actions) - 1)]
		FA = self.featureTransMatrix[currentState][action]
		while len(list(currentState)) != 0 and not ifTerminal(currentState):  	# Check if the algorithm has reached the terminal
			i = list(FA == 1)
			i = i.index(True)
			self.eligibility[i] = 1		# Replacing traces

			self.problem.takeAction(currentState, action)						# or the object is already out of sight 
			nextState = self.problem.getCurrentState()
			visitedStates.append(nextState)
			reward = self.problem.getReward(currentState, action, nextState)
			totalReward += reward

			tdError = reward - FA * self.paras
			currentState = nextState

			if not ifTerminal(currentState):
				if rd.random() < (1 - self.epsilonGreedy):
					for i in self.actionSpace[currentState]:
						Fa = 
			self.apxtParas += self.alpha * tdError * self.eligibility
			
			self.eligibility *= self.gamma * self.lambdaDiscount

			step += 1
		print visitedStates
		print 'The episoid has been done in ', step, 'step'
		return step, totalReward, visitedStates

	def trainModel(self):
		for i in xrange(self.numEpisoid):
			print 'Trace', i + 1, ':'
			self.trainEpisoid()
			print 'Q Function'
			for j in self.qFunc:
				print j, ':', self.qFunc[j]
			self.epsilonGreedy = 1 - (1 - self.epsilonGreedy) * 0.99

	def derivePolicy(self):
		policy = {}
		for i in self.stateSpace:
			optimalAction = max(self.qFunc[i].iteritems(), key=operator.itemgetter(1))[0]
			policy[i] = optimalAction
		return policy

	def getPolicy(self):
		return  self.derivePolicy()
