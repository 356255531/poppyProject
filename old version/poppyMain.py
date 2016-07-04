__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms on real poppy.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  Sarsa0InPoppy = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma).
	And then call the class methed trainModel() to train. (It may depends on how you design your RL algorithm module)
	In this case sarsaZero is an algorithm module which was predefined under sarsaZero.py file.
	"""
from ARL_package.StateActionSetting import StateActionSpaceFull

from ARL_package.Reward import RewardZhiwei

from ARL_package.AlgorithmsZhiwei import SarsaZero, SarsaLambda, SarsaWithLinApxt

from ARL_package.CodeFramework import PlotAgent
################################### Reinforcement Learning Parameters Setting ###################################
dimension = (5, 3)					# Number of state setting
epsilonGreedy = 0.3					# Epsilon used in epsilonGreedy method	
alpha = 0.1							# Step Length
gamma = 0.7							# Discount coefficient used in computation of TD error
numEpisoids = 2000					# Number of Episoids used in trainning
lambdaDiscount = 0.5				# Lambda in SarsaLambda algorithm
iterNumLimit = 500					# Iteration number Limit

################################### Reinforcement Learning with Mathematical Model ###################################
## Initialize MathModel and Create Objects
from ARL_package.MathematicalClasses import MathematicalActor, MathematicalObserver, ProblemDummy
from ARL_package.StateActionSetting import StateActionSpaceFull

dummyStateActionSpace = StateActionSpaceFull(dimension)
dummyObserver = MathematicalObserver(dummyStateActionSpace)
dummyActor = MathematicalActor(dummyObserver)
dummyReward = RewardZhiwei(dummyStateActionSpace)

dummyProblem = ProblemDummy(dummyObserver, dummyActor, 
	dummyReward, dummyStateActionSpace)

plotAgent = PlotAgent(dimension)

## Reinforcement Learning with Mathmatical Model
sarsaZeroDummyLerner = SarsaZero(dummyProblem, epsilonGreedy, 
	numEpisoids, alpha, gamma, iterNumLimit, plotAgent)
sarsaLambdaDummyLerner = SarsaLambda(dummyProblem, epsilonGreedy, 
	numEpisoids, alpha, gamma, lambdaDiscount, iterNumLimit, plotAgent)

## Train Model
sarsaZeroDummyLerner.train_model()
# sarsaLambdaDummyLerner.train_model()

print 'Policy is'
print sarsaZeroDummyLerner.get_policy()
# print sarsaLambdaDummyLerner.get_policy()

qFunc = sarsaZeroDummyLerner.export_qFunc()
# qFunc = sarsaLambdaDummyLerner.export_qFunc()

################################### Reinforcement Learning with Real Poppy ###################################

## Initialize Poppy
from ARL_package.PoppyClasses import ProblemPoppy, CVStateObserver, ActorPoppy

import pypot.dynamixel

ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

## Create Objects Requried by RL Algorithm
poppyStateActionSpace = StateActionSpaceFull(dimension)
poppyObserver = CVStateObserver(dimension)
poppyActor = ActorPoppy(dxl_io, dimension)
poppyReward = RewardZhiwei()

poppyProblem = ProblemPoppy(poppyObserver, poppyActor, 
	poppyReward, poppyStateActionSpace)

## Reinforcement Learning with Real Poppy
SarsaZeroPoppyLerner = SarsaZero(dummyProblem, epsilonGreedy, 
	numEpisoids, alpha, gamma, iterNumLimit, plotAgent, qFunc)
sarsaLambdaPoppyLerner = SarsaLambda(dummyProblem, epsilonGreedy, 
	numEpisoids, alpha, gamma, lambdaDiscount, iterNumLimit, plotAgent, qFunc)

## Train Model
sarsaZeroPoppyLerner.train_model()
# sarsaLambdaPoppyLerner.train_model()

print 'Policy is'
print sarsaZeroPoppyLerner.get_policy()
# print sarsaLambdaPoppyLerner.get_policy()