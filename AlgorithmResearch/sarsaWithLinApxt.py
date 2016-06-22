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

		self.stateSpace = self.problem.get_list_of_states()  				# Initialize the state list
		self.actionSpace = self.problem.get_list_of_actions()				# Initialize the action list
		self.qFunc = self.initQFfunc()									# Initialize the Q function

		self.featureTransitionDict = self.featureTransition()			# Initialize the features used in gradient descent
		self.apxtParas = self.initApxtParas()		
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

	def initApxtParas(self):
		featuresState = list(self.featureTransitionDict.items())[0]
		featuresStateAction = list(featuresState)[1]
		values = featuresStateAction.values()
		numFeatures = len(values[0])
		return np.zeros(numFeatures)

	def featureTransition(self):
		""" Including feature set up and nomalization """
		euclideanDistSet = set()
		for i in self.stateSpace:
			x, y = i
			if x >= 0 and y >= 0:
				euclideanDistSet.add(np.sqrt(x ** 2 + y ** 2))
		euclideanDistSet = list(euclideanDistSet)

		featureTransitionDict = {}
		for i in self.stateSpace:
			featureTransitionDict[i] = {}
			for j in self.actionSpace[i]:
				array = np.zeros(2 * len(euclideanDistSet))
				x, y = i
				diffX, diffY = j
				goalX, goalY = x + diffX, y + diffY
				euclideanDist1 = np.sqrt(x ** 2 + y ** 2)
				euclideanDist2 = np.sqrt(goalX ** 2 + goalY ** 2)
				array[euclideanDistSet.index(euclideanDist1)] = 1
				array[len(euclideanDistSet) + euclideanDistSet.index(euclideanDist2)] = 1
				featureTransitionDict[i][j] = array

		return featureTransitionDict

	def get_next_action(self, currentState):
		""" Pick the action from action space with given state by 
			using epsilon greedy method """
		if rd.random() < self.epsilonGreedy:
			actions = list(self.actionSpace[currentState])
			action = actions[rd.randint(0, len(actions) - 1)]
			return action
		else:
			actions = self.qFunc[currentState]
			action = max(actions.iteritems(), key=operator.itemgetter(1))[0]
			return action

	def updateQFunc(self):
		""" Update the Q function with given current state and 
				next state by weighted TD error """
		for i in self.stateSpace:
			for j in self.actionSpace[i]:
				self.qFunc[i][j] = round(sum(self.featureTransitionDict[i][j] * self.apxtParas), 3)

	def trainEpisoid(self):
		""" Train the model with only one episoid and 
			use the predefined function update the Q
			function in every step """
		ifTerminal = lambda x: list(x)[0] == list(x)[1] == 0

		visitedStates = []

		currentState = self.problem.get_initial_state()
		visitedStates.append(currentState)

		self.initEligibility()

		step = 0
		totalReward = 0

		actions = self.actionSpace[currentState]
		action = actions[rd.randint(0, len(actions) - 1)]
		FA = self.featureTransitionDict[currentState][action]
		while len(list(currentState)) != 0 and not ifTerminal(currentState):  	# Check if the algorithm has reached the terminal
			index = [i for i, e in enumerate(FA) if e != 0]
			for i in index:
				self.eligibility[i] = 1

			self.problem.perform_action(currentState, action)						# or the object is already out of sight 
			nextState = self.problem.get_current_state()
			visitedStates.append(nextState)
			reward = self.problem.get_reward(currentState, action, nextState)
			totalReward += reward

			tdError = reward - sum(FA * self.apxtParas)
			currentState = nextState

			if len(list(currentState)) != 0:
				if not ifTerminal(currentState):
					if rd.random() < (1 - self.epsilonGreedy):
						MaxQFunc = 0
						for i in self.actionSpace[currentState]:
							Fa = self.featureTransitionDict[currentState][i]
							estimatedQ = sum(Fa * self.apxtParas)
							if estimatedQ > MaxQFunc:
								MaxQFunc = estimatedQ
								action = i
					else:
						actions = self.actionSpace[currentState]
						action = actions[rd.randint(0, len(actions) - 1)]
						FA = self.featureTransitionDict[currentState][action]
						estimatedQ = self.apxtParas * FA
					tdError += self.gamma * estimatedQ

			self.apxtParas += self.alpha * tdError * self.eligibility
			
			self.eligibility *= self.gamma * self.lambdaDiscount

			step += 1
		print visitedStates
		print 'The episoid has been done in ', step, 'step'
		return step, totalReward, visitedStates

	def trainModel(self):
		self.initQFfunc()
		self.initApxtParas()
		for i in xrange(self.numEpisoid):
			print 'Trace', i + 1, ':'
			self.trainEpisoid()
			self.updateQFunc()
			print 'Q Function'
			for j in self.qFunc:
				print j, ':', self.qFunc[j]
			# print 'paras'
			# print self.apxtParas

			self.epsilonGreedy *= 0.99

	def derivePolicy(self):
		policy = {}
		for i in self.stateSpace:
			optimalAction = max(self.qFunc[i].iteritems(), key=operator.itemgetter(1))[0]
			policy[i] = optimalAction
		return policy

	def getPolicy(self):
		return  self.derivePolicy()
