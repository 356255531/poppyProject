__author__ = 'Zhiwei Han'

class pseudoCV():
    """docstring for pseudoCV"""
    def __init__(self, poppy, io, name, positionMatrix):
        self.poppy = poppy
        self.io = io
        self.name = name
        self.positionMatrix = positionMatrix
        
    def headForwardDirection(self):
        angleNegativeY = self.poppy.head_z.present_position
        angleSurfaceXY = - self.poppy.head_y.present_position

        angleNegativeY = angleNegativeY / 180 * 3.14159
        angleSurfaceXY = angleSurfaceXY / 180 * 3.14159

        y = - np.cos(angleSurfaceXY) * np.cos(angleNegativeY)
        x = np.cos(angleSurfaceXY) * np.sin(angleNegativeY)
        z = np.sin(angleSurfaceXY)

        forwardDire = [x, y, z]
        return forwardDire

    def objectRelPosition(self):
        objectPos = self.io.get_object_position(self.name)
        positionCameraOri = [0, -0.05, 1.06] # Camera's position in Vrep

        objectRelPos = [objectPos[i] - positionCameraOri[i] for i in xrange(3)]

        return objectRelPos

    def canSeeJudge(self):
        orthognalBasis1 = self.headForwardDirection()
        orthognalBasis2 = [orthognalBasis1[1], -orthognalBasis1[0], 0]
        normOrthBasis2 = np.linalg.norm(orthognalBasis2)
        orthognalBasis2 =  [orthognalBasis2[i] / normOrthBasis2 for i in xrange(3) ]
        orthognalBasis3 = np.cross(orthognalBasis2, orthognalBasis1)

        objectRelPos = self.objectRelPosition()
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

    # Output the position of problem
    def getPosition(self):
        angle = self.canSeeJudge()
        m, n = self.positionMatrix
        if not angle:
            return []
        angle1, angle2 = angle
        x = math.ceil(abs(np.sin(angle1 / 180.0 * 3.14159) / np.sin(37 / 180.0 * 3.14159) * m))
        y = math.ceil(abs(np.sin(angle2 / 180.0 * 3.14159) / np.sin(18.5 / 180.0 * 3.14159) * m))
        if angle1 > 0:
            x = -x
        if angle2 < 0:
            y = -y
        return (x, y)
