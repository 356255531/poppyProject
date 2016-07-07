__author__ = 'ben'

from .. import CodeFramework
import random as rd
from matplotlib import pyplot
import numpy as np


class LearningAlgorithmBen(CodeFramework.LearningAlgorithm):
    def __init__( self, state_action_space, Reward, epsilon, gamma, learning_rate, oldData = dict() ):
        assert isinstance(state_action_space, CodeFramework.GridStateActionSpace2D)
        assert isinstance(Reward, CodeFramework.Reward)

        self.figure_count = 1 # if several figures shall be displayed
        self.state_action_space = state_action_space
        self.states = state_action_space.get_list_of_states()
        self.actions = state_action_space.get_list_of_actions()

        """
        if not( (0,0) in self.actions ):
            self.actions.append((0,0))
        """
        self.rewardObj = Reward
        self.epsilon = epsilon
        self.gamma = gamma
        self.learning_rate = learning_rate
        if oldData.has_key('values'):
            self.values = oldData['values']
        else:
            self.values = [0 for x in self.states]  # changed it from self.actions to self.states

        if oldData.has_key('policy'):
            self.policy = oldData['policy']
        else:
            self.policy = [ (0,0) for x in self.states]
            for stat in self.states:
                self.policy[self.states.index(stat)] = self.state_action_space.get_eligible_actions(stat)[0]

        self.frequencies = [dict() for x in self.states]
        for state in self.states:
            state_freq = self.frequencies[self.states.index(state)]
            for action in self.state_action_space.get_eligible_actions(state):
                state_freq.update({action: [[0 for x in self.states], 0]})
        # print self.states
        # print self.frequencies

    def get_old_data(self):
        oldData = dict()
        oldData['values'] = self.values
        oldData['policy'] = self.policy
        return oldData

    def compute_expectation(self, curr_state, freq_dict):
        exp_values_per_actions = [0 for x in self.state_action_space.get_eligible_actions(curr_state)]
        for action in self.state_action_space.get_eligible_actions(curr_state):
            tot_number_counts = freq_dict[action][1]
            freq_per_action = freq_dict[action][0]
            exp_curr_action = 0
            for state in self.states:
                if tot_number_counts != 0:
                    probab_currState_action_state = float(freq_per_action[self.states.index(state)]) / float(tot_number_counts)
                else:
                    probab_currState_action_state = 1/float(len(self.states))
                exp_component = self.rewardObj.get_rewards(curr_state, action, nextState=state) + self.gamma * self.values[self.states.index(state)]
                exp_curr_action += probab_currState_action_state * exp_component
            exp_values_per_actions[self.state_action_space.get_eligible_actions(curr_state).index(action)] = exp_curr_action
        return exp_values_per_actions

    def get_next_action(self, current_state):
        if rd.random() >= self.epsilon:
            # print 'deterministic choice', self.policy[self.states.index(current_state)]
            return self.policy[self.states.index(current_state)]
        else:
            # print 'epsilon-greedy choice'
            return rd.choice(self.state_action_space.get_eligible_actions(current_state))


    def receive_reward(self, old_state, action, next_state, reward):
        """Do TD return"""
        terminal_status = self.state_action_space.is_terminal_state(next_state)

        old_state_index = self.states.index(old_state)
        next_state_index = self.states.index(next_state)

        td_error = reward + self.gamma * self.values[next_state_index] - self.values[old_state_index]

        self.values[old_state_index] += self.learning_rate * td_error
        # Update frequencies ~ probabilities
        self.frequencies[old_state_index][action][0][next_state_index] += 1  # update count of old_state -> action -> next_state
        self.frequencies[old_state_index][action][1] += 1  # update total count of old_state reached

    def finalise_episode(self):
        for state in self.states:
            state_index = self.states.index(state)
            expected_values = self.compute_expectation(state, self.frequencies[state_index])
            self.policy[state_index] = self.state_action_space.get_eligible_actions(state)[expected_values.index(max(expected_values))]
            if not(self.policy[state_index] in self.state_action_space.get_eligible_actions(state)):
                print 'ERROR IN FINALISE EPISODE'
        # print 'policy updated'
        # print self.policy, self.values

    def plot_results(self):
        max_tup_coord = self.state_action_space.max_indices
        min_tup_coord = self.state_action_space.min_indices

        min_x = min_tup_coord[0]
        min_y = min_tup_coord[1]
        max_x = max_tup_coord[0]
        max_y = max_tup_coord[1]

        matr_values = []
        for y in range(min_y, max_y + 1):
            new_row_values = []
            for x in range(min_x, max_x + 1):
                new_row_values.append( self.values[self.states.index((x, -y))] )
            matr_values.append(new_row_values)
        # For Reference see
        # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.matshow
        # http://matplotlib.org/examples/pylab_examples/matshow.html
        VALUES_MAT = np.array(matr_values)
        pyplot.matshow(VALUES_MAT, fignum=self.figure_count, cmap=pyplot.cm.gray)
        pyplot.show()
        self.figure_count += 1
        pass


if __name__ == '__main__':
    from rewardSimple import rewardSimple
    from ActorVrep import ActorVrep
    from ObserverVrep import ObserverVrep
    from MathematicalActor import MathematicalActor
    from MathematicalObserver  import MathematicalObserver
    from CodeFramework.GridStateActionSpace import GridStateActionSpace2D
    from CodeFramework.main import run_learning
    from CodeFramework.main import run_episode
    import numpy as np

    positionMatrix = (5, 3)

    dummy_states_actions = GridStateActionSpace2D(dimensions=positionMatrix,allow_diag_actions=True)
    dummy_observer = MathematicalObserver(dummy_states_actions)
    dummy_actor = MathematicalActor(dummy_observer,greedy_epsilon=0.1)
    dummy_reward = rewardSimple()
    dummy_learner = LearningAlgorithmBen(dummy_states_actions, dummy_reward)

    for i in xrange(500):
        run_episode(dummy_actor, dummy_learner, dummy_reward, dummy_observer, dummy_states_actions, max_num_iterations=100)

    print 'current_state', dummy_observer.get_current_state()
    print "Values: ", str(dummy_learner.values)

    dummy_learner.plot_results()

    poppy_observer = ObserverVrep(dummy_states_actions,positionMatrix)
    poppy_actor = ActorVrep(poppy_observer)

    new_learner = LearningAlgorithmBen(dummy_states_actions, dummy_reward, oldData=dummy_learner.get_old_data())

    for i in range(50):
        run_episode(poppy_actor, dummy_learner, dummy_reward, poppy_observer, dummy_states_actions, max_num_iterations=100)
    dummy_learner.plot_results()

    print 'current_state', dummy_observer.get_current_state()
    print "Values: ", str(dummy_learner.values)