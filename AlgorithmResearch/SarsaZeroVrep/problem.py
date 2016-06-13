__author__ = 'Zhiwei Han'

class problem(object):
	def __init__(self, pseudoStateObserver, actor, reward, stateActionSpace):
		self.pseudoStateObserver = pseudoStateObserver
		self.actor = actor
		self.reward = reward
		self.stateActionSpace = stateActionSpace

		self.stateSpace = self.stateActionSpace.getStateSpace()
		self.actionSpace = self.stateActionSpace.getActionSpace()

	def initStateSpace(self):
		pass

	def getInitialState(self):
		self.actor.randMove(self.stateSpace)
		return self.pseudoStateObserver.getCurrentState()

	def getStateSpace(self):
		return self.stateSpace

	def getActionSpace(self):
		return self.actionSpace

	def takeAction(self, currentState, action):
		self.actor.takeAction(action)

	def getSuccessor(self, currentState, action):
		diffX, diffY = action
		x, y = currentState
		newX, newY = x + diffX, y + diffY
		return (newX, newY)

		x, y = currentState
		diffX, diffY = action
		nextState = (x + diffX, y + diffY)
		return reward.get_rewards(currentState, action, nextState)

if __name__ == '__main__':
	from poppy.creatures import PoppyTorso
	import numpy as np
	import time
	import math

	from stateActionSpace import stateActionSpace
	from pseudoStateObserver import pseudoStateObserver 
	from actor import actor
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
	a = actor(poppy, io, name, positionMatrix)
	r = reward()
	s = stateActionSpace(positionMatrix)
	pro = problem(p,a,r,s)

	print pro.getSuccessor((0, -3), (10, 10))