__author__ = 'erik'

from ARL_package import CodeFramework, MathematicalClasses
import random


def random_choice(num_choices):
    """Choose uniformly between choices.
    """
    return int(random.random()*num_choices)

dims = (11,11)

gridStateActionSpace = CodeFramework.GridStateActionSpace2D(dims, allow_diag_actions=True)
observer = MathematicalClasses.MathematicalObserver(gridStateActionSpace)
actor = MathematicalClasses.MathematicalActor(observer, greedy_epsilon=0.05)
learningAlgorithm = CodeFramework.dummy_classes.DummyLearner(gridStateActionSpace)
reward = CodeFramework.dummy_classes.DummyReward(gridStateActionSpace)


for i in range(1000):
    CodeFramework.main.run_episode(
        actor, learningAlgorithm, reward, observer, gridStateActionSpace, max_num_iterations=500)