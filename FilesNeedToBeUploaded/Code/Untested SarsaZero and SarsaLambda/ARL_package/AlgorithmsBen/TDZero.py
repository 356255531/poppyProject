__author__ = 'ben'

from ..CodeFramework.LearningAlgorithm import LearningAlgorithm

import numpy as np
from random import random, randint, choice
import operator
from copy import deepcopy

class TDZero(LearningAlgorithm):
	""" The Sarsa(0) algorithm dessign. """
	def __init__(self, problem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent=None, oldData=None):
		self.epsilonGreedy = epsilonGreedy
		self.numEpisodes = numEpisodes
		self.learningRate = learningRate
		self.gamma = gamma
		self.iterNumLimit = iterNumLimit

		self.problem = problem

		self.stateSpace = self.problem.get_list_of_states()  		# Initialize the state list
		self.actionSpace = self.problem.get_list_of_actions()		# Initialize the action list
		self.valueFunc, self.policy = self.import_oldData(oldData)

		self.plotAgent = plotAgent	
		self.diagInfo = []
		self.valueFuncHistory = []
		self.policyHistory = []

	def init_policy(self):
		policy = {i:choice(self.actionSpace) for i in self.stateSpace}
		return policy

	def init_valueFunc(self):
		""" Initialize the Q function 
			used in constructor """
		valueFunc = {i:0 for i in self.stateSpace}
		return valueFunc

	def import_oldData(self, oldData):
		valueFunc = {}
		policy = {}

		if oldData:
			if oldData.has_key('values'):
				valueFunc = oldData['values']

			if oldData.has_key('policy'):
						policy = oldData['policy']
		else:
			valueFunc = self.init_valueFunc()  # changed it from self.actions to self.states
			policy = self.init_policy()  # changed it from self.actions to self.states

		return valueFunc, policy
		
	def export_oldData(self):
		oldData = {}
		oldData['policy'] = self.policy
		oldData['values'] = self.valueFunc
		return oldData

	def get_next_action(self, currentState):
		""" Pick the action from action space with given state by 
			using epsilon greedy method """
		if random() < self.epsilonGreedy:
			actions = self.actionSpace
			action = actions[randint(0, len(actions) - 1)]
			return action
		else:
			action = self.policy[currentState]
			return action

	def receive_reward(self, currentState, action, reward, nextState, nextAction):
		""" Update the Q function with given current state and 
				next state by weighted TD error """
		isTerminal = self.problem.is_terminal_state(nextState)
		if not isTerminal:
			tdError = reward + self.gamma * self.valueFunc[nextState] - self.valueFunc[currentState]
			self.valueFunc[currentState] = self.valueFunc[currentState] + self.learningRate * tdError
		else:
			tdError = reward - self.valueFunc[currentState]
			self.valueFunc[currentState] = self.valueFunc[currentState] + self.learningRate * tdError

	def update_policy(self):
		newPolicy = {}
		for i in self.stateSpace:
			maxStateValue = -1000
			for j in self.actionSpace:
				x, y = i
				m, n = j
				newState = (x + m, y + n)

				isTerminal = self.problem.is_terminal_state(newState)
				if isTerminal == 1:
					newPolicy[i] = j
					continue
				elif isTerminal == -1:
					continue

				if self.valueFunc[newState] > maxStateValue:
					maxStateValue = self.valueFunc[newState]
					newPolicy[i] = j
		return newPolicy

	def run_episode(self):
		""" Train the model with only one Episodes and 
			use the predefined function update the Q
			function in every step """
		visitedStates = []

		currentState = self.problem.get_initial_state()
		visitedStates.append(currentState)
  
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
		print 'The Episodes has been done in ', step, 'step'
		isTerminal = self.problem.is_terminal_state(currentState)
		if isTerminal == 1:
			reachCenter = True
		else:
			reachCenter = False
		return step, totalReward, reachCenter

	def train_model(self):
		for i in xrange(self.numEpisodes):
			if i % 10	 == 0:
				self.valueFuncHistory.append(deepcopy(self.valueFunc))
				self.policyHistory.append(self.get_policy())

			print 'Trace', i + 1, ':'
			stepNum, totalReward, reachCenter = self.run_episode()
			self.policy = self.update_policy()

			self.epsilonGreedy *= 0.99
			self.diagInfo.append((stepNum, totalReward, reachCenter))
		if self.plotAgent:
			self.plot(self.diagInfo, self.valueFuncHistory, self.policyHistory)

	def get_policy(self):
		return self.policy

	def plot(self, diagInfo, valueFuncHistory, policyHistory):
		"""
		Diagramm:
			Horizontal: Episodes Number
			Vertical:
				1. Step Number
				2. Total Reward
				3. If reach center
				4. Q function difference every 100 Episodes
		Graph:
			Policy after 10 Episodes
		"""
		self.plotAgent.plot(diagInfo, valueFuncHistory, policyHistory)
		# self.plotAgent.plot(self.diagInfo, self.policyHistory)