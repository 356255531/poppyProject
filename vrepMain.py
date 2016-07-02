__author__ = 'ben'

from ARL_package import CodeFramework, VrepClasses, Learning, Rewards, MathematicalClasses

positionMatrix = (5, 3)

# Step 1 - Mathematical Pre-Training
dummy_states_actions = CodeFramework.GridStateActionSpace2D(dimensions=positionMatrix, allow_diag_actions=True)
dummy_observer = MathematicalClasses.MathematicalObserver(dummy_states_actions)
dummy_actor = VrepClasses.MathematicalActorExtended(dummy_observer, greedy_epsilon=0.1)
dummy_reward = Rewards.RewardSimple(1,-10)
dummy_learner = Learning.LearningAlgorithmBen(dummy_states_actions, dummy_reward)

for i in xrange(500):
    CodeFramework.main.run_episode(dummy_actor, dummy_learner, dummy_reward, dummy_observer, dummy_states_actions, max_num_iterations=100)

print 'current_state', dummy_observer.get_current_state()
print "Values: ", str(dummy_learner.values)

dummy_learner.plot_results()

# Step 2 - Vrep-Simulation
poppy_observer = VrepClasses.ObserverVrep(dummy_states_actions, positionMatrix)
poppy_actor = VrepClasses.ActorVrep(poppy_observer)

new_learner = Learning.LearningAlgorithmBen(dummy_states_actions, dummy_reward, oldData=dummy_learner.get_old_data())

for i in range(50):
    CodeFramework.main.run_episode(poppy_actor, dummy_learner, dummy_reward, poppy_observer, dummy_states_actions, max_num_iterations=100)
dummy_learner.plot_results()

print 'current_state', dummy_observer.get_current_state()
print "Values: ", str(dummy_learner.values)