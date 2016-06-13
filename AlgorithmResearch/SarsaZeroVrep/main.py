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

p = pseudoStateObserver(poppy, io, name, positionMatrix)
a = actor(poppy, io, name, positionMatrix)
r = reward()
s = stateActionSpace(positionMatrix)
pro = problem(p,a,r,s)
Sarsa0InVrep = SarsaZeroVrep(pro, errorAfterTrained, epsilonGreedy)
