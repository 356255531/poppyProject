__author__ = 'Zhiwei Han'
from ..CodeFramework.TrainningWorld import TrainningWorld
from random import randint
from time import sleep

class ProblemVrep(TrainningWorld):
	""" A trainning world of agent and enviroment.
		The main and only object interacts with learning algorithm
		during learning. """
	def __init__(self, stateObserver, actor, reward, stateActionSpace):
		super(ProblemVrep, self).__init__()
		self.stateObserver = stateObserver
		self.actor = actor
		self.reward = reward
		self.stateActionSpace = stateActionSpace

		self.stateSpace = self.stateActionSpace.get_list_of_states()
		self.actionSpace = self.stateActionSpace.get_list_of_actions()
		self.reward = reward

	def get_current_state(self):
		""" Return the current state """
		return self.stateObserver.get_current_state()

	def get_initial_state(self):
		self.actor.initialise_episode()
		return self.get_current_state()

	def get_list_of_states(self):
		return self.stateSpace

	def get_list_of_actions(self):
		return self.actionSpace

	def perform_action(self, action):
		self.actor.perform_action(action)

	def get_reward(self, currentState, action, nextState):
		return self.reward.get_rewards(currentState, action, nextState)

	def is_terminal_state(self, state):
		return self.stateActionSpace.is_terminal_state(state)