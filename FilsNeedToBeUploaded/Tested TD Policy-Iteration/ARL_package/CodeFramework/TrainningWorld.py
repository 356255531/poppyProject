__author__ = 'Zhiwei Han'

from abc import ABCMeta, abstractmethod

class TrainningWorld(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_current_state(self):
		""" Get the current state """
		pass

	@abstractmethod
	def get_initial_state(self):
		""" Get the initial random state """
		pass

	@abstractmethod
	def get_list_of_states(self):
		""" Return a list of all states"""
		pass

	@abstractmethod
	def get_list_of_actions(self):
		""" Return a dictionary of all states to their actions """
		pass

	@abstractmethod
	def perform_action(self, currentState, action):
		""" Perform actions """
		pass

	@abstractmethod
	def get_reward(self, currentState, action, nextState):
		""" Return the reward of given current state
				and next state """
		pass