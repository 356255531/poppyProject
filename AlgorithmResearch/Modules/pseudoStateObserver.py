from CodeFramework.stateObserverAb import stateObserverAb
from pseudoCV import pseudoCV

class pseudoStateObserver(stateObserverAb, pseudoCV):
	""" Use pseudoCV algorithm to observe the agent current state"""
	def __init__(self, poppy, io, name, positionMatrix):
		pseudoCV.__init__(self, poppy, io, name, positionMatrix)
		super(pseudoStateObserver, self).__init__()


	def getCurrentState(self):
		""" Return the current state """
		return super(pseudoStateObserver, self).getPosition()

if __name__ == '__main__':
	from poppy.creatures import PoppyTorso
	import numpy as np
	import time
	import math
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

	observer = pseudoStateObserver(poppy, io, name, positionMatrix)
	print observer.getCurrentState()