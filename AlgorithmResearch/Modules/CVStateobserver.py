from CodeFramework.StateObserver import StateObserver
from CVAlgorithm import CVAlgorithm
import math

class CVStateObserver(StateObserver, CVAlgorithm):
	""" Use pseudoCV algorithm to observe the agent current state"""
	def __init__(self, positionMatrix):
		super(CVStateObserver, self).__init__()
		self.positionMatrix = positionMatrix

	def get_current_state(self):
		""" Return the current state """
		a = super(CVStateObserver, self).getPosition()
		if len(list(a)) == 0:
			return ()
		coordinate, shape = a
		y, x = coordinate
		n, m = shape
		m, n = m / 2, n / 2
		x, y = x - m, n - y

		mm, nn = self.positionMatrix
		unitX, unitY = m / mm, n / nn
		x = math.floor(x / unitX)
		y = math.floor(y / unitY)
		return (x, y)

if __name__ == '__main__':
	positionMatrix = [25, 20]
	observer = CVStateObserver(positionMatrix)
	print observer.get_current_state()