__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms in Vrep.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  Sarsa0InVrep = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma).
	And then call the class methed trainModel() to train. (It may depends on how you design your RL algorithm module)
	In this case sarsaZero is an algorithm module which was predefined under sarsaZero.py file.
	"""
from poppy.creatures import PoppyTorso			# Import the nessesary file for setting vrep

import numpy as np 								# Import the required python libs
import time
import random as rd

from Modules.stateActionSpace import stateActionSpace	# Import the modules required by RL algorithm
from Modules.pseudoStateObserver import pseudoStateObserver 
from Modules.actorVrep import actorVrep
from reward import reward
from Modules.problemVrep import problemVrep

from sarsaZero import sarsaZero							# import the predefined RL algorithm
from sarsaLambda import sarsaLambda

################################### Initialize Vrep ###################################
poppy = PoppyTorso(simulator='vrep')

################################### Object Interaction ###################################
io = poppy._controllers[0].io 					# Object controller setting

name1 = 'Support'								# Obeject parameters' setting
position1 = [0, -1, 0.5]						# Position Coordinates
size1 = [3, 0.3, 1]								# Size
mass1 = 0										# Mass
io.add_cube(name1, position1, size1, mass1)		# Add second object

time.sleep(1)

name2 = 'cube'
position2 = [0, -1, 1.05]
size2 = [0.1, 0.1, 0.1]
mass2 = 0
io.add_cube(name2, position2, size2, mass2)

################################### Reinforcement Learning Parameters Setting ###################################
positionMatrix = [4, 2]			# Number of state setting
epsilonGreedy = 0.1				# Epsilon used in epsilonGreedy method	
alpha = 0.1						# Step Length
gamma = 0.7						# Discount coefficient used in computation of TD error
numEpisoids = 200				# Number of Episoids used in trainning
lambdaDiscount = 0.9			# Lambda in SarsaLambda algorithm

################################### Creating Objects Requried by RL Algorithm ###################################
p = pseudoStateObserver(poppy, io, name2, positionMatrix)
a = actorVrep(poppy, io, name2, positionMatrix)
r = reward()
s = stateActionSpace(positionMatrix)

pro = problemVrep(p,a,r,s)						# Creating the Trainning World Object

################################### Reinforcement Learning ###################################
SarsaZeroVrep = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma)			#Creating the RL algorithm Module
sarsaLambdaVrep = sarsaLambda(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)

SarsaZeroVrep.trainModel()					# Train the model with specific algorithm
# sarsaLambdaVrep.trainModel()

print '\n'
print 'The policy is'
print sarsaLambdaVrep.getPolicy()
# print SarsaZeroVrep.getPolicy()				# Output the policy derived by Q-function
