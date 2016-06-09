from poppy.creatures import PoppyTorso
import numpy as np
import time
from SarsaZeroVrep import SarsaZeroVrep

poppy = PoppyTorso(simulator='vrep')

# Add object
io = poppy._controllers[0].io
name = 'cube'
position = [0, -0.15, 0.85] # X, Y, Z
sizes = [0.1, 0.1, 0.1] # in meters
mass = 0 # in kg
io.add_cube(name, position, sizes, mass)
time.sleep(1)
name1 = 'cube2'
position1 = [0, -1, 0.5]
sizes1 = [3, 0.3, 1]
io.add_cube(name1, position1, sizes1, mass)
io.set_object_position('cube', position=[0, -1, 1.05])

positionMatrix = [25, 20]
errorAfterTrained = 10e-6
epsilonGreedy = 0.1
Sarsa0InVrep = SarsaZeroVrep(self, poppy, io, name, positionMatrix, errorAfterTrained, epsilonGreedy)