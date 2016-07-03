__author__ = 'ben'

from ARL_package import CodeFramework, VrepClasses, Learning, Rewards, MathematicalClasses

positionMatrix = (5, 3)

# Step 1 - Mathematical Pre-Training
states_actions = CodeFramework.GridStateActionSpace2D(dimensions=positionMatrix, allow_diag_actions=True)
observer = MathematicalClasses.MathematicalObserver(states_actions)
actor = VrepClasses.MathematicalActorExtended(observer, greedy_epsilon=0.1)
reward = Rewards.RewardSimple(1,-10)
learner = Learning.LearningAlgorithmBen(states_actions, reward)

for i in xrange(500):
    CodeFramework.main.run_episode(actor, learner, reward, observer, states_actions, max_num_iterations=100)

print 'Current_state: ', observer.get_current_state()
print "Values: ", str(learner.values)

learner.plot_results()

# Step 2 - Vrep-Simulation
poppy_observer = VrepClasses.ObserverVrep(states_actions, positionMatrix)
poppy_actor = VrepClasses.ActorVrep(poppy_observer)

new_learner = Learning.LearningAlgorithmBen(states_actions, reward, oldData=learner.get_old_data())

for i in range(50):
    CodeFramework.main.run_episode(poppy_actor, learner, reward, poppy_observer, states_actions, max_num_iterations=100)
    
learner.plot_results()

print 'Current_state: ', observer.get_current_state()
print "Values: ", str(learner.values)