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

    while True:
        next_action = learning_algorithm.get_next_action(current_state)
        actor.perform_action(next_action)
        next_state = state_observer.get_current_state()
        reward_given = reward.get_rewards(current_state, next_action, next_state)
        learning_algorithm.receive_reward(current_state, next_action, next_state, reward_given)
        current_state = next_state

if __name__ == '__main__':
    