__author__ = 'Zhiwei Han'
from CodeFramework.TrainningWorld import TrainningWorld
from GridStateActionSpace2D import GridStateActionSpace2D
from CVStateObserver import CVStateObserver 
from actorPoppy import actorPoppy
from reward import reward
import time

class problemPoppy(TrainningWorld):
	""" A trainning world of agent and enviroment.
		The main and only object interacts with learning algorithm
		during learning. """
	def __init__(self, CVStateObserver, actorPoppy, reward, GridStateActionSpace2D):
		super(problemPoppy, self).__init__()
		self.CVStateObserver = CVStateObserver
		self.actorPoppy = actorPoppy
		self.reward = reward
		self.GridStateActionSpace2D = GridStateActionSpace2D

		self.stateSpace = self.GridStateActionSpace2D.get_list_of_states()
		self.actionSpace = self.GridStateActionSpace2D.get_list_of_actions()
		self.reward = reward

	def get_current_state(self):
		""" Return the current state """
		return self.CVStateObserver.get_current_state()

	def get_initial_state(self):
		self.actorPoppy.come_to_zero()
		time.sleep(3)
		currentState = self.CVStateObserver.get_current_state()
		while currentState == (0, 0) or currentState == ():
			currentState = self.get_current_state
			time.sleep(1)

	def get_list_of_states(self):
		return self.stateSpace

	def get_list_of_actions(self):
		return self.actionSpace

	def perform_action(self, currentState, action):
		self.actorPoppy.perform_action(action)

	def get_reward(self, currentState, action, nextState):
		return self.reward.get_rewards(currentState, action, nextState)

	# def getSuccessor(self, currentState, action):
	# 	diffX, diffY = action
	# 	x, y = currentState
	# 	newX, newY = x + diffX, y + diffY
	# 	return (newX, newY)

	# 	x, y = currentState
	# 	diffX, diffY = action
	# 	nextState = (x + diffX, y + diffY)
	# 	return reward.get_rewards(currentState, action, nextState)



if __name__ == '__main__':
	pass