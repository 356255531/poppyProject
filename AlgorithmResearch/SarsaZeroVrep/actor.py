__author__ = 'Zhiwei Han'
from pseudoStateObserver import pseudoStateObserver
from CodeFramwork.actorAb import actorAb
import itertools
import random as rd
import time
import numpy as np

class actor(pseudoStateObserver, actorAb):
	"""docstring for actor"""
	def __init__(self, poppy, io, name, positionMatrix):
		super(actor, self).__init__(poppy, io, name, positionMatrix)
		self.positionMatrix = positionMatrix
		self.poppy = poppy
		self.io = io
		self.name = name

	def motorControl(self, action, motionUnit):
		m, n = action
		angleY = self.poppy.head_y.present_position
		angleZ = self.poppy.head_z.present_position
		if m != 0 and n != 0:
			m = m / abs(m)
			n = n / abs(n)
			self.poppy.head_z.goal_position = angleZ + 1.5 * motionUnit * m
			self.poppy.head_y.goal_position = angleY + 1 * motionUnit * n
		if m != 0 and n == 0:
			m = m / abs(m)
			self.poppy.head_z.goal_position = angleZ + 1.5 * motionUnit * m
		if m == 0 and n != 0:
			n = n / abs(n)
			self.poppy.head_y.goal_position = angleY + 1 * motionUnit * n
		time.sleep(0.04)			

	def takeAction(self, action):

		if action == (0, 0):
			return 'action illegal'
		currentState = super(actor, self).getCurrentState()
		if len(list(currentState)) == 0:
			return False

		x, y = currentState
		diffX, diffY = action
		goalX, goalY = x + diffX, y + diffY
		count = 0
		while (x != goalX or y != goalY) and count < 20:
			actionX = goalX - x
			actionY = goalY - y
			a = max((abs(actionX) * 1.5) // 5, 1)
			b = max(abs(actionY) // 5, 1)
			motionUnit = min(a, b)
			self.motorControl((actionX, actionY), motionUnit)

			currentState = super(actor, self).getCurrentState()
			if len(list(currentState)) == 0:
				return False

			x, y = currentState
			count += 1
		return True

	def randMove(self, stateSpace):
		while len(list(super(actor, self).getCurrentState())) == 0:
			list1 = np.arange(-self.positionMatrix[0], self.positionMatrix[0])
			list2 = np.arange(-self.positionMatrix[1], self.positionMatrix[1])
			motionSpace = [(i, j) for i, j in itertools.product(list1, list2)]
			motionSpace.remove((0, 0))
			self.takeAction(motionSpace[rd.randint(0, len(motionSpace) - 1)])


		initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
		while initialState == (0, 0):
			initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]

		x, y = super(actor, self).getCurrentState()
		initialX, initialY = initialState
		diffX, diffY = int(initialX - x), int(initialY - y)


		while not self.takeAction((diffX, diffY)):
			initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
			while initialState == (0, 0):
				initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]

			x, y = super(actor, self).getCurrentState()
			initialX, initialY = initialState
			diffX, diffY = int(initialX - x), int(initialY - y)
			self.takeAction((diffX, diffY))

	def getActionSpace(self, stateSpace):
		pass


if __name__ == '__main__':
	from poppy.creatures import PoppyTorso
	import numpy as np
	import time
	import math
	from stateActionSpace import stateActionSpace
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
	positionMatrix = (25, 20)

	a = actor(poppy, io, name, positionMatrix)
	b = stateActionSpace(positionMatrix)
	c = pseudoStateObserver(poppy, io, name, positionMatrix)
	print 'current State Before action', c.getCurrentState()

	for i in xrange(100):
		a.randMove(b.getStateSpace())

	print 'next state after action', c.getCurrentState()