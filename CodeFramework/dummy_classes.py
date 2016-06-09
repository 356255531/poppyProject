__author__ = 'erik'

from StateActionSpace import StateActionSpace
from Actor import Actor
from LearningAlgorithm import LearningAlgorithm
from Reward import Reward
from StateObserver import StateObserver


class DummyStateActionSpace(StateActionSpace):

    def __init__(self):
        self.states = [0, 1]
        self.actions = [2, 4]

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
        if action == self.actions[0]:
            return 1
        else:
            return 0


class DummyLearner(LearningAlgorithm):

    def __init__(self, state_action_space):
        assert isinstance(state_action_space, StateActionSpace)

        self.state_action_space = state_action_space
        self.states = state_action_space.get_list_of_states()
        self.actions = state_action_space.get_list_of_actions()

        self.values = [0 for x in self.actions]
        self.gamma = 0.5
        self.learning_rate = 0.1

    def get_next_action(self, current_state):
        return self.state_action_space.get_eligible_actions(current_state)[0]

    def receive_reward(self, old_state, action, next_state, reward):
        """Do TD return"""
        old_state_index = self.states.index(old_state)
        next_state_index = self.states.index(next_state)

        td_error = reward + self.gamma*self.values[next_state_index] - self.values[old_state_index]

        self.values[old_state_index] += self.learning_rate * td_error