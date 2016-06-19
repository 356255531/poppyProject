__author__ = 'Zhiwei Han'

import numpy as np
import random as rd
import operator

class sarsaLambda(object):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, problem, epsilonGreedy, numEpisoid, alpha, gamma, lambdaDiscount):
		self.epsilonGreedy = epsilonGreedy
		self.numEpisoid = numEpisoid
		self.alpha = alpha
		self.gamma = gamma
		self.lambdaDiscount = lambdaDiscount

		self.problem = problem

		self.stateSpace = self.problem.getStateSpace()  		# Initialize the state list
		self.actionSpace = self.problem.getActionSpace()		# Initialize the action list
		self.qFunc = self.initQFfunc()							# Initialize the Q function
		self.eligibility = self.initEligibility()				# Initialize the Eligibility

	def initQFfunc(self):
		""" Initialize the Q function 
			used in constructor """
		qFunc = {}
		for i in self.stateSpace:
			qFunc[i] = {j:0 for j in self.actionSpace[i]}
		return qFunc

	def initEligibility(self):
		""" Initialize the eligibility memory """
		eligibility = {}
		for i in self.stateSpace:
			eligibility[i] = {j:0 for j in self.actionSpace[i]}
		return eligibility

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
		""" Update the Q function with eligibility and weighted TD error """
		if len(list(nextState)) != 0:
			tdError = reward + self.gamma * self.qFunc[nextState][nextAction] - self.qFunc[currentState][action]
		else:
			tdError = reward + self.gamma * -100 - self.qFunc[currentState][action]
		self.eligibility[currentState][action] += 1
		for i in self.stateSpace:
			for j in self.actionSpace:
				self.qFunc[currentState][action] += self.alpha * tdError * self.eligibility[currentState][action]
				self.qFunc[currentState][action] = round(self.qFunc[currentState][action], 3)
				self.eligibility[currentState][action] = self.gamma * self.lambdaDiscount * self.eligibility[currentState][action]

	def trainEpisoid(self):
		""" Train the model in only one episoid and 
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
		while len(list(currentState)) != 0 and not ifTerminal(currentState):  	# Check if the algorithm has reached the terminal
			self.problem.takeAction(currentState, action)						# or the object is already out of sight 
			nextState = self.problem.getCurrentState()
			visitedStates.append(nextState)
			reward = self.problem.getReward(currentState, action, nextState)
			totalReward += reward

			if len(list(nextState)) == 0:										# If next state is out of sight then no further action can be taken
				nextAction = ()
			else:
				nextAction = self.epsilonGreedySelection(nextState)

			self.updateQFunc(currentState, action, reward, nextState, nextAction)	# Update Q function with the new knowledge of reward

			currentState = nextState
			
			action = nextAction

			step += 1
		print visitedStates
		print 'The episoid has been done in ', step, 'step'
		return step, totalReward, visitedStates

	def trainModel(self):
		""" Train the whole model within the given episoids number """
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
