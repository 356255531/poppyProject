__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms on real poppy.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  sarsaZeroDummyLerner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit)
	And then call the class methed trainModel() to train.

	After learning the trained Q function in the mathematical model, it will be passed into the online learning an poppy.
	But unfortunately, the camera breaks down and we are not able to do that with SARSA(0) and SARSA(lambda).
	"""
from ARL_package.StateActionSetting import StateActionSpaceMath

from ARL_package.Reward import RewardZhiwei, RewardBen

from ARL_package.AlgorithmsZhiwei import SarsaZero, SarsaLambda, SarsaWithLinApxt

from ARL_package.CodeFramework import PlotAgent, GridStateActionSpace2D

from ARL_package.StateActionSetting import StateActionSpaceMath, StateActionSpaceVrep

################################### Reinforcement Learning Parameters Setting ###################################
dimension = (5, 3)					# Number of state setting
epsilonGreedy = 0.2					# Epsilon used in epsilonGreedy method	
learningRate = 0.1					# learningRate
gamma = 0.7							# Discount coefficient used in computation of TD error
numEpisodes = 1000					# Number of Episodes used in trainning
lambdaDiscount = 0.5				# Lambda in SarsaLambda algorithm
iterNumLimit = 50					# Iteration number Limit

################################### Reinforcement Learning with Mathematical Model ###################################
from ARL_package.MathematicalClasses import MathematicalActor, MathematicalObserver, ProblemDummy

print 'Initializing the modules'
dummyStateActionSpace = StateActionSpaceMath(dimension)
# dummyStateActionSpace = GridStateActionSpace2D(dimensions=dimension,allow_diag_actions=True)
dummyObserver = MathematicalObserver(dummyStateActionSpace)
dummyActor = MathematicalActor(dummyObserver)
dummyReward = RewardZhiwei(dummyStateActionSpace)
# dummyReward = RewardBen(dummyStateActionSpace)

dummyProblem = ProblemDummy(dummyObserver, dummyActor, dummyReward, dummyStateActionSpace)

plotAgent = PlotAgent(dimension)						# If plots are not needed can set plotAgent = None
# plotAgent = None

print 'Initializing reinforcement algorithm lerner'
sarsaZeroDummyLerner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent)
sarsaLambdaDummyLerner = SarsaLambda(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent)

print 'Training model'
# sarsaZeroDummyLerner.train_model()
sarsaLambdaDummyLerner.train_model()

print 'Outputing policy'
print 'The policy is:'
# print sarsaZeroDummyLerner.get_policy()
print sarsaLambdaDummyLerner.get_policy()

print 'Exporting the Q function'
qFunc = sarsaZeroDummyLerner.export_qFunc()
# # qFunc = sarsaLambdaDummyLerner.export_qFunc()

################################### Reinforcement Learning with Vrep ###################################
from ARL_package.VrepClasses import ObserverVrep, ActorVrep, ProblemVrep

from time import sleep

print 'Initializing the modules'
vrepStateActionSpace = StateActionSpaceVrep(dimension)
# vrepStateActionSpace = GridStateActionSpace2D(dimensions=dimension,allow_diag_actions=True)
vrepObserver = ObserverVrep(vrepStateActionSpace, dimension)
vrepActor = ActorVrep(vrepObserver)
vrepReward = RewardZhiwei(vrepStateActionSpace)

vrepProblem = ProblemVrep(vrepObserver, vrepActor, vrepReward, vrepStateActionSpace)

plotAgent = PlotAgent(dimension)						# If plots are not needed can set plotAgent = None
# plotAgent = None

# print 'Initializing reinforcement algorithm lerner'
# sarsaZeroVrepLerner = SarsaZero(vrepProblem, epsilonGreedy, 
# 	numEpisodes, learningRate, gamma, iterNumLimit, plotAgent, qFunc)
# sarsaLambdaVrepLerner = SarsaLambda(vrepProblem, epsilonGreedy, 
# 	numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent, qFunc)

# print 'Training model'
# sarsaZeroVrepLerner.train_model()
# # sarsaLambdaVrepLerner.train_model()

# print 'Outputing policy'
# print 'The policy is:'
# print sarsaZeroVrepLerner.get_policy()
# # print sarsaLambdaVrepLerner.get_policy()

# print 'Exporting the Q function'
# qFunc = sarsaZeroVrepLerner.export_qFunc()
# # qFunc = sarsaLambdaDummyLerner.export_qFunc()

# ################################### Reinforcement Learning with Real Poppy ###################################
# from ARL_package.PoppyClasses import ProblemPoppy, CVStateObserver, ActorPoppy
# from ARL_package.StateActionSetting import StateActionSpacePoppy


# import pypot.dynamixel

# print 'Initializing poppy'
# ports = pypot.dynamixel.get_available_ports()
# print('available ports:', ports)

# port = ports[0]
# print('Using the first on the list', port)

# dxl_io = pypot.dynamixel.DxlIO(port)
# print('Connected!')

# print 'Initializing the modules'
# poppyStateActionSpace = StateActionSpacePoppy(dimension)
# poppyObserver = CVStateObserver(dimension)
# poppyActor = ActorPoppy(dxl_io, dimension)
# poppyReward = RewardZhiwei()

# poppyProblem = ProblemPoppy(poppyObserver, poppyActor, 
# 	poppyReward, poppyStateActionSpace)

# print 'Initializing reinforcement algorithm lerner'
# SarsaZeroPoppyLerner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent, qFunc)
# sarsaLambdaPoppyLerner = SarsaLambda(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent, qFunc)

# print 'Trainning model'
# sarsaZeroPoppyLerner.train_model()
# # sarsaLambdaPoppyLerner.train_model()

# print 'Outputing policy'
# print 'The policy is:'
# print sarsaZeroPoppyLerner.get_policy()
# # print sarsaLambdaPoppyLerner.get_policy()

# print 'Exporting the Q function'
# qFunc = SarsaZeroPoppyLerner.export_qFunc()
# # qFunc = sarsaLambdaPoppyLerner.export_qFunc()