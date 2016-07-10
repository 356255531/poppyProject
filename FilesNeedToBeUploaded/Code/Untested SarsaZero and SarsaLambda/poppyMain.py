__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms on mathematical model as well as on Vrep.
    It should work an real poppy but due to the camera broken it has never been tested.
    When you want to run your  predefined RL algorithms, just uncomment one algorithm in {choosing reinforcement learning learner}.

    Please note, since it will pass the learned parameters in mathematical model into next learning platform(Vrep or real poppy). 
    Make sure to use the same kind of algorithms in learning (Sarsa(0) can together with Sarsa(lambda) with Q function).

    """
from ARL_package.StateActionSetting import StateActionSpaceMath

from ARL_package.Reward import RewardZhiwei, RewardBen

from ARL_package.AlgorithmsZhiwei import SarsaZero, SarsaLambda, SarsaWithLinApxt

from ARL_package.CodeFramework import PlotAgent, PlotAgentValueFunc, GridStateActionSpace2D

from ARL_package.StateActionSetting import StateActionSpaceMath, StateActionSpaceVrep

################################### Reinforcement Learning Parameters Setting ###################################
dimension = (5, 3)            # Number of state setting
epsilonGreedy = 0.5           # Epsilon used in epsilonGreedy method  
learningRate = 0.1            # learningRate
gamma = 0.7                  # Discount coefficient used in computation of TD error
numEpisodes = 1000            # Number of Episodes used in trainning
lambdaDiscount = 0.5          # Lambda in SarsaLambda algorithm
iterNumLimit = 50             # Iteration number Limit

################################### Reinforcement Learning with Mathematical Model ###################################
from ARL_package.MathematicalClasses import MathematicalActor, MathematicalObserver, ProblemDummy

print 'Initializing the modules'
dummyStateActionSpace = StateActionSpaceMath(dimension)
dummyObserver = MathematicalObserver(dummyStateActionSpace)
dummyActor = MathematicalActor(dummyObserver)

plotAgent = PlotAgent(dimension)
# plotAgent = None

print 'Choosing reward'
dummyReward = RewardZhiwei(dummyStateActionSpace)
# dummyReward = RewardBen(dummyStateActionSpace)

print 'Creating training world'
dummyProblem = ProblemDummy(dummyObserver, dummyActor, dummyReward, dummyStateActionSpace)

print 'Choosing reinforcement algorithm lerner'     # Choose learning algorithm by uncommenting one of them
dummyLearner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent)
# dummyLearner = SarsaLambda(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent)

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
vrepObserver = ObserverVrep(vrepStateActionSpace, dimension)
vrepActor = ActorVrep(vrepObserver)

print 'Choosing reward'
vrepReward = RewardZhiwei(vrepStateActionSpace)

print 'Creating training world'
vrepProblem = ProblemVrep(vrepObserver, vrepActor, vrepReward, vrepStateActionSpace)

print 'Initializing reinforcement algorithm learner'
# vrepLearner = SarsaZero(vrepProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent, oldData)
# vrepLearner = SarsaLambda(vrepProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent, oldData)

print 'Training model'
vrepLearner.train_model()

print 'Outputing policy'
print 'The policy is:'
print vrepLearner.get_policy()

print 'Exporting the old data'
oldData = vrepLearner.export_oldData()

################################ Reinforcement Learning with Real Poppy ###################################
from ARL_package.PoppyClasses import ProblemPoppy, CVStateObserver, ActorPoppy
from ARL_package.StateActionSetting import StateActionSpacePoppy


import pypot.dynamixel

print 'Initializing poppy'
ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

print 'Initializing the modules'
poppyStateActionSpace = StateActionSpacePoppy(dimension)
poppyObserver = CVStateObserver(dimension)
poppyActor = ActorPoppy(dxl_io, dimension)

print 'Choosing reward'
poppyReward = RewardZhiwei()

print 'Creating training world'
poppyProblem = ProblemPoppy(poppyObserver, poppyActor, poppyReward, poppyStateActionSpace)

print 'Initializing reinforcement algorithm Learner'
# poppyLearner = SarsaZero(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, iterNumLimit, plotAgent, oldData)
# poppyLearner = SarsaLambda(dummyProblem, epsilonGreedy, numEpisodes, learningRate, gamma, lambdaDiscount, iterNumLimit, plotAgent, oldData)

print 'Trainning model'
poppyLearner.train_model()

print 'Outputing policy'
print 'The policy is:'
print poppyLearner.get_policy()

print 'Exporting the old data'
oldData = poppyLearner.export_oldData()