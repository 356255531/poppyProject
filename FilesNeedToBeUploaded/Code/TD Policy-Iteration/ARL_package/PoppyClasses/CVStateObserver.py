from ..CodeFramework.StateObserver import StateObserver
from CVAlgorithm import CVAlgorithm
from math import floor

class CVStateObserver(StateObserver, CVAlgorithm):
	""" Use computer vision algorithm to observe the agent current state"""
	def __init__(self, dimensions=(3, 1)):
		super(CVStateObserver, self).__init__()
		self.dimensions = dimensions

	def get_current_state(self):
		""" Return the current state """
		a = super(CVStateObserver, self).getPosition()
		if len(list(a)) == 0:
			return (10000, 10000)
		mm, nn = self.dimensions
		if mm % 2 == 0:
			mm += 1
		if nn % 2 == 0:
			nn += 1

		coordinate, shape = a
		y, x = coordinate
		n, m = shape

		unitX = m / float(mm)
		unitY = n / float(nn)
		xx = floor(x / unitX)
		yy = floor(y / unitY)
		print 'mm', unitX
		print 'nn', unitY
		
		x = int(xx - floor(mm / 2))
		y = int(yy - floor(nn / 2))

		print 'x,y:',x,-y
		if (x < -floor(self.dimensions[0]/2) or x > floor(self.dimensions[0]/2) or
			y < -floor(self.dimensions[1]/2) or y > floor(self.dimensions[1]/2)):
			return (10000,10000)

		return (x, -y)

	def is_terminal_state(self, state):
		""" returns if the current state is terminal

        Current implementation: (0,0) is terminal

        :param state: state inquired about
        :return: is_terminal: boolean
        """
		return state == (0, 0)

if __name__ == '__main__':
	dimensions = (25, 20)
	observer = CVStateObserver(dimensions)
	print observer.get_current_state()