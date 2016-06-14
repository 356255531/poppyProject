from poppy.creatures import PoppyTorso
import numpy as np
import time
import random as rd

from stateActionSpace import stateActionSpace
from pseudoStateObserver import pseudoStateObserver 
from actor import actor
from reward import reward
from problem import problem

from SarsaZeroVrep import SarsaZeroVrep

poppy = PoppyTorso(simulator='vrep')

################################### Object Interaction ###################################
io = poppy._controllers[0].io 		# Object parameter setting
name = 'cube'
position = [0, -0.15, 0.85] 		# X, Y, Z
sizes = [0.1, 0.1, 0.1] 			# in meters
mass = 0 							# in kg

io.add_cube(name, position, sizes, mass)	# Add object
time.sleep(1)

name1 = 'cube2'						# Second object parameter setting
position1 = [0, -1, 0.5]
sizes1 = [3, 0.3, 1]
io.add_cube(name1, position1, sizes1, mass)	# Add second object

io.set_object_position('cube', position=[0, -1, 1.05])	# Relocate the first object
######################################################################

################################### Reinforcement Learning ###################################
positionMatrix = [2, 1]					# Number of state setting
epsilonGreedy = 0.1
alpha = 0.1
gamma = 0.7
numEpisoids = 100

p = pseudoStateObserver(poppy, io, name, positionMatrix)
a = actor(poppy, io, name, positionMatrix)
r = reward()
s = stateActionSpace(positionMatrix)
pro = problem(p,a,r,s)
Sarsa0InVrep = SarsaZeroVrep(pro, epsilonGreedy, numEpisoids, alpha, gamma)

Sarsa0InVrep.trainModel()
print Sarsa0InVrep.getPolicy()