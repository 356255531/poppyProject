__author__ = 'Zhiwei Han'
from CodeFramework.TrainningWorld import TrainningWorld
from stateActionSpace import stateActionSpace	# Import the modules required by RL algorithm
from pseudoStateObserver import pseudoStateObserver 
from actorVrep import actorVrep
from reward import reward

class problemVrep(TrainningWorld):
	""" A trainning world of agent and enviroment.
		The main and only object interacts with learning algorithm
		during learning. """
	def __init__(self, pseudoStateObserver, actorVrep, reward, stateActionSpace):
		super(problemVrep, self).__init__()
		self.pseudoStateObserver = pseudoStateObserver
		self.actorVrep = actorVrep
		self.reward = reward
		self.stateActionSpace = stateActionSpace

		self.stateSpace = self.stateActionSpace.get_list_of_states()
		self.actionSpace = self.stateActionSpace.get_list_of_actions()
		self.reward = reward

	def get_current_state(self):
		""" Return the current state """
		return self.pseudoStateObserver.get_current_state()

	def get_initial_state(self):
		self.actorVrep.randMove(self.stateSpace)
		return self.pseudoStateObserver.get_current_state()

	def get_list_of_states(self):
		return self.stateSpace

	def get_list_of_actions(self):
		return self.actionSpace

	def perform_action(self, currentState, action):
		self.actorVrep.perform_action(action)

	def get_reward(self, currentState, action, nextState):
		return self.reward.get_reward(currentState, action, nextState)

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
	from poppy.creatures import PoppyTorso
	import numpy as np
	import time
	import math

	from stateActionSpace import stateActionSpace
	from pseudoStateObserver import pseudoStateObserver 
	from actorVrep import actorVrep
	from reward import reward

	poppy = PoppyTorso(simulator='vrep')

	io = poppy._controllers[0].io
	name = 'cube'
	position = [0, -0.15, 0.85] # X, Y, Z
	sizes = [0.1, 0.1, 0.1] # in meters
	mass = 0 # in kg
	io.add_cube(name, position, sizes, mass)
	time.sleep(1)
	name1 = 'cube2'
	position1 = [0, -1, 0.5]
	sizes1 = [3, 1, 1]
	io.add_cube(name1, position1, sizes1, mass)
	io.set_object_position('cube', position=[0, -1, 1.05])
	positionMatrix = [25, 20]

	p = pseudoStateObserver(poppy, io, name, positionMatrix)
	a = actorVrep(poppy, io, name, positionMatrix)
	r = reward()
	s = stateActionSpace(positionMatrix)
	pro = problemVrep(p,a,r,s)

	print pro.get_initial_state()