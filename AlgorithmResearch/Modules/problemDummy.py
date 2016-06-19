__author__ = 'Zhiwei Han'
from CodeFramework.trainningWorld import trainningWorld
import random as rd

class problemDummy(trainningWorld):
	""" A trainning world of agent and enviroment, which only use math model
		without any simulation.
		The main and only object interacts with learning algorithm
		during learning. """
	def __init__(self, reward, stateActionSpace):
		super(problemDummy, self).__init__()
		self.reward = reward
		self.stateActionSpace = stateActionSpace

		self.stateSpace = self.stateActionSpace.getStateSpace()
		self.actionSpace = self.stateActionSpace.getActionSpace()
		self.currentState = self.getInitialState()

	def getCurrentState(self):
		""" Return the current state """
		x, y = self.currentState
		xx = list(self.stateActionSpace.positionMatrix)[0]
		yy =list(self.stateActionSpace.positionMatrix)[1]
		if abs(x) > xx or abs(y) > yy:
			return ()
		else:
			return self.currentState

	def getInitialState(self):
		initialState = self.stateSpace[rd.randint(0, len(self.stateSpace) - 1)]
		self.currentState = initialState
		return initialState

	def getStateSpace(self):
		return self.stateSpace

	def getActionSpace(self):
		return self.actionSpace

	def takeAction(self, currentState, action):
		x, y = self.currentState 
		diffX, diffY = action
		self.currentState = (x + diffX, y + diffY)

	def getReward(self, currentState, action, nextState):
		return self.reward.getReward(currentState, action, nextState)