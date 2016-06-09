__author__ = 'Zhiwei Han'
from pseudoCV import pseudoCV
import itertools

class actor(pseudoCV):
	"""docstring for actor"""
	def __init__(self, poppy, io, name, positionMatrix):
		pseudoCV.__init__(self, poppy, io, name, positionMatrix)
		self.positionMatrix = positionMatrix
		self.poppy = poppy
		self.io = io
		self.name = name


	def getCurrentPosition(self):
		return pseudoCV.getPosition()

	def getAllPosition(self):
		m, n = self.positionMatrix

		list1 = [i for i in range(- m // 2, m // 2 + 1)]
		list2 = [i for i in range(- n // 2, n // 2 + 1)]

		allPosition = []
		for x, y in itertools.product(list1, list2):
			allPosition.append((x, y))

		return allPosition

	def takeAction(self, currentPosition, action):

		def headMotionVertical(k):
			k = k / abs(k)
		    angleY = poppy.head_y.present_position
		    poppy.head_y.goal_position = angleY - 3 * k
		    time.sleep(0.02)

		def headMotionHorizontal(k):
			k = k / abs(k)
		    angleZ = poppy.head_z.present_position
		    poppy.head_z.goal_position = angleZ - 3 * k
		    time.sleep(0.02)

		def headMotionUpRight(k, b):
			k = k / abs(k)
			b = b / abs(b)
		    angleY = poppy.head_y.present_position
		    angleZ = poppy.head_z.present_position
		    poppy.head_z.goal_position = angleZ - 3 * k
		    poppy.head_y.goal_position = angleY - 3 * b
		    time.sleep(0.02)

		x, y = currentPosition
		diffX, diffY = action
		newX, newY = x + diffX, y + diffY

		while :
			pass


	def randMove(self):
		pass

