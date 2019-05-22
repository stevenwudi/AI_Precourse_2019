import cv2
import numpy as np
import math
import imutils
from imutils.object_detection import non_max_suppression

from sys import platform

if platform == "linux" or platform == "linux2":
    # linux
    assert ("linux not tested!")
elif platform == "darwin":
    # OS X: because Wudi cannot install pyautogui on my mac--sad
    # https://github.com/msanders/autopy/
    import autopy
elif platform == "win32":
    # Windows...
    import pyautogui


def detect_body(img, body_pos, hog, overlap_ratio=0.3):
    '''
    detect hand using opencv convex hull
    :param img:
    :param hand_pos:
    :return:
    '''
    #img = imutils.resize(img, width=min(400, img.shape[1]))

    body_pos_rect = [body_pos[0]-body_pos[2], body_pos[1]-body_pos[3], body_pos[0]+body_pos[2], body_pos[1]+body_pos[3]]
    body_pos_img = (int(body_pos_rect[0]*img.shape[1]), int(body_pos_rect[1]*img.shape[0]),\
                    int(body_pos_rect[2]*img.shape[1]), int(body_pos_rect[3]*img.shape[0]))
    area = (body_pos_img[2]- body_pos_img[0]) * (body_pos_img[3]-body_pos_img[0])

    cv2.rectangle(img, (body_pos_img[0], body_pos_img[1]), (body_pos_img[2], body_pos_img[3]), (0, 255, 0), 0)
    crop_img = img[body_pos_img[1]:body_pos_img[3], body_pos_img[0]:body_pos_img[2]]

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.05)
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.)

    if platform == "linux" or platform == "linux2":
        # linux
        assert ("linux not tested!")
    elif platform == "darwin":
        # OS X: because Wudi cannot install pyautogui on my mac--sad
        cv2.namedWindow('Body')
        cv2.moveWindow('Body', 800, 210)

        cv2.namedWindow('Croped')
        cv2.moveWindow('Croped', 800, 100 - crop_img.shape[1])

        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(img, (xA, yA), (xB, yB), (255, 255, 0), 2)

        cv2.imshow('Body', img)
        cv2.imshow('Hand', crop_img)

    elif platform == "win32":
        # Windows...
        cv2.namedWindow('Body')
        cv2.moveWindow('Body', 2000, 210)

        cv2.namedWindow('Croped')
        cv2.moveWindow('Croped', 2000, 200 - crop_img.shape[0])

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img, (xA, yA), (xB, yB), (255, 255, 0), 2)

    cv2.imshow('Body', img)
    cv2.imshow('Croped', crop_img)

    # draw the final bounding boxes
    if len(pick) > 0:
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            crop_img = img[yA:yB, xA:xB]

            #overlap = (body_pos_img[0], body_pos_img[1]), (body_pos_img[2], body_pos_img[3])
            xx1 = max(body_pos_img[0], xA)
            yy1 = max(body_pos_img[1], yA)
            xx2 = min(body_pos_img[2], xB)
            yy2 = min(body_pos_img[3], yB)
            overlap = float((yy2-yy1)*(xx2-xx1)) /area
            if overlap > overlap_ratio:
                cv2.imshow('Body', img)
                cv2.imshow('Croped', crop_img)
                #cv2.waitKey(0)
                return True, [xx1, yy1, xx2, yy2]

    return False, []

