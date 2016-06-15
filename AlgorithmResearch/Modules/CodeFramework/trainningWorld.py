__author__ = 'Zhiwei Han'

from abc import ABCMeta, abstractmethod

class trainningWorld(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def getCurrentState(self):
		""" Get the current state """
		pass

	@abstractmethod
	def getInitialState(self):
		""" Get the initial random state """
		pass

	@abstractmethod
	def getStateSpace(self):
		""" Return a list of all states"""
		pass

	@abstractmethod
	def getActionSpace(self):
		""" Return a dictionary of all states to their actions """
		pass

	@abstractmethod
	def takeAction(self, currentState, action):
		""" Perform actions """
		pass

	@abstractmethod
	def getReward(self, currentState, action, nextState):
		""" Return the reward of given current state
				and next state """
		pass