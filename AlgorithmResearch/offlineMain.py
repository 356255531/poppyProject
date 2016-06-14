from poppy.creatures import PoppyTorso
import numpy as np
import time
import random as rd

from Modules.stateActionSpace import stateActionSpace
from reward import reward
from Modules.offlineProblem import offlineProblem

from SarsaZero import SarsaZero


################################### Reinforcement Learning ###################################
positionMatrix = [5, 3]					# Number of state setting
epsilonGreedy = 0.1
alpha = 0.1
gamma = 0.7
numEpisoids = 200

r = reward()
s = stateActionSpace(positionMatrix)
pro = offlineProblem(r,s)
Sarsa0InVrep = SarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma)

Sarsa0InVrep.trainModel()
print '\n\n\n\n\n\n'
print 'The policy is'
print Sarsa0InVrep.getPolicy()
