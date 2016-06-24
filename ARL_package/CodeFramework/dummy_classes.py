__author__ = 'erik'

from StateActionSpace import StateActionSpace
from Actor import Actor
from LearningAlgorithm import LearningAlgorithm
from Reward import Reward
from StateObserver import StateObserver


class DummyStateActionSpace(StateActionSpace):

    def __init__(self):
        self.states = [0, 1, 2, 3]
        self.actions = [7, 4]

    def get_list_of_states(self):
        return self.states

    def get_list_of_actions(self):
        return self.actions

    def get_eligible_actions(self, state):
        if state == self.states[0]:
            return [self.actions[1]]
        else:
            return [self.actions[0]]


class DummyActor(Actor):

    def __init__(self):

        self.a_variable = 1

    def perform_action(self, action):
        self.a_variable += 1
        print "DummyActor performs action " + str(action)


class DummyObserver(StateObserver):

    def __init__(self, state_action_space, dummy_actor):
        assert isinstance(state_action_space, StateActionSpace)
        assert isinstance(dummy_actor, DummyActor)

        self.states = state_action_space.get_list_of_states()
        self.whichState = 0
        self.dummy_actor = dummy_actor

    def get_current_state(self):
        self.whichState = self.dummy_actor.a_variable % 2
        return self.states[self.whichState]


class DummyReward(Reward):

    def __init__(self, state_action_space):
        self.actions = state_action_space.get_list_of_actions()

    def get_rewards(self, state, action, next_state, next_action=None):
        if next_state == (0, 0):
            return 1000
        else:
            return 0


class DummyLearner(LearningAlgorithm):

    def __init__(self, state_action_space):
        assert isinstance(state_action_space, StateActionSpace)

        self.state_action_space = state_action_space
        self.states = state_action_space.get_list_of_states()
        self.actions = state_action_space.get_list_of_actions()

        self.gamma = 0.5
        self.learning_rate = 0.1

        #random initialisation
        self.values = dict()
        self.policy = dict()
        for i, state in enumerate(self.states):
            self.values[state] = 0
            eligible_actions = self.state_action_space.get_eligible_actions(state)
            self.policy[state] = eligible_actions[i % len(eligible_actions)]
        print self.values

    def get_next_action(self, current_state):
        return self.policy[current_state]

    def receive_reward(self, old_state, action, next_state, reward):
        """Do TD return"""

        td_error = reward + self.gamma*self.values[next_state] - self.values[old_state]

        self.values[old_state] += self.learning_rate * td_error

    def finalise_episode(self):
        """
        Update policy greedily, in the dummy example assuming equal transition probabilities
        """
        next_state_deterministic = \
            lambda current_state, action: (current_state[0] + action[0], current_state[1] + action[1])

        for state in self.policy.keys():
            current_next_value = self.values[next_state_deterministic(state, self.policy[state])]

            # find best action
            for action in self.state_action_space.get_eligible_actions(state):
                value_of_next = self.values[next_state_deterministic(state, action)]
                if value_of_next >= current_next_value:
                    self.policy[state] = action
                    current_next_value = value_of_next

        print "DummyLearner: Episode ended, policy updated. Current policy: " + str(self.policy)
        print "DummyLearner: Current values: " + str(self.values)

