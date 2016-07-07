__author__ = 'Zhiwei Han'

import itertools
import random as rd
import time
import numpy as np

from ..CodeFramework.Actor import Actor

class actorPoppy(Actor):
	""" Real Poppy """
	def __init__(self, poppy, dimensions=(3, 1)):
		""" 
		params:
			poppy: robot interface 
			dimensions: tuple(m, n), grid number of state in horizontal and vertical
		"""
		super(actorPoppy, self).__init__()
		self.dimensions = dimensions
		self.poppy = poppy

		ids = [36, 37]
		speed = dict(zip(ids, itertools.repeat(200)))
		self.poppy.enable_torque(ids)
		self.poppy.set_moving_speed(speed)

	def perform_action(self, action):
		""" Action may be not deterministic and may not change the state
			Params:
				action: tuple(m, n) next trend state (x + m, y + n)
			"""
		m, n = action
		if m == 0 and n == 0:
			return False
		if m == 0:
			n = abs(n) / n
		if n == 0 :
			m = abs(m) / m

		angleY = self.poppy.get_present_position((37, ))[0]
		angleZ = self.poppy.get_present_position((36, ))[0]

		mm, nn = self.dimensions
		motionUnitX = 10 / mm
		motionUnitY = 6 / nn
		smallerEle = min(motionUnitX, motionUnitY)
		motionUnit = max(1, smallerEle)

		if m != 0 and n != 0:
			goalZ = angleZ + 1.5 * motionUnit * m
			goalY = angleY + 1 * motionUnit * n
			pos = dict(zip([36, 37], [goalZ, goalY]))
			self.poppy.set_goal_position(pos)
		if m != 0 and n == 0:
			goalZ = angleZ + 1.5 * motionUnit * m
			self.poppy.set_goal_position({36:goalZ})
		if m == 0 and n != 0:
			goalY = angleY + 1 * motionUnit * n
			self.poppy.set_goal_position({37:goalY})
		time.sleep(0.04)			

	def come_to_zero(self):
		pos = dict(zip([36, 37], [0, -25]))
		self.poppy.set_goal_position(pos)
		time.sleep(0.04)

	def initialise_episode(self):
		""" Initialize by changing the position of red point """
		pass

if __name__ == '__main__':
	""" Only for testing and need not to be modified """
