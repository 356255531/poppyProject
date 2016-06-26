__author__ = 'ben'

from CodeFramework.StateActionSpace import StateActionSpace
from CodeFramework.Actor import Actor
from CodeFramework.LearningAlgorithm import LearningAlgorithm
from CodeFramework.Reward import Reward
from CodeFramework.StateObserver import StateObserver
import random as rd


class LearningAlgorithmBen(LearningAlgorithm):
    def __init__(self, state_action_space, Reward):
        assert isinstance(state_action_space, StateActionSpace)

        self.state_action_space = state_action_space
        self.states = state_action_space.get_list_of_states()
        # self.states.append([])
        self.actions = state_action_space.get_list_of_actions()
        if not( (0,0) in self.actions ):
            self.actions.append((0,0))
        self.rewardObj = Reward
        self.epsilon = 0.1
        self.values = [0 for x in self.states]  # changed it from self.actions to self.states
        self.gamma = 0.7
        self.learning_rate = 0.3
        # self.policy = [(0,0) for x in self.states]
        self.policy = [ (0,0) for x in self.states]
        for stat in self.states:
            self.policy[self.states.index(stat)] = self.state_action_space.get_eligible_actions(stat)[0]

        self.frequencies = [dict() for x in self.states]
        for state in self.states:
            state_freq = self.frequencies[self.states.index(state)]
            for action in self.actions:
                state_freq.update({action: [[0 for x in self.states], 0]})
        print self.states
        print self.frequencies

    def compute_expectation(self, curr_state, freq_dict):
        exp_values_per_actions = [0 for x in self.actions]
        for action in self.state_action_space.get_eligible_actions(curr_state):
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
        # print "curr_state: ", curr_state, "freq_dict: ", freq_dict
        # print "expected Values per action: ",  exp_values_per_actions
        return exp_values_per_actions

    def get_next_action(self, current_state):
        if rd.random() >= 0.1:
            return self.policy[self.states.index(current_state)]
        else:
            return rd.choice(self.state_action_space.get_eligible_actions(current_state))

    def receive_reward(self, old_state, action, next_state, reward):
        """Do TD return"""
        old_state_index = self.states.index(old_state)
        next_state_index = self.states.index(next_state)

        td_error = reward + self.gamma * self.values[next_state_index] - self.values[old_state_index]

        self.values[old_state_index] += self.learning_rate * td_error
        # Update frequencies ~ probabilities
        self.frequencies[old_state_index][action][0][next_state_index] += 1  # update count of old_state -> action -> next_state
        self.frequencies[old_state_index][action][1] += 1  # update total count of old_state reached

    def finalise_episode(self):
        print('finalise episode')
        # Update policy
        # if self.global_counter == self.max_number_iterations:
        for state in self.states:
            state_index = self.states.index(state)
            expected_values = self.compute_expectation(state, self.frequencies[state_index])
            self.policy[state_index] = self.actions[expected_values.index(max(expected_values))]
        print 'policy updated'
        print self.policy, self.values

    def plot_results(self):
        pass


if __name__ == '__main__':
    from rewardSimple import rewardSimple
    from actorVrep import actorVrep
    from pseudoStateObserver import pseudoStateObserver
    from CodeFramework.GridStateActionSpace import GridStateActionSpace2D
    from CodeFramework.main import run_learning
    from CodeFramework.main import run_episode
    from LearningAlgorithmBen import LearningAlgorithmBen

    from poppy.creatures import PoppyTorso
    import numpy as np
    import time
    import math

    poppy = PoppyTorso(simulator='vrep')

    io = poppy._controllers[0].io
    name = 'cube'
    position = [0, -0.15, 0.85]  # X, Y, Z
    sizes = [0.1, 0.1, 0.1]  # in meters
    mass = 0  # in kg
    io.add_cube(name, position, sizes, mass)
    time.sleep(1)
    name1 = 'cube2'
    position1 = [-0.4, -1, 0.5]
    sizes1 = [3, 1, 1]
    io.add_cube(name1, position1, sizes1, mass)
    io.set_object_position('cube', position=[0, -1, 1.05])
    positionMatrix = (9, 5)

    # observer = pseudoStateObserver()
    # print(observer.get_current_state())

    dummy_states_actions = GridStateActionSpace2D(dimensions=positionMatrix,allow_diag_actions=True)
    # dummy_states_actions.stateSpace[0] = 2 #because I defined the loop to run while current state wasn't 0/false

    dummy_observer = pseudoStateObserver(poppy, io, name, positionMatrix)
    dummy_actor = actorVrep(poppy, io, name, positionMatrix)
    dummy_reward = rewardSimple()
    dummy_learner = LearningAlgorithmBen(dummy_states_actions, dummy_reward)

    # run_learning(dummy_actor, dummy_learner, dummy_reward, dummy_observer)
    for i in xrange(10):
        run_episode(dummy_actor, dummy_learner, dummy_reward, dummy_observer, dummy_states_actions, max_num_iterations=50)
    print 'current_state', dummy_observer.get_current_state()
    print "Values: ", str(dummy_learner.values)