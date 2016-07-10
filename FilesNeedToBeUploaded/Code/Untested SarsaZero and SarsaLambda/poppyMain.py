__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms on real poppy.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  sarsaZeroDummyLearner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit)
	And then call the class methed trainModel() to train.

	After learning the trained Q function in the mathematical model, it will be passed into the online learning an poppy.
	But unfortunately, the camera breaks down and we are not able to do that with SARSA(0) and SARSA(lambda).
	"""
from ARL_package.StateActionSetting import StateActionSpaceMath

from ARL_package.Reward import RewardZhiwei, RewardBen

from ARL_package.AlgorithmsZhiwei import SarsaZero, SarsaLambda, SarsaWithLinApxt
from ARL_package.AlgorithmsBen import TDZero

from ARL_package.CodeFramework import PlotAgent, PlotAgentValueFunc, GridStateActionSpace2D

from ARL_package.StateActionSetting import StateActionSpaceMath, StateActionSpaceVrep

################################### Reinforcement Learning Parameters Setting ###################################
dimension = (9, 7)					# Number of state setting
epsilonGreedy = 0.6					# Epsilon used in epsilonGreedy method	
learningRate = 0.1					# learningRate
gamma = 0.7							# Discount coefficient used in computation of TD error
numEpisodes = 4500					# Number of Episodes used in trainning
lambdaDiscount = 0.5				# Lambda in SarsaLambda algorithm
iterNumLimit = 500					# Iteration number Limit

################################### Reinforcement Learning with Mathematical Model ###################################
from ARL_package.MathematicalClasses import MathematicalActor, MathematicalObserver, ProblemDummy

print 'Initializing the modules'
dummyStateActionSpace = StateActionSpaceMath(dimension)
# dummyStateActionSpace = GridStateActionSpace2D(dimensions=dimension,allow_diag_actions=True)
dummyObserver = MathematicalObserver(dummyStateActionSpace)
dummyActor = MathematicalActor(dummyObserver)

plotAgent = PlotAgent(dimension)
plotAgentValueFunc = PlotAgentValueFunc(dimension)
# plotAgent = None

print 'Choosing reward'
dummyReward = RewardZhiwei(dummyStateActionSpace)
# dummyReward = RewardBen(dummyStateActionSpace)

print 'Creating training world'
dummyProblem = ProblemDummy(dummyObserver, dummyActor, dummyReward, dummyStateActionSpace)

print 'Choosing reinforcement algorithm lerner'		# Choose learning algorithm by uncommenting one of them
# dummyLearner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent)
# dummyLearner = SarsaLambda(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent)
# dummyLearner = TDZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgentValueFunc)

print 'Training model'					
dummyLearner.train_model()

print 'Outputing policy'
print 'The policy is:'
print dummyLearner.get_policy()

print 'Exporting the old data'
oldData = dummyLearner.export_oldData()

# ################################### Reinforcement Learning with Vrep ###################################
from ARL_package.VrepClasses import ObserverVrep, ActorVrep, ProblemVrep

from time import sleep

print 'Initializing the modules'
vrepStateActionSpace = StateActionSpaceVrep(dimension)
# vrepStateActionSpace = GridStateActionSpace2D(dimensions=dimension,allow_diag_actions=True)
vrepObserver = ObserverVrep(vrepStateActionSpace, dimension)
vrepActor = ActorVrep(vrepObserver)

print 'Choosing reward'
vrepReward = RewardZhiwei(vrepStateActionSpace)

print 'Creating training world'
vrepProblem = ProblemVrep(vrepObserver, vrepActor, vrepReward, vrepStateActionSpace)

print 'Initializing reinforcement algorithm learner'
# vrepLearner = SarsaZero(vrepProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent, oldData)
# vrepLearner = SarsaLambda(vrepProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent, oldData)
# vrepLearner = TDZero(vrepProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgentValueFunc, oldData)

print 'Training model'
vrepLearner.train_model()

print 'Outputing policy'
print 'The policy is:'
print vrepLearner.get_policy()

print 'Exporting the old data'
oldData = vrepLearner.export_oldData()

# ################################ Reinforcement Learning with Real Poppy ###################################
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

# print 'Choosing reward'
# poppyReward = RewardZhiwei()

# print 'Creating training world'
# poppyProblem = ProblemPoppy(poppyObserver, poppyActor, poppyReward, poppyStateActionSpace)

# print 'Initializing reinforcement algorithm Learner'
# # poppyLearner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent, oldData)
# # poppyLearner = SarsaLambda(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent, oldData)
# # poppyLearner = TDZero(poppyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgentValueFunc, oldData)

# print 'Trainning model'
# poppyLearner.train_model()

# print 'Outputing policy'
# print 'The policy is:'
# print poppyLearner.get_policy()

# print 'Exporting the old data'
# oldData = poppyLearner.export_oldData()