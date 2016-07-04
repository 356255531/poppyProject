__author__ = 'Zhiwei Han'
import numpy as np
import math
import cv2    

class CVAlgorithm(object):
    """ This class returns the current positon by using color detection """
    def __init__(self):
        super(CVAlgorithm, self).__init__()
        
    def takeImage(self):
        """ Take image"""
        def get_image():
            retval, im = camera.read()
            return im

        camera = cv2.VideoCapture(0)
        ramp_frames = 3
        for i in xrange(ramp_frames):
            temp = get_image()
        return temp

    def __getMask(self, image):
        """ Get binary mask of the image """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([115,50,50])
        upper_blue = np.array([125,255,255])

        lower_red = np.array([-10,50,50])
        upper_red = np.array([10,255,255])

        lower_green = np.array([50,50,50])
        upper_green = np.array([70,255,255])

        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)
        maskBlue = cv2.blur(maskBlue,(20,20))
        ret, maskBlue = cv2.threshold(maskBlue,127,255,cv2.THRESH_BINARY)

        maskRed = cv2.inRange(hsv, lower_red, upper_red)
        maskRed = cv2.blur(maskRed,(20,20))
        ret, maskRed = cv2.threshold(maskRed, 127, 255,cv2.THRESH_BINARY)

        return maskRed, maskBlue

    def __getColour(self, maskRed, maskBlue):
        """ detect the color (red or blue)"""
        countRed = sum(sum(1 for i in row if i) for row in maskRed)

        countBlue = sum(sum(1 for i in row if i) for row in maskBlue)

        if countRed > 1000 or countBlue > 1000:
            if countBlue > countRed:
                color = 'Blue'
            else:
                color = 'Red'
            return color
        return False

    def __getCentroid(self, mask):
        """ Calculate the centroid of object"""
        x, y = mask.nonzero()
        x = np.int0(x.mean())
        y = np.int0(y.mean())
        centroid =(x, y)
        return centroid

    def getPosition(self):
        """ Return the centroid position of object """
        image = self.takeImage()
        maskRed, maskBlue = self.__getMask(image)
        cv2.imshow('haha', maskRed)
        cv2.waitKey(0)
        color = self.__getColour(maskRed, maskBlue)
        if not color:
            return ()
        if color == 'Blue':
            centroid = self.__getCentroid(maskBlue)
        else:
            centroid = self.__getCentroid(maskRed)

        centroid = (list(centroid)[1], list(centroid)[0])
        # cv2.drawContours(image, [np.int0([centroid, centroid, centroid, centroid])], 0, (255, 0, 0), 7)
        # cv2.imshow('dd', image)
        # cv2.waitKey(0)
        return (centroid, maskRed.shape)


if __name__ == '__main__':
    cv = CVAlgorithm()
    print cv.getPosition()
