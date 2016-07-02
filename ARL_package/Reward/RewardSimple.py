__author__ = 'ben'
# changes:
# 1 created a simple get_rewards-function
# 2 changed the name get_reward -> get_rewards (as defined in the framework)

from CodeFramework.Reward import Reward

class RewardSimple(Reward):
    """ The class gives the setting of reward """
    def __init__(self, final_reward, final_penalty):
        self.reward = final_reward
        self.penalty = final_penalty
        
    def get_rewards(self, currentState, action, nextState):
        if nextState == []:
            return self.penalty
        elif nextState == (0,0):
            return self.reward
        else:
            return 0

if __name__ == '__main__':
	a = RewardSimple(10,-10)
	print a.get_rewards((1, 2), (1, 0), (1, 1), 'capture') # changed to correct function name
