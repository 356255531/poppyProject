__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms in Vrep.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  Sarsa0InVrep = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma).
	And then call the class methed trainModel() to train. (It may depends on how you design your RL algorithm module)
	In this case sarsaZero is an algorithm module which was predefined under sarsaZero.py file.
	"""
import pypot.dynamixel			# Import the nessesary file for setting vrep

import numpy as np 								# Import the required python libs
import time
import random as rd
import itertools

from Modules.stateActionSpace import stateActionSpace	# Import the modules required by RL algorithm
from Modules.CVStateobserver import CVStateobserver 
from Modules.actorPoppy import actorPoppy
from reward import reward
from Modules.problemPoppy import problemPoppy

from sarsaZero import sarsaZero							# import the predefined RL algorithm
from sarsaLambda import sarsaLambda
from sarsaWithLinApxt import sarsaWithLinApxt

################################### Initialize Poppy ###################################
ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

################################### Reinforcement Learning Parameters Setting ###################################
positionMatrix = [4, 2]			# Number of state setting
epsilonGreedy = 0.1				# Epsilon used in epsilonGreedy method	
alpha = 0.1						# Step Length
gamma = 0.7						# Discount coefficient used in computation of TD error
numEpisoids = 200				# Number of Episoids used in trainning
lambdaDiscount = 0.9			# Lambda in SarsaLambda algorithm

################################### Creating Objects Requried by RL Algorithm ###################################
p = CVStateobserver(positionMatrix)
a = actorPoppy(dxl_io, positionMatrix)
r = reward()
s = stateActionSpace(positionMatrix)

pro = problemPoppy(p,a,r,s)						# Creating the Trainning World Object

################################### Reinforcement Learning ###################################
SarsaZeroVrep = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma)			#Creating the RL algorithm Module
sarsaLambdaVrep = sarsaLambda(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)
sarsaWithLinApxtPoppy = sarsaWithLinApxt(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)

SarsaZeroVrep.trainModel()					# Train the model with specific algorithm
# sarsaLambdaVrep.trainModel()

print '\n'
print 'The policy is'
print sarsaLambdaVrep.getPolicy()
# print SarsaZeroVrep.getPolicy()				# Output the policy derived by Q-function
