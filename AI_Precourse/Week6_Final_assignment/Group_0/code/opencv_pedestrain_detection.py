"""
Opencv for pedestrian detection

author: Di Wu
email: stevenwudi@gmail.com
"""

import cv2
import numpy as np
import imutils
from imutils.object_detection import non_max_suppression

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)   # capture the video using opencv video capture
while cap.isOpened():
    ret, image = cap.read()
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()
 
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)
 
    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.)
 
    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
 
    # show some information on the number of bounding boxes
    print("[INFO]: {} original boxes, {} after suppression".format(len(rects), len(pick)))
 
    # show the output images
    cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", image)

    k = cv2.waitKey(10)
    if k == 27:
        break
