from poppy.creatures import PoppyTorso
import numpy as np
import time
import random as rd

from Modules.stateActionSpace import stateActionSpace
from reward import reward
from Modules.offlineProblem import offlineProblem

from sarsaZero import sarsaZero
from sarsaLambda import sarsaLambda


################################### Reinforcement Learning ###################################
positionMatrix = [5, 3]					# Number of state setting
epsilonGreedy = 0.1
alpha = 0.1
gamma = 0.7
numEpisoids = 200
lambdaDiscount = 0.9
delta = 0.8

r = reward()
s = stateActionSpace(positionMatrix)
pro = offlineProblem(r,s)

# Sarsa0InVrep = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma)
Sarsa0InVrep = sarsaLambda(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount, delta)

Sarsa0InVrep.trainModel()
print '\n\n\n\n\n\n'
print 'The policy is'
print Sarsa0InVrep.getPolicy()
