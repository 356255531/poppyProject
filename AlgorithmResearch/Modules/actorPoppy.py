__author__ = 'Zhiwei Han'

import itertools					# Import the neccesary python libs
import random as rd
import time
import numpy as np

from CVStateObserver import CVStateObserver		# Import the required modules
from CodeFramework.Actor import Actor

class actorPoppy(CVStateObserver, Actor):
	"""Agent in the trainning enviromtn"""
	def __init__(self, poppy,positionMatrix):
		super(actor, self).__init__(poppy, io, name, positionMatrix)
		self.positionMatrix = positionMatrix		# The state size (2 * positionMatrix[0] + 1) * (2 * positionMatrix[1] + 1)
		self.poppy = poppy 							# The virtual poppy in Vrep

		ids = [36, 37]
		speed = dict(zip(ids, itertools.repeat(50)))
		self.poppy.enable_torque(ids)
		self.poppy.set_moving_speed(speed)			# Motor speed setting

	def __motorControl(self, action, motionUnit):
		""" Motor control interface and unexpected to be called outside the class 
			action: Head moves left: (-1, 0), right:(0, 1), rightdown(1, -1) etc.
			motionUnit: used to accelerate or slow down the movement
			"""
		m, n = action
		angleY = self.poppy.get_present_position((37, ))[0]
		angleZ = self.poppy.get_present_position((36, ))[0]
		if m != 0 and n != 0:
			m = m / abs(m)
			n = n / abs(n)
			goalZ = angleZ + 1.5 * motionUnit * m
			goalY = angleY + 1 * motionUnit * n
			pos = dict(zip([36, 37], [goalZ, goalY]))
			self.poppy.set_goal_position(pos)
		if m != 0 and n == 0:
			m = m / abs(m)
			goalZ = angleZ + 1.5 * motionUnit * m
			self.poppy.set_goal_position({36:goalZ})
		if m == 0 and n != 0:
			n = n / abs(n)
			goalY = angleY + 1 * motionUnit * n
			self.poppy.set_goal_position({37:goalY})
		time.sleep(0.04)			

	def perform_action(self, action):
		""" Use closed loop control the agent move to the next corresponding state. 
			The definition of action see in self.__motorControl.
			When no obect in sight, return Flase. """
		if action == (0, 0):
			return 'action illegal'
		currentState = super(actor, self).get_current_state()
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
			self.__motorControl((actionX, actionY), motionUnit)

			currentState = super(actor, self).get_current_state()
			if len(list(currentState)) == 0:
				return False

			x, y = currentState
			count += 1
		return True

	def randMove(self, stateSpace):
		""" Agent moves to a random state by being given state space """
		while len(list(super(actor, self).get_current_state())) == 0:
			list1 = np.arange(-self.positionMatrix[0], self.positionMatrix[0])
			list2 = np.arange(-self.positionMatrix[1], self.positionMatrix[1])
			motionSpace = [(i, j) for i, j in itertools.product(list1, list2)]
			motionSpace.remove((0, 0))
			self.perform_action(motionSpace[rd.randint(0, len(motionSpace) - 1)])


		initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
		while initialState == (0, 0):
			initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]

		x, y = super(actor, self).get_current_state()
		initialX, initialY = initialState
		diffX, diffY = int(initialX - x), int(initialY - y)


		while not self.perform_action((diffX, diffY)):
			initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
			while initialState == (0, 0):
				initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]

			x, y = super(actor, self).get_current_state()
			initialX, initialY = initialState
			diffX, diffY = int(initialX - x), int(initialY - y)
			self.perform_action((diffX, diffY))


if __name__ == '__main__':
	""" Only for testing and need not to be modified """
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
	c = CVStateObserver(poppy, io, name, positionMatrix)
	print 'current State Before action', c.get_current_state()

	for i in xrange(100):
		a.randMove(b.getStateSpace())

	print 'next state after action', c.get_current_state()