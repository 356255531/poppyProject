__author__ = 'Zhiwei Han'
from CodeFramework.TrainningWorld import TrainningWorld
import random as rd

class problemDummy(TrainningWorld):
	""" A trainning world of agent and enviroment, which only use math model
		without any simulation.
		The main and only object interacts with learning algorithm
		during learning. """
	def __init__(self, reward, stateActionSpace):
		super(problemDummy, self).__init__()
		self.reward = reward
		self.stateActionSpace = stateActionSpace

		self.stateSpace = self.stateActionSpace.get_list_of_states()
		self.actionSpace = self.stateActionSpace.get_list_of_actions()
		self.currentState = self.get_initial_state()

	def get_current_state(self):
		""" Return the current state """
		x, y = self.currentState
		xx = list(self.stateActionSpace.positionMatrix)[0]
		yy =list(self.stateActionSpace.positionMatrix)[1]
		if abs(x) > xx or abs(y) > yy:
			return ()
		else:
			return self.currentState

	def get_initial_state(self):
		initialState = self.stateSpace[rd.randint(0, len(self.stateSpace) - 1)]
		self.currentState = initialState
		return initialState

	def get_list_of_states(self):
		return self.stateSpace

	def get_list_of_actions(self):
		return self.actionSpace

	def perform_action(self, currentState, action):
		x, y = self.currentState 
		diffX, diffY = action
		self.currentState = (x + diffX, y + diffY)

	def get_reward(self, currentState, action, nextState):
		return self.reward.get_reward(currentState, action, nextState)