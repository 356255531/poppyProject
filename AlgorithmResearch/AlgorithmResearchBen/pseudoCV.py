__author__ = 'ben'
# changes:
# Added extension for random cube position, if state (0,0) was reached [lines 92-97]
import numpy as np
import math
import random as rd1

class pseudoCV(object):
    """ This class returns the current positon of poppy in Vrep
    within a math way """
    def __init__(self, poppy, io, name, positionMatrix):
        self.poppy = poppy
        self.io = io
        self.name = name
        self.positionMatrix = positionMatrix
        
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
        objectPos = self.io.get_object_position(self.name)
        positionCameraOri = [0, -0.05, 1.06] # Camera's position in Vrep

        objectRelPos = [objectPos[i] - positionCameraOri[i] for i in xrange(3)]

        return objectRelPos

    def __canSeeJudge(self):
        """ Judge if the object is in sight by calculating if
            the object is out of perspective """
        orthognalBasis1 = self.__headForwardDirection()
        orthognalBasis2 = [orthognalBasis1[1], -orthognalBasis1[0], 0]
        normOrthBasis2 = np.linalg.norm(orthognalBasis2)
        orthognalBasis2 =  [orthognalBasis2[i] / normOrthBasis2 for i in xrange(3) ]
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

        if abs(angle1) > 37:
            return False
        t = [objectProjectionOnOrthBasis1, 0, objectProjectionOnOrthBasis3]
        angle2 = np.arccos(np.dot(tt, t) / np.linalg.norm(t)) / 3.14159 * 180
        if abs(angle2) > 18.5:
            return False
        
        if objectProjectionOnOrthBasis3 < 0 and angle2 > 0:
            angle2 = -angle2

        if objectProjectionOnOrthBasis2 > 0 and angle1 > 0:
            angle1 = -angle1
        return angle1, angle2

    def getPosition(self):
        """ Return the position of centorid in state matrix
            if object out of perspective return () """
        angle = self.__canSeeJudge()
        m, n = self.positionMatrix
        if not angle:
            return []
        angle1, angle2 = angle
        x = math.floor(abs(np.sin(angle1 / 180.0 * 3.14159) / np.sin(37 / 180.0 * 3.14159) * (m + 1)))
        y = math.floor(abs(np.sin(angle2 / 180.0 * 3.14159) / np.sin(18.5 / 180.0 * 3.14159) * (n + 1)))
        if angle1 > 0:
            x = -x
        if angle2 < 0:
            y = -y
        # extension:
        # if (x,y) == (0,0):
            # rd_hor = rd1.choice([-0.6, -0.3, 0.3, 0.6])
            # self.io.set_object_position('cube', position=[rd_hor, -1, 1.05])
            # print 'position updated', rd_hor
        # end of extension
        return (x, y)

if __name__ == '__main__':
    print math.floor(abs(np.sin(36 / 180.0 * 3.14159) / np.sin(37 / 180.0 * 3.14159) * 26))