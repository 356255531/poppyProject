from .. import CodeFramework
from poppy.creatures import PoppyTorso
import time
import numpy as np
import math


class ObserverVrep(CodeFramework.StateObserver):
    """ Use pseudoCV algorithm to observe the agent's current state"""
    def __init__(self, state_action_space, positionMatrix):
        assert isinstance(state_action_space, CodeFramework.GridStateActionSpace2D)  # possibly change to 2DGrid
        self.state_actions_space = state_action_space
        self.poppy = PoppyTorso(simulator='vrep')
        self.io = self.poppy._controllers[0].io
        self.positionMatrix = positionMatrix
        self.max_angle_vert = 18.5 # Default should be: 18.5
        self.max_angle_hori = 37.0 # Default should be 37.0

        # Defining an object that can be tracked
        self.mobile_object_name = 'cube'  # Adding a mobile cube as target
        mobile_object_position = [0, -0.15, 0.85]  # X, Y, Z
        mobile_object_sizes = [0.1, 0.1, 0.1]  # in meters
        mobile_object_mass = 0  # in kg
        self.io.add_cube(self.mobile_object_name, mobile_object_position, mobile_object_sizes, mobile_object_mass)

        time.sleep(1)

        # Defining an object as support for the mobile object to keep it in place
        self.support_object_name = 'cube2'
        support_object_position = [0, -1, 0.5]  # X, Y, Z
        support_object_sizes = [3, 1, 1]  # in meters
        support_object_mass = 0  # in kg

        self.io.add_cube(self.support_object_name, support_object_position, support_object_sizes, support_object_mass)

        self.io.set_object_position('cube', position=[0, -1, 1.05])

    def get_current_state(self):
        """ Return the current state """
        angle = self.get_relative_angles()
        m, n = (np.array(self.positionMatrix) / 2).astype(int)
        if not angle:
            return []
        angle1, angle2 = angle
        x = math.floor(abs(np.sin(angle1 / 180.0 * 3.14159) / np.sin(self.max_angle_hori / 180.0 * 3.14159) * (m + 1)))
        y = math.floor(abs(np.sin(angle2 / 180.0 * 3.14159) / np.sin(self.max_angle_vert / 180.0 * 3.14159) * (n + 1)))
        if angle1 > 0:
            x = -x
        if angle2 < 0:
            y = -y
        return (x, y)

    def __headForwardDirection(self):
        """ Return the vector of camera foward direction """
        angleNegativeY = self.poppy.head_z.present_position
        angleSurfaceXY = - self.poppy.head_y.present_position

        angleNegativeY = angleNegativeY / 180 * 3.14159
        angleSurfaceXY = angleSurfaceXY / 180 * 3.14159

        y = - np.cos(angleSurfaceXY) * np.cos(angleNegativeY)
        x = np.cos(angleSurfaceXY) * np.sin(angleNegativeY)
        z = np.sin(angleSurfaceXY)

        forwardDire = [x, y, z]
        return forwardDire

    def __objectRelPosition(self):
        """ return the relativ positon(vector) of object to camera"""
        objectPos = self.io.get_object_position(self.mobile_object_name)
        positionCameraOri = [0, -0.05, 1.06]  # Camera's position in Vrep

        objectRelPos = [objectPos[i] - positionCameraOri[i] for i in xrange(3)]

        return objectRelPos

    def get_relative_angles(self):
        """ Judge if the object is in sight by calculating if
            the object is out of perspective """
        orthognalBasis1 = self.__headForwardDirection()
        orthognalBasis2 = [orthognalBasis1[1], -orthognalBasis1[0], 0]
        normOrthBasis2 = np.linalg.norm(orthognalBasis2)
        orthognalBasis2 = [orthognalBasis2[i] / normOrthBasis2 for i in xrange(3)]
        orthognalBasis3 = np.cross(orthognalBasis2, orthognalBasis1)

        objectRelPos = self.__objectRelPosition()
        objectProjectionOnOrthBasis1 = np.dot(objectRelPos, orthognalBasis1)
        if objectProjectionOnOrthBasis1 < 0:
            return False
        objectProjectionOnOrthBasis2 = np.dot(objectRelPos, orthognalBasis2)
        objectProjectionOnOrthBasis3 = np.dot(objectRelPos, orthognalBasis3)

        newCoordinate = [objectProjectionOnOrthBasis1, objectProjectionOnOrthBasis2, objectProjectionOnOrthBasis3]

        tt = [1, 0, 0]

        t = [objectProjectionOnOrthBasis1, objectProjectionOnOrthBasis2, 0]
        angle1 = np.arccos(np.dot(tt, t) / np.linalg.norm(t)) / 3.14159 * 180

        if abs(angle1) > self.max_angle_hori:
            return False
        t = [objectProjectionOnOrthBasis1, 0, objectProjectionOnOrthBasis3]
        angle2 = np.arccos(np.dot(tt, t) / np.linalg.norm(t)) / 3.14159 * 180
        if abs(angle2) > self.max_angle_vert:
            return False

        if objectProjectionOnOrthBasis3 < 0 and angle2 > 0:
            angle2 = -angle2

        if objectProjectionOnOrthBasis2 > 0 and angle1 > 0:
            angle1 = -angle1
        return angle1, angle2


if __name__ == '__main__':
    from .. import CodeFramework

    positionMatrix = (5,3)
    state_action_space = CodeFramework.GridStateActionSpace2D(dimensions=positionMatrix, allow_diag_actions=True)

    observer = ObserverVrep(state_action_space, positionMatrix)
    print observer.get_current_state()
