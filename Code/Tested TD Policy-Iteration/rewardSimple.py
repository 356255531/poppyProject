__author__ = 'ben'
# changes:
# 1 created a simple get_rewards-function
# 2 changed the name get_reward -> get_rewards (as defined in the framework)
# 3 kept Zhiwei's function as get_rewards_ to have quick access to it

from CodeFramework.Reward import Reward
import numpy as np

class rewardSimple(Reward):
    """ The class gives the setting of reward """
    def __init__(self):
        super(rewardSimple, self).__init__()
        
    def get_rewards(self, currentState, action, nextState, problemType='capture'):
        if nextState == []:
            return -10
        elif nextState == (0,0):
            return 1
        else:
            return 0

    def get_rewards_(self, currentState, action, nextState=None, problemType='capture'): # changed to correct function name
        """This method give back the reward value according to given current
            state, action, next state and if it's a greeting or avoiding case(optional).
            By default is greeting. """
        if len(list(currentState)) == 0 and len(list(nextState)) == 0:
            return 0

        if problemType == 'capture':
            if len(list(currentState)) == 0:
                if len(list(nextState)) != 0:
                    return 0
            if len(list(currentState)) != 0:
                if len(list(nextState)) == 0:
                    return -100
            euclideanDis1 = list(currentState)[0] ** 2 + list(currentState)[1] ** 2
            euclideanDis2 = list(nextState)[0] ** 2 + list(nextState)[1] ** 2
            absReward = np.sqrt(euclideanDis1) - np.sqrt(euclideanDis2)
            if absReward > 0:
                return round(absReward, 3)
            else:
                return round(absReward, 3) - 1
        else:
            if len(list(currentState)) == 0:
                if len(list(nextState)) != 0:
                    return -100
            if len(list(currentState)) != 0:
                if len(list(nextState)) == 0:
                    return 100
            euclideanDis1 = list(currentState)[0] ** 2 + list(currentState)[1] ** 2
            euclideanDis2 = list(nextState)[0] ** 2 + list(nextState)[1] ** 2
            if absReward < 0:
                return -round(absReward, 3)
            else:
                return -round(absReward, 3) - 1
if __name__ == '__main__':
	a = rewardSimple()
	print a.get_rewards((1, 2), (1, 0), (1, 1), 'capture') # changed to correct function name
