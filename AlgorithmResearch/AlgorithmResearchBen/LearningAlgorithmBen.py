__author__ = 'ben'

from CodeFramework.StateActionSpace import StateActionSpace
from CodeFramework.Actor import Actor
from CodeFramework.LearningAlgorithm import LearningAlgorithm
from CodeFramework.Reward import Reward
from CodeFramework.StateObserver import StateObserver


class LearningAlgorithmBen(LearningAlgorithm):
    def __init__(self, state_action_space, Reward):
        assert isinstance(state_action_space, StateActionSpace)

        self.state_action_space = state_action_space
        self.states = state_action_space.get_list_of_states()
        self.actions = state_action_space.get_list_of_actions()
        
        self.rewardObj = Reward

        self.values = [0 for x in self.states]  # changed it from self.actions to self.states
        self.gamma = 0.7
        self.learning_rate = 0.3
        # self.policy = [(0,0) for x in self.states]
        self.policy = [(1,0), (1,0), (1,0), (-1,0), (-1,0), (-1,0)]

        self.max_number_iterations = 100
        self.global_counter = 0
        self.frequencies = [dict() for x in self.states]
        for state in self.states:
            state_freq = self.frequencies[self.states.index(state)]
            for action in self.actions:
                state_freq.update({action: [[0 for x in self.states], 0]})

    def compute_expectation(self, curr_state, freq_dict):
        exp_values_per_actions = [0 for x in self.actions]
        for action in self.actions:
            tot_number_counts = freq_dict[action][1]
            freq_per_action = freq_dict[action][0]
            exp_curr_action = 0
            for state in self.states:
                if tot_number_counts != 0:
                    probab_currState_action_state = float(freq_per_action[self.states.index(state)]) / float(tot_number_counts)
                else:
                    probab_currState_action_state = 1/float(len(self.states))
                td_error = self.rewardObj.get_rewards(curr_state, action, nextState=state, problemType='capture') + self.gamma * self.values[self.states.index(state)]
                exp_curr_action += probab_currState_action_state * td_error
            exp_values_per_actions[self.actions.index(action)] = exp_curr_action
        print "curr_state: ", curr_state, "freq_dict: ", freq_dict
        print "expected Values per action: ",  exp_values_per_actions
        return exp_values_per_actions

    def get_next_action(self, current_state):
        return self.policy[self.states.index(current_state)]

    def receive_reward(self, old_state, action, next_state, reward):
        """Do TD return"""
        old_state_index = self.states.index(old_state)
        next_state_index = self.states.index(next_state)

        td_error = reward + self.gamma * self.values[next_state_index] - self.values[old_state_index]

        self.values[old_state_index] += self.learning_rate * td_error

        # Update frequencies ~ probabilities
        self.frequencies[old_state_index][action][0][
            next_state_index] += 1  # update count of old_state -> action -> next_state
        self.frequencies[old_state_index][action][1] += 1  # update total count of old_state reached

        # Update policy
        # if self.global_counter == self.max_number_iterations:
        if next_state == (0,0) or next_state == [] or self.global_counter == 100:
            for state in self.states:
                state_index = self.states.index(state)
                expected_values = self.compute_expectation(state, self.frequencies[state_index])
                self.policy[state_index] = self.actions[expected_values.index(max(expected_values))]
            print 'policy updated'
            print self.policy, self.values
            self.global_counter = -1
        self.global_counter += 1
