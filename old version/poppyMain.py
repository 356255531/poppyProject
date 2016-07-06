__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms on real poppy.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  Sarsa0InPoppy = sarsaZero(pro, epsilonGreedy, numEpisodes, alpha, gamma).
	And then call the class methed trainModel() to train. (It may depends on how you design your RL algorithm module)
	In this case sarsaZero is an algorithm module which was predefined under sarsaZero.py file.
	"""
from ARL_package.StateActionSetting import StateActionSpaceFull

from ARL_package.Reward import RewardZhiwei
from ARL_package.Reward import RewardBen

from ARL_package.AlgorithmsZhiwei import SarsaZero, SarsaLambda, SarsaWithLinApxt

from ARL_package.CodeFramework import PlotAgent
from ARL_package.CodeFramework import GridStateActionSpace2D
################################### Reinforcement Learning Parameters Setting ###################################
dimension = (7, 5)					# Number of state setting
epsilonGreedy = 0.1					# Epsilon used in epsilonGreedy method	
alpha = 0.3							# Step Length
gamma = 0.5							# Discount coefficient used in computation of TD error
numEpisodes = 5000					# Number of Episodes used in trainning
lambdaDiscount = 0.5				# Lambda in SarsaLambda algorithm
iterNumLimit = 500					# Iteration number Limit

################################### Reinforcement Learning with Mathematical Model ###################################
## Initialize MathModel and Create Objects
from ARL_package.MathematicalClasses import MathematicalActor, MathematicalObserver, ProblemDummy
from ARL_package.StateActionSetting import StateActionSpaceFull

dummyStateActionSpace = StateActionSpaceFull(dimension)
# dummyStateActionSpace = GridStateActionSpace2D(dimensions=dimension,allow_diag_actions=True)
dummyObserver = MathematicalObserver(dummyStateActionSpace)
dummyActor = MathematicalActor(dummyObserver)
dummyReward = RewardZhiwei(dummyStateActionSpace)
# dummyReward = RewardBen(dummyStateActionSpace)

dummyProblem = ProblemDummy(dummyObserver, dummyActor, 
	dummyReward, dummyStateActionSpace)

plotAgent = PlotAgent(dimension)

## Reinforcement Learning with Mathmatical Model
sarsaZeroDummyLerner = SarsaZero(dummyProblem, epsilonGreedy, 
	numEpisodes, alpha, gamma, iterNumLimit, plotAgent)
sarsaLambdaDummyLerner = SarsaLambda(dummyProblem, epsilonGreedy, 
	numEpisodes, alpha, gamma, lambdaDiscount, iterNumLimit, plotAgent)

## Train Model
sarsaZeroDummyLerner.train_model()
# sarsaLambdaDummyLerner.train_model()

print 'Policy is'
print sarsaZeroDummyLerner.get_policy()
# print sarsaLambdaDummyLerner.get_policy()

qFunc = sarsaZeroDummyLerner.export_qFunc()
# # qFunc = sarsaLambdaDummyLerner.export_qFunc()

################################### Reinforcement Learning with Vrep ###################################
# from ARL_package.VrepClasses import ObserverVrep, ActorVrep
# from time import sleep

# # poppy = PoppyTorso(simulator='vrep')

# # io = poppy._controllers[0].io
# # name1 = 'support'
# # position1 = [-0.4, -1, 0.5]
# # sizes1 = [3, 1, 1]
# # mass1 = 0  # in kg
# # io.add_cube(name1, position1, sizes1, mass1)

# # sleep(1)
# # name2 = 'cube'
# # position2 = [0, -1, 1.05]  # X, Y, Z
# # sizes2 = [0.1, 0.1, 0.1]  # in meters
# # mass2 = 0  # in kg
# # io.add_cube(name2, position2, sizes2, mass2)

# vrepStateActionSpace = StateActionSpaceFull(dimension)
# # vrepStateActionSpace = GridStateActionSpace2D(dimensions=dimension,allow_diag_actions=True)
# vrepObserver = ObserverVrep(vrepStateActionSpace, dimension)
# vrepActor = ActorVrep(vrepObserver)
# vrepReward = RewardZhiwei(vrepStateActionSpace)

# vrepProblem = ProblemVrep(vrepObserver, vrepActor, 
# 	vrepReward, vrepStateActionSpace)

# plotAgent = PlotAgent(dimension)

# ## Reinforcement Learning with Mathmatical Model
# sarsaZeroVrepLerner = SarsaZero(vrepProblem, epsilonGreedy, 
# 	numEpisodes, alpha, gamma, iterNumLimit, plotAgent)
# sarsaLambdaVrepLerner = SarsaLambda(vrepProblem, epsilonGreedy, 
# 	numEpisodes, alpha, gamma, lambdaDiscount, iterNumLimit, plotAgent)

# ## Train Model
# # sarsaZeroVrepLerner.train_model()
# sarsaLambdaVrepLerner.train_model()

# print 'Policy is'
# print sarsaZeroVrepLerner.get_policy()
# # print sarsaLambdaVrepLerner.get_policy()

# qFunc = sarsaZeroVrepLerner.export_qFunc()
# # # qFunc = sarsaLambdaDummyLerner.export_qFunc()
################################### Reinforcement Learning with Real Poppy ###################################

# ## Initialize Poppy
# from ARL_package.PoppyClasses import ProblemPoppy, CVStateObserver, ActorPoppy

# import pypot.dynamixel

# ports = pypot.dynamixel.get_available_ports()
# print('available ports:', ports)

# port = ports[0]
# print('Using the first on the list', port)

# dxl_io = pypot.dynamixel.DxlIO(port)
# print('Connected!')

# ## Create Objects Requried by RL Algorithm
# poppyStateActionSpace = StateActionSpaceFull(dimension)
# poppyObserver = CVStateObserver(dimension)
# poppyActor = ActorPoppy(dxl_io, dimension)
# poppyReward = RewardZhiwei()

# poppyProblem = ProblemPoppy(poppyObserver, poppyActor, 
# 	poppyReward, poppyStateActionSpace)

# ## Reinforcement Learning with Real Poppy
# SarsaZeroPoppyLerner = SarsaZero(dummyProblem, epsilonGreedy, 
# 	numEpisodes, alpha, gamma, iterNumLimit, plotAgent, qFunc)
# sarsaLambdaPoppyLerner = SarsaLambda(dummyProblem, epsilonGreedy, 
# 	numEpisodes, alpha, gamma, lambdaDiscount, iterNumLimit, plotAgent, qFunc)

# ## Train Model
# sarsaZeroPoppyLerner.train_model()
# # sarsaLambdaPoppyLerner.train_model()

# print 'Policy is'
# print sarsaZeroPoppyLerner.get_policy()
# # print sarsaLambdaPoppyLerner.get_policy()