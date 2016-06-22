__author__ = 'erik'

from Actor import Actor
from LearningAlgorithm import LearningAlgorithm
from Reward import Reward
from StateObserver import StateObserver


def run_learning(actor, learning_algorithm, reward, state_observer):
    """Run the main loop!"""
    # Check that the variables given have the right superclasses
    assert (isinstance(actor, Actor))
    assert (isinstance(learning_algorithm, LearningAlgorithm))
    assert (isinstance(reward, Reward))
    assert (isinstance(state_observer, StateObserver))

    current_state = state_observer.get_current_state()
    i = 1
    while i<= 1000: # changed from while current_state
        next_action = learning_algorithm.get_next_action(current_state)
        actor.perform_action(next_action)
        next_state = state_observer.get_current_state()
        reward_given = reward.get_rewards(current_state, next_action, next_state)
        learning_algorithm.receive_reward(current_state, next_action, next_state, reward_given)
        print 'Loop No. : ', i, 'current state ', current_state, 'action ', next_action, 'next_state ', next_state
        current_state = next_state
        i = i + 1

if __name__ == '__main__':
    from dummy_classes import *

    dummy_states_actions = DummyStateActionSpace()
    dummy_states_actions.states[0] = 2 #because I defined the loop to run while current state wasn't 0/false

    dummy_actor = DummyActor()
    dummy_observer = DummyObserver(dummy_states_actions, dummy_actor)
    dummy_learner = DummyLearner(dummy_states_actions)
    dummy_reward = DummyReward(dummy_states_actions)

    run_learning(dummy_actor, dummy_learner, dummy_reward, dummy_observer)

    print "Values: " + str(dummy_learner.values)