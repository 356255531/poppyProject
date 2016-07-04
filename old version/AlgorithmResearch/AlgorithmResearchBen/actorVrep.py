__author__ = 'ben'

import itertools					# Import the neccesary python libs
import random as rd
import time
import numpy as np

from pseudoStateObserver import pseudoStateObserver		# Import the required modules
from CodeFramework.Actor import Actor

class actorVrep(pseudoStateObserver, Actor):
    """Agent in the trainning enviromtn"""
    def __init__(self, poppy, io, name, positionMatrix):
        super(actorVrep, self).__init__(poppy, io, name, positionMatrix)
        self.positionMatrix = positionMatrix	#  The state size (2 * positionMatrix[0] + 1) * (2 * positionMatrix[1] + 1)
        self.poppy = poppy 			# The virtual poppy in Vrep
        self.io = io 				# The object interacting interface in Vrep
        self.name = name 			# The object name in Vrep

    def __motorControl(self, action, motionUnit):
        """ Motor control interface and unexpected to be called outside the class
            action: Head moves left: (-1, 0), right:(0, 1), rightdown(1, -1) etc.
            motionUnit: used to accelerate or slow down the movement
            """
        m, n = action
        angleY = self.poppy.head_y.present_position
        angleZ = self.poppy.head_z.present_position
        if m != 0 and n != 0:
            m = m / abs(m)
            n = n / abs(n)
            self.poppy.head_z.goal_position = angleZ + 1.5 * motionUnit * m
            self.poppy.head_y.goal_position = angleY + 1 * motionUnit * n
        if m != 0 and n == 0:
            m = m / abs(m)
            self.poppy.head_z.goal_position = angleZ + 1.5 * motionUnit * m
        if m == 0 and n != 0:
            n = n / abs(n)
            self.poppy.head_y.goal_position = angleY + 1 * motionUnit * n
        time.sleep(0.3) # increased sleep-time

    def perform_action(self, action):
        """ This function performs the action using the function motorControl """
        motionUnit = 1
        self.__motorControl(action, motionUnit)
        return True

    def initialise_episode(self):
        """ Initialises a new episode i.e. sets the cube to a new random position """
        self.poppy.head_z.goal_position = 0 # return to start-position in horizontal direction
        self.poppy.head_y.goal_position = rd.choice([-5,-4,-3,-2,-1,0,1,2,3,4]) # vertical head position is randomly chosen
        horizontal_pos = [-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6] # possible cube positions in horizontal direction
        cube_position_old = self.io.get_object_position('cube')
        self.io.set_object_position('cube', position=[rd.choice(horizontal_pos), -1, 1.05])
        time.sleep(0.5) # sleep to ensure correct position update
        cube_position_new = self.io.get_object_position('cube')
        currentState = super(actorVrep, self).get_current_state()
        # The while loop ensures that the cube can be seen at the new position and is not in the same position as before
        while currentState == [] or cube_position_old == cube_position_new:
            self.io.set_object_position('cube', position=[rd.choice(horizontal_pos), -1, 1.05])
            time.sleep(0.5) # sleep to ensure correct position update
            cube_position_new = self.io.get_object_position('cube')
            currentState = super(actorVrep, self).get_current_state()
        return True

    def __perform_action_old(self, action):
        # this function is no longer used
        """ Use closed loop control to move the agent to the next corresponding state.
            For definition of action see self.__motorControl.
            When no obect in sight, return False. """
        if action == (0, 0):
            return 'action illegal'
        currentState = super(actorVrep, self).get_current_state()
        if len(list(currentState)) == 0:
            return False

        x, y = currentState
        diffX, diffY = action
        goalX, goalY = x + diffX, y + diffY
        count = 0
        while (x != goalX or y != goalY) and count < 20:
            actionX = goalX - x
            actionY = goalY - y
            a = max((abs(actionX) * 1.5) // 5, 1)
            b = max(abs(actionY) // 5, 1)
            motionUnit = min(a, b)
            self.__motorControl((actionX, actionY), motionUnit)

            currentState = super(actorVrep, self).get_current_state()
            if len(list(currentState)) == 0:
                return False

            x, y = currentState
            count += 1
        return True

    def __randMove_old(self, stateSpace):
        # this function is no longer used
        """ Agent moves to a random state by being given state space """
        while len(list(super(actorVrep, self).get_current_state())) == 0:
            list1 = np.arange(-self.positionMatrix[0], self.positionMatrix[0])
            list2 = np.arange(-self.positionMatrix[1], self.positionMatrix[1])
            motionSpace = [(i, j) for i, j in itertools.product(list1, list2)]
            motionSpace.remove((0, 0))
            self.perform_action(motionSpace[rd.randint(0, len(motionSpace) - 1)])

        initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
        while initialState == (0, 0):
            initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]

        x, y = super(actorVrep, self).get_current_state()
        initialX, initialY = initialState
        diffX, diffY = int(initialX - x), int(initialY - y)

        while not self.perform_action((diffX, diffY)):
            initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]
            while initialState == (0, 0):
                initialState = stateSpace[rd.randint(0, len(stateSpace) - 1)]

            x, y = super(actorVrep, self).get_current_state()
            initialX, initialY = initialState
            diffX, diffY = int(initialX - x), int(initialY - y)
            self.perform_action((diffX, diffY))

if __name__ == '__main__':
    """ Only for testing - no modification necessary """
    from poppy.creatures import PoppyTorso
    import numpy as np
    import time
    import math
    from CodeFramework.GridStateActionSpace import GridStateActionSpace2D
    poppy = PoppyTorso(simulator='vrep')

    io = poppy._controllers[0].io
    name = 'cube'
    position = [0, -0.15, 0.85] # X, Y, Z
    sizes = [0.1, 0.1, 0.1] # in meters
    mass = 0 # in kg
    io.add_cube(name, position, sizes, mass)
    time.sleep(1)
    name1 = 'cube2'
    position1 = [0, -1, 0.5]
    sizes1 = [3, 1, 1]
    io.add_cube(name1, position1, sizes1, mass)
    io.set_object_position('cube', position=[0, -1, 1.05])
    positionMatrix = (25, 20)

    a = actorVrep(poppy, io, name, positionMatrix)
    b = GridStateActionSpace2D(dimensions = positionMatrix, allow_diag_actions=True)
    c = pseudoStateObserver(poppy, io, name, positionMatrix)
    print 'current State Before action', c.get_current_state()

    print 'next state after action', c.get_current_state()

    """
    for i in xrange(10):
        a.initialise_episode()
        print 'New Position cube at: ', io.get_object_position('cube')
    """

    a.perform_action((0, 1))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((0, -1))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((1, 1))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((1, -1))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((1, 0))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((-1, 0))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((-1, 1))
    time.sleep(1)
    print c.get_current_state()
    a.perform_action((-1, -1))
    time.sleep(1)
    print c.get_current_state()