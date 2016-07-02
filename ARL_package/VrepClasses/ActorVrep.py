__author__ = 'ben'

# Import the required python libs
import random as rd
import time

from CodeFramework.Actor import Actor
from ObserverVrep import ObserverVrep		# Import the required modules

class ActorVrep(Actor):
    """Agent in the trainning enviromtn"""
    def __init__(self, observerVrep):
        assert isinstance(observerVrep, ObserverVrep)
        self.observer = observerVrep
        self.positionMatrix = observerVrep.positionMatrix
        self.poppy = observerVrep.poppy
        self.io = observerVrep.io
        self.name = observerVrep.mobile_object_name

    def __motorControl(self, action, motionUnit):
        """ Motor control interface and unexpected to be called outside the class
            action: Head moves left: (-1, 0), right:(0, 1), right-down(1, -1) etc.
            motionUnit: determines amount of rotation
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
        time.sleep(0.5) # increased sleep-time

    def perform_action(self, action):
        """ This function performs the action using the function motorControl """
        motionUnit = 3
        current_state = self.observer.get_current_state()
        time.sleep(0.5)
        eligible_actions = self.observer.state_actions_space.get_eligible_actions(current_state)
        if action in eligible_actions:
            self.__motorControl(action, motionUnit)
        else:
            print "ActorVrep: From state " + str(current_state) + \
                  ", action " + str(action) + " is not eligible"
            raise ValueError

        return True

    def initialise_episode(self):
        """ Initialises a new episode i.e. sets the cube to a new random position """
        self.poppy.head_z.goal_position = 0 # return to start-position in horizontal direction
        self.poppy.head_y.goal_position = rd.choice([-5,-4,-3,-2,-1,0,1,2,3,4]) # vertical head position is randomly chosen
        horizontal_pos = [-0.6, -0.4, -0.2, 0.2, 0.4, 0.6] # possible cube positions in horizontal direction
        cube_position_old = self.io.get_object_position('cube')
        self.io.set_object_position('cube', position=[rd.choice(horizontal_pos), -1, 1.05])
        time.sleep(0.5) # sleep to ensure correct position update
        cube_position_new = self.io.get_object_position('cube')
        currentState = self.observer.get_current_state()
        # The while loop ensures that the cube can be seen at the new position and is not in the same position as before

        while currentState == [] or cube_position_old == cube_position_new:
            self.io.set_object_position('cube', position=[rd.choice(horizontal_pos), -1, 1.05])
            time.sleep(0.5) # sleep to ensure correct position update
            cube_position_new = self.io.get_object_position('cube')
            currentState = self.observer.get_current_state()
        return True

if __name__ == '__main__':
    """ Only for testing - no modification necessary """
    from CodeFramework.GridStateActionSpace import GridStateActionSpace2D

    positionMatrix = (11,5)
    state_action_space = GridStateActionSpace2D(dimensions=positionMatrix, allow_diag_actions=True)

    observer = ObserverVrep(state_action_space, positionMatrix)
    actor = ActorVrep(observer)

    # Testing the method intialise_episode()
    for i in xrange(10):
        actor.initialise_episode()
        print 'New Position cube at: ', observer.io.get_object_position('cube')

    # Testing the method perform_action as well as the implications of get_eligible_actions
    for j in xrange(10):
        curr_state = observer.get_current_state()
        time.sleep(0.5)
        eligible_actions = state_action_space.get_eligible_actions(curr_state)
        act = rd.choice(eligible_actions)
        actor.perform_action(act)
        time.sleep(0.5)
        new_state = observer.get_current_state()
        print 'Initial State: ', curr_state, ', Action: ', act, ' New State: ', new_state
