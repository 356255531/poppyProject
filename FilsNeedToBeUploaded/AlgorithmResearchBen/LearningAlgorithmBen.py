__author__ = 'ben'

from CodeFramework.StateActionSpace import StateActionSpace
from CodeFramework.Actor import Actor
from CodeFramework.LearningAlgorithm import LearningAlgorithm
from CodeFramework.Reward import Reward
from CodeFramework.StateObserver import StateObserver
import random as rd
from matplotlib import pyplot
import numpy as np
 

class LearningAlgorithmBen(LearningAlgorithm):
    def __init__(self, state_action_space, Reward, oldData = dict()):
        assert isinstance(state_action_space, StateActionSpace)

        self.figure_count = 1
        self.state_action_space = state_action_space
        self.states = state_action_space.get_list_of_states()
        self.actions = state_action_space.get_list_of_actions()
        if not( (0,0) in self.actions ):
            self.actions.append((0,0))
        self.rewardObj = Reward
        self.epsilon = 0.1
        if oldData.has_key('values'):
            self.values = oldData['values']
        else:
            self.values = [0 for x in self.states]  # changed it from self.actions to self.states

        self.gamma = 0.7
        self.learning_rate = 0.3
        if oldData.has_key('policy'):
            self.policy = oldData['policy']
        else:
            self.policy = [ (0,0) for x in self.states]
            for stat in self.states:
                print 'state', stat
                print 'action', self.actions
                self.policy[self.states.index(stat)] = self.state_action_space.get_eligible_actions(stat)[0]

        self.frequencies = [dict() for x in self.states]
        for state in self.states:
            state_freq = self.frequencies[self.states.index(state)]
            for action in self.state_action_space.get_eligible_actions(state):
                state_freq.update({action: [[0 for x in self.states], 0]})
        print self.states
        print self.frequencies

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
                td_error = self.rewardObj.get_rewards(curr_state, action, nextState=state, problemType='capture') + self.gamma * self.values[self.states.index(state)]
                exp_curr_action += probab_currState_action_state * td_error
            exp_values_per_actions[self.state_action_space.get_eligible_actions(curr_state).index(action)] = exp_curr_action
        # print "curr_state: ", curr_state, "freq_dict: ", freq_dict
        # print "expected Values per action: ",  exp_values_per_actions
        return exp_values_per_actions

    def get_next_action(self, current_state):
        print 'state', current_state
        if rd.random() >= 0.1:
            # print 'deterministic choice', self.policy[self.states.index(current_state)]
            print 'action', self.policy[self.states.index(current_state)]
            return self.policy[self.states.index(current_state)]
        else:
            # print 'epsilon-greedy choice'
            a = rd.choice(self.state_action_space.get_eligible_actions(current_state))
            print 'action', a
            return a
            # return rd.choice(self.state_action_space.get_eligible_actions(current_state))


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
        # print('finalise episode')
        # Update policy
        # if self.global_counter == self.max_number_iterations:
        for state in self.states:
            state_index = self.states.index(state)
            expected_values = self.compute_expectation(state, self.frequencies[state_index])
            self.policy[state_index] = self.state_action_space.get_eligible_actions(state)[expected_values.index(max(expected_values))]
            if not(self.policy[state_index] in self.state_action_space.get_eligible_actions(state)):
                print 'ERROR IN FINALISE EPISODE'
        # print 'policy updated'
        print self.policy, self.values
        # self.plot_results()

    def plot_results(self):
        max_tup_coord = max(self.states)
        min_tup_coord = min(self.states)

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
        # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.matshow
        # http://matplotlib.org/examples/pylab_examples/matshow.html
        VALUES_MAT = np.array(matr_values)
        pyplot.matshow(VALUES_MAT, fignum=self.figure_count, cmap=pyplot.cm.gray)
        pyplot.show()
        self.figure_count += 1
        pass


if __name__ == '__main__':
    from rewardSimple import rewardSimple
    from actorVrep import actorVrep
    from pseudoStateObserver import pseudoStateObserver
    from MathematicalActor import MathematicalActor
    from MathematicalObserver  import MathematicalObserver
    from CodeFramework.GridStateActionSpace import GridStateActionSpace2D
    from CodeFramework.main import run_learning
    from CodeFramework.main import run_episode
    from LearningAlgorithmBen import LearningAlgorithmBen
    import numpy as np
    import time
    import math

    """
    from poppy.creatures import PoppyTorso


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
    """


    positionMatrix = (5, 3)

    dummy_states_actions = GridStateActionSpace2D(dimensions=positionMatrix,allow_diag_actions=True)

    # dummy_observer = pseudoStateObserver(poppy, io, name, positionMatrix)
    dummy_observer = MathematicalObserver(dummy_states_actions)
    # dummy_actor = actorVrep(poppy, io, name, positionMatrix)
    dummy_actor = MathematicalActor(dummy_observer,greedy_epsilon=0.1)
    dummy_reward = rewardSimple()
    dummy_learner = LearningAlgorithmBen(dummy_states_actions, dummy_reward)

    # run_learning(dummy_actor, dummy_learner, dummy_reward, dummy_observer)
    for i in xrange(500):
        run_episode(dummy_actor, dummy_learner, dummy_reward, dummy_observer, dummy_states_actions, max_num_iterations=100)

    print 'current_state', dummy_observer.get_current_state()
    print "Values: ", str(dummy_learner.values)

    dummy_learner.plot_results()

    # from poppy.creatures import PoppyTorso

    # poppy = PoppyTorso(simulator='vrep')

    # io = poppy._controllers[0].io
    # name = 'cube'
    # position = [0, -0.15, 0.85]  # X, Y, Z
    # sizes = [0.1, 0.1, 0.1]  # in meters
    # mass = 0  # in kg
    # io.add_cube(name, position, sizes, mass)
    # time.sleep(1)
    # name1 = 'cube2'
    # position1 = [-0.4, -1, 0.5]
    # sizes1 = [3, 1, 1]
    # io.add_cube(name1, position1, sizes1, mass)
    # io.set_object_position('cube', position=[0, -1, 1.05])
    from ARL_package.PoppyClasses import actorPoppy, CVStateObserver
    import pypot.dynamixel

    ports = pypot.dynamixel.get_available_ports()
    print('available ports:', ports)

    port = ports[0]
    print('Using the first on the list', port)

    dxl_io = pypot.dynamixel.DxlIO(port)
    print('Connected!')

    poppy_observer = CVStateObserver(positionMatrix)
    poppy_actor = actorPoppy(dxl_io,positionMatrix)

    new_learner = LearningAlgorithmBen(dummy_states_actions, dummy_reward, oldData=dummy_learner.get_old_data())

    for i in range(50):
        run_episode(poppy_actor, dummy_learner, dummy_reward, poppy_observer, dummy_states_actions, max_num_iterations=100)
        time.sleep(3)
    dummy_learner.plot_results()

    print 'current_state', dummy_observer.get_current_state()
    print "Values: ", str(dummy_learner.values)

