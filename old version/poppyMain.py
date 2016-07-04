__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms on real poppy.
	When you want to run your  predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  Sarsa0InPoppy = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma).
	And then call the class methed trainModel() to train. (It may depends on how you design your RL algorithm module)
	In this case sarsaZero is an algorithm module which was predefined under sarsaZero.py file.
	"""
from ARL_package.MathematicalClasses import MathematicalActor, MathematicalObserver
from ARL_package.StateActionSetting import StateActionSpaceFull
from ARL_package.PoppyClasses import ProblemDummy

from ARL_package.Reward import RewardZhiwei

from ARL_package.AlgorithmsZhiwei import SarsaZero, SarsaLambda, SarsaWithLinApxt

from ARL_package.CodeFramework import PlotAgent
################################### Reinforcement Learning Parameters Setting ###################################
dimension = (15, 9)				# Number of state setting
epsilonGreedy = 0.3				# Epsilon used in epsilonGreedy method	
alpha = 0.1					# Step Length
gamma = 0.7						# Discount coefficient used in computation of TD error
numEpisoids = 20000			# Number of Episoids used in trainning
lambdaDiscount = 0.5			# Lambda in SarsaLambda algorithm
iterNumLimit = 500

################################### Initialize MathModel ###################################
from ARL_package.MathematicalClasses import MathematicalActor
from ARL_package.MathematicalClasses import MathematicalObserver
from ARL_package.StateActionSetting import StateActionSpaceFull
from ARL_package.PoppyClasses import ProblemDummy

dummyStateActionSpace = StateActionSpaceFull(dimension)
dummyObserver = MathematicalObserver(dummyStateActionSpace)
dummyActor = MathematicalActor(dummyObserver)
dummyReward = RewardZhiwei(dummyStateActionSpace)
dummyProblem = ProblemDummy(dummyObserver, dummyActor, 
	dummyReward, dummyStateActionSpace)
dummyPlotAgent = PlotAgent(dimension)

sarsaZeroDummyLerner = SarsaZero(dummyProblem, epsilonGreedy, 
	numEpisoids, alpha, gamma, iterNumLimit, dummyPlotAgent)
sarsaLambdaDummyLerner = SarsaLambda(dummyProblem, epsilonGreedy, 
	numEpisoids, alpha, gamma, lambdaDiscount, iterNumLimit)

sarsaZeroDummyLerner.train_model()
# sarsaLambdaDummyLerner.train_model()

print 'Policy is'
print sarsaZeroDummyLerner.get_policy()
# print sarsaLambdaDummyLerner.get_policy()

qFunc = sarsaZeroDummyLerner.export_qFunc()
# qFunc = sarsaLambdaDummyLerner.export_qFunc()

# ################################### Initialize Poppy ###################################
# from ARL_package.PoppyClasses import StateActionSpaceFull
# from ARL_package.PoppyClasses import CVStateObserver 
# from ARL_package.PoppyClasses import ActorPoppy

# import pypot.dynamixel

# ports = pypot.dynamixel.get_available_ports()
# print('available ports:', ports)

# port = ports[0]
# print('Using the first on the list', port)

# dxl_io = pypot.dynamixel.DxlIO(port)
# print('Connected!')



# ################################### Creating Objects Requried by RL Algorithm ###################################
# p = CVStateObserver(dimension)
# a = ActorPoppy(dxl_io, dimension)
# r = RewardZhiwei()
# s = StateActionSpaceFull(dimension)

# ################################### Reinforcement Learning ###################################
# SarsaZeroPoppy = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma)			#Creating the RL algorithm Module
# sarsaLambdaPoppy = sarsaLambda(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)
# sarsaWithLinApxtPoppy = sarsaWithLinApxt(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)

# SarsaZeroPoppy.trainModel()					# Train the model with specific algorithm
# # sarsaLambdaPoppy.trainModel()

# print '\n'
# print 'The policy is'
# # print sarsaLambdaPoppy.getPolicy()
# print SarsaZeroPoppy.getPolicy()				# Output the policy derived by Q-function
