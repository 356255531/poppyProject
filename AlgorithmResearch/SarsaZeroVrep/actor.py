__author__ = 'Zhiwei Han'
from pseudoStateObserver import pseudoStateObserver
from CodeFramwork.actorAb import actorAb
import itertools
import random as rd
import time

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
			print 'action', (m, n)
			self.poppy.head_z.goal_position = angleZ + 1.5 * motionUnit * m
			self.poppy.head_y.goal_position = angleY + 1 * motionUnit * n
		if m != 0 and n == 0:
			m = m / abs(m)
			print 'action', (m, n)
			self.poppy.head_z.goal_position = angleZ + 1.5 * motionUnit * m
		if m == 0 and n != 0:
			n = n / abs(n)
			print 'action', (m, n)
			self.poppy.head_y.goal_position = angleY + 1 * motionUnit * n
		time.sleep(0.04)			

	def takeAction(self, action):

		if action == (0, 0):
			return 'action illegal'
		x, y = super(actor, self).getCurrentState()
		diffX, diffY = action
		goalX, goalY = x + diffX, y + diffY
		while x != goalX or y != goalY:
			actionX = goalX - x
			actionY = goalY - y
			if abs(actionX) != 0:
				motionUnit = (abs(actionX) * 1.5) // 5;
			if abs(actionY) != 0:
				if abs(actionY) // 5 < motionUnit:
					print 'actionY', actionY
					motionUnit = abs(actionY) // 5
			if motionUnit < 1:
				motionUnit = 1
			print motionUnit
			self.motorControl((actionX, actionY), motionUnit)
			x, y = super(actor, self).getCurrentState()
			print 'current state', (x, y)

	def randMove(self, stateSpace):
		goalState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
		while abs(list(goalState)[0]) == list(self.positionMatrix)[0] or abs(list(goalState)[1]) == list(self.positionMatrix)[1]:
			goalState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
		x, y = super(actor, self).getCurrentState()
		goalX, goalY = goalState
		diffX, diffY = int(goalX - x), int(goalY - y)

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

	a.randMove(b.getStateSpace())

	print 'next state after action', c.getCurrentState()