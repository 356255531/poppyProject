__author__ = 'Zhiwei Han'

""" This Script will run the predefined algorithms within a dummy tranning world.
	When you want to run your predefined RL algorithms, firstly set up a class with your predefined algorithm model.
	E.g.  SarsaZeroDummy = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma).
	And then call the class methed trainModel() to train. (It may depends on how you design your RL algorithm module)
	In this case sarsaZero is an algorithm module which was predefined under sarsaZero.py file. """
from Modules.stateActionSpace import stateActionSpace	# Import the modules required by RL algorithm
from reward import reward

from sarsaZero import sarsaZero							# import the predefined RL algorithm
from sarsaLambda import sarsaLambda
# from sarsaWithLinApxt import sarsaWithLinApxt

from Modules.problemDummy import problemDummy


################################### Reinforcement Learning Parameters Setting ###################################
positionMatrix = [2, 1]			# Number of state setting
epsilonGreedy = 0.1				# Epsilon used in epsilonGreedy method	
alpha = 0.1						# Step Length
gamma = 0.7						# Discount coefficient used in computation of TD error
numEpisoids = 200				# Number of Episoids used in trainning
lambdaDiscount = 0.9			# Lambda in SarsaLambda algorithm

################################### Creating Objects Requried by RL Algorithm ###################################
r = reward()
s = stateActionSpace(positionMatrix)
pro = problemDummy(r,s)

# ################################### Reinforcement Learning ###################################
sarsaZeroDummy = sarsaZero(pro, epsilonGreedy, numEpisoids, alpha, gamma)			#Creating the RL algorithm Module
sarsaLambdaDummy = sarsaLambda(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)
# sarsaWithLinApxtDummy = sarsaWithLinApxt(pro, epsilonGreedy, numEpisoids, alpha, gamma, lambdaDiscount)


sarsaZeroDummy.trainModel()					# Train the model with specific algorithm
# sarsaLambdaDummy.trainModel()
# sarsaWithLinApxtDummy.trainModel()


print '\n'
print 'The policy is'
# print sarsaLambdaDummy.getPolicy()
print sarsaZeroDummy.getPolicy()				# Output the policy derived by Q-function