import numpy as np
import cv2

# Image Acquisition Algorithm running on 26.05.2016
# REFERENCE:

cap = cv2.VideoCapture(1)
return_value, image = cap.read()
#cv2.imshow( "image", image )
#cv2.waitKey(0)

# http://blog.christianperone.com/2014/06/simple-and-effective-coin-segmentation-using-python-and-opencv/
#http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html?highlight=box2d

### Reading Test Images
#img_list = ['red_card_center_3.jpg', 'red_card_center_4.jpg', 'red_card_center_5.jpg']
#img_list = ['red_card_center.jpg', 'red_card_left.jpg', 'red_card_right.jpg']

#frame = cv2.imread(filename)
frame = image
roi = frame
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)[:,:,1]

gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 1)

kernel = np.ones((2, 2), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                           kernel, iterations=4)

cont_img = closing.copy()
cont_img, contours, hierarchy = cv2.findContours(cont_img, mode = cv2.RETR_EXTERNAL,method = cv2.CHAIN_APPROX_SIMPLE) #http://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html#gsc.tab=0

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 2000 or area > 40000:
        continue

    if len(cnt) < 5:
        continue
    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(roi, ellipse, (0, 255, 0), 2)
    box = cv2.boxPoints(ellipse)
    print (box)
    box_center = np.mean(box, axis=0)
    cv2.drawContours(roi, [np.int0([box_center, box_center, box_center, box_center])], 0, (255, 0, 0), 7)
# cv2.imshow("Morphological Closing", closing)
# cv2.waitKey(0)
# cv2.imshow("Adaptive Thresholding", thresh)
# cv2.waitKey(0)
cv2.imshow('Contours', roi)
cv2.waitKey(0)


