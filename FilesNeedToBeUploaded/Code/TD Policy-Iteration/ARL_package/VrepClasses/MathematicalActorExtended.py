__author__ = 'erik' # modified by ben
from .. import CodeFramework # changed this
from .. import MathematicalClasses
import random as rd


class MathematicalActorExtended(CodeFramework.Actor):
    """Deterministic Actor that prints every action it takes"""

    def __init__(self, mathematicalObserver, greedy_epsilon=0):
        assert isinstance(mathematicalObserver, MathematicalClasses.MathematicalObserver)
        self.mathematicalObserver = mathematicalObserver
        self.epsilon = greedy_epsilon

        if greedy_epsilon > 0:  # only import 'random' library if we want epsilon-greedy
            import random
            random.seed()

            def probabilistic_event(probability):
                """ Check if a probabilistic event happens.

                This is calculated from if a uniform random variable in [0,1) is smaller than probability.
                """
                return random.random() < probability

            def random_choice(num_choices):
                """Choose uniformly between choices.
                """
                return int(random.random()*num_choices)

            self.probabilistic_event = probabilistic_event
            self.random_choice = random_choice

    def perform_action(self, action):
        """
        Change state in MathematicalObserver and print

        :param action: tuple
        :return:
        """

        current_state = self.mathematicalObserver.get_current_state()
        eligible_actions = self.mathematicalObserver.state_action_space.get_eligible_actions(current_state)
        if action in eligible_actions:
            if self.epsilon == 0 or not self.probabilistic_event(self.epsilon):
                next_state = (current_state[0] + action[0], current_state[1] + action[1])
                # print "MathematicalActor: Executing policy-action " + str(action) + \
                #      " from " + str(current_state) + " to " + str(next_state)
                self.mathematicalObserver.current_state = next_state
            else:
                num_choices = len(eligible_actions)
                choice = self.random_choice(num_choices)
                random_action = eligible_actions[choice]
                next_state = (current_state[0] + random_action[0], current_state[1] + random_action[1])
                # print "MathematicalActor: Executing epsilon-random action" + str(random_action) + \
                #      " from " + str(current_state) + " to " + str(next_state)
                self.mathematicalObserver.current_state = next_state

        else:
            print "MathematicalActor: From state " + str(current_state) + \
                  ", action " + str(action) + " is not eligible"
            raise ValueError

    def initialise_episode(self):
        """
        Don't need to do anything, really.
        :return:
        """
        self.mathematicalObserver.current_state = rd.choice( self.mathematicalObserver.state_action_space.states )
        pass