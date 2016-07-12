__author__ = 'Zhiwei Han'
from ..CodeFramework.LearningAlgorithm import LearningAlgorithm

import numpy as np
from random import randint, random
import operator
from copy import deepcopy

class SarsaLambda(LearningAlgorithm):
	"""docstring for SarsaZeroVrep"""
	def __init__(self, problem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent=None, qFunc=None):
		self.epsilonGreedy = epsilonGreedy
		self.numEpisodes = numEpisodes
		self.learningRate = learningRate
		self.gamma = gamma
		self.lambdaDiscount = lambdaDiscount
		self.iterNumLimit = iterNumLimit

		self.problem = problem

		self.stateSpace = self.problem.get_list_of_states()  		# Initialize the state list
		self.actionSpace = self.problem.get_list_of_actions()		# Initialize the action list
		self.qFunc = self.import_oldData(qFunc)						# Initialize the Q function
		self.eligibility = self.init_eligibility()				# Initialize the Eligibility

		self.plotAgent = plotAgent	
		self.diagInfo = []
		self.qFuncHistory = []
		self.policyHistory = []

	def import_oldData(self, oldData):
		if oldData:
			if oldData.has_key('Q Function'):
				qFunc = oldData['Q Function']
		else:
			qFunc = self.init_qFunc()  # changed it from self.actions to self.states

		return qFunc

	def init_qFunc(self):
		""" Initialize the Q function 
			used in constructor """
		qFunc = {}
		for i in self.stateSpace:
			qFunc[i] = {j:0 for j in self.actionSpace}
		return qFunc

	def init_eligibility(self):
		""" Initialize the eligibility memory """
		eligibility = {}
		for i in self.stateSpace:
			eligibility[i] = {j:0 for j in self.actionSpace}
		return eligibility

	def get_next_action(self, currentState):
		""" Pick the action from action space with given state by 
			using epsilon greedy method """
		if random() < self.epsilonGreedy:
			actions = self.actionSpace
			action = actions[randint(0, len(actions) - 1)]
			return action
		else:
			actions = self.qFunc[currentState]
			action = max(actions.iteritems(), key=operator.itemgetter(1))[0]
			return action

	def receive_reward(self, currentState, action, reward, nextState, nextAction):
		""" Update the Q function with eligibility and weighted TD error """
		isTerminal = self.problem.is_terminal_state(nextState)
		if not isTerminal:
			tdError = reward + self.gamma * self.qFunc[nextState][nextAction] - self.qFunc[currentState][action]
		else:
			tdError = reward - self.qFunc[currentState][action]
		self.eligibility[currentState][action] = 1
		for i in self.stateSpace:
			for j in self.actionSpace:
				self.qFunc[currentState][action] += self.learningRate * tdError * self.eligibility[currentState][action]
				self.qFunc[currentState][action] = self.qFunc[currentState][action]
				self.eligibility[currentState][action] *= self.gamma * self.lambdaDiscount

	def run_episode(self):
		""" Train the model in only one episoid and 
			use the predefined function update the Q
			function in every step """
		visitedStates = []

		currentState = self.problem.get_initial_state()
		visitedStates.append(currentState)

		self.init_eligibility()

		step = 0
		totalReward = 0
		iterNum = 0

		action = self.get_next_action(currentState)
		isTerminal = self.problem.is_terminal_state(currentState)
		while not isTerminal and iterNum < self.iterNumLimit:  	# Check if the algorithm has reached the terminal
			self.problem.perform_action(action)						# or the object is already out of sight 
			nextState = self.problem.get_current_state()
			visitedStates.append(nextState)
			reward = self.problem.get_reward(currentState, action, nextState)
			totalReward += reward

			isTerminal = self.problem.is_terminal_state(nextState)
			if isTerminal:										# If next state is out of sight then no further action can be taken
				nextAction = ()
			else:
				nextAction = self.get_next_action(nextState)

			self.receive_reward(currentState, action, reward, nextState, nextAction)	# Update Q function with the new knowledge of reward

			currentState = nextState
			
			action = nextAction

			step += 1
			iterNum += 1
		print visitedStates
		print 'The episoid has been done in ', step, 'step'
		isTerminal = self.problem.is_terminal_state(currentState)
		if isTerminal == 1:
			reachCenter = True
		else:
			reachCenter = False
		return step, totalReward, reachCenter

	def train_model(self):
		""" Train the whole model within the given episoids number """
		for i in xrange(self.numEpisodes):
			if i % 10	 == 0:
				self.qFuncHistory.append(deepcopy(self.qFunc))
				self.policyHistory.append(self.get_policy())

			print 'Trace', i + 1, ':'
			stepNum, totalReward, reachCenter = self.run_episode()
			self.epsilonGreedy *= 0.99

			self.diagInfo.append((stepNum, totalReward, reachCenter))

		if self.plotAgent:
			self.plot(self.diagInfo, self.qFuncHistory, self.policyHistory)

	def get_policy(self):
		policy = {}
		stateSpace = self.stateSpace
		for i in stateSpace:			
			optimalAction = max(self.qFunc[i].iteritems(), key=operator.itemgetter(1))[0]
			policy[i] = optimalAction
		return policy

	def export_oldData(self):
		oldData = {}
		oldData['Q Function'] = self.qFunc
		return oldData

	def plot(self, diagInfo, qFuncHistory, policyHistory):
		"""
		Diagramm:
			Horizontal: Episoid Number
			Vertical:
				1. Step Number
				2. Total Reward
				3. If reach center
				4. Q function difference every 100 episoid
		Graph:
			Policy after 100 Episoid
		"""
		self.plotAgent.plot(diagInfo, qFuncHistory, policyHistory)
		# self.plotAgent.plot(self.diagInfo, self.policyHistory)