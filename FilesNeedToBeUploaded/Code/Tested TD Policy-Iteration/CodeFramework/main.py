__author__ = 'erik'

from . import Actor, LearningAlgorithm, Reward, StateActionSpace, StateObserver


def run_learning(actor, learning_algorithm, reward, state_observer):
    """Run the main loop!"""
    # Check that the variables given have the right superclasses
    assert (isinstance(actor, Actor))
    assert (isinstance(learning_algorithm, LearningAlgorithm))
    assert (isinstance(reward, Reward))
    assert (isinstance(state_observer, StateObserver))

    current_state = state_observer.get_current_state()

    while current_state:
        next_action = learning_algorithm.get_next_action(current_state)
        actor.perform_action(next_action)
        next_state = state_observer.get_current_state()
        reward_given = reward.get_rewards(current_state, next_action, next_state)
        learning_algorithm.receive_reward(current_state, next_action, next_state, reward_given)
        current_state = next_state


def run_episode(actor, learning_algorithm, reward, state_observer, state_action_space, max_num_iterations = 1000000):
    # assert (isinstance(actor, Actor))
    # assert (isinstance(learning_algorithm, LearningAlgorithm))
    # assert (isinstance(reward, Reward))
    # assert (isinstance(state_observer, StateObserver))
    # assert isinstance(state_action_space, StateActionSpace)

    actor.initialise_episode(state_action_space)
    current_state = state_observer.get_current_state()
    current_iter = 0
    while current_iter < max_num_iterations:
        next_action = learning_algorithm.get_next_action(current_state)
        actor.perform_action(next_action)
        next_state = state_observer.get_current_state()
        reward_given = reward.get_rewards(current_state, next_action, next_state)
        learning_algorithm.receive_reward(current_state, next_action, next_state, reward_given)

        current_state = next_state
        current_iter += 1
        if state_action_space.is_terminal_state(current_state):
            reward_given = reward.get_rewards(current_state, (0, 0), next_state)
            learning_algorithm.receive_reward(current_state, (0, 0), next_state, reward_given)
            break

    learning_algorithm.finalise_episode()
    print "run_episode: Episode ended after " + str(current_iter) + " iterations."

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