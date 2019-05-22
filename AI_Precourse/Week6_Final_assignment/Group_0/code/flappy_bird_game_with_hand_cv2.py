"""
This is the demon program using hand detection/tracking to control a mini game: flappy bird

author: Di Wu
email: stevenwudi@gmail.com
"""

import cv2
from classes.flappy_bird_classes_cv2 import game, frame, hand_pos, hand_convex_number
from classes.hand_detect import detect_hand

track_flag = False  # track flag indicate whether we have a hand detected and start tracking
tracker = cv2.TrackerKCF_create()  # cv2 correlation tracker initialisation

cap = cv2.VideoCapture(0)   # capture the video using opencv video capture

while cap.isOpened():
    ret, img = cap.read()
    if not track_flag:
        count_defects = detect_hand(img, hand_pos)
        if count_defects > hand_convex_number:
            cv2.destroyWindow('Thresholded')

            bbox = (hand_pos[0], hand_pos[1], hand_pos[2] - hand_pos[0], hand_pos[3] - hand_pos[1])
            ok = tracker.init(img, bbox)
            track_flag = True

            # Update tracker
            ok, bbox = tracker.update(img)
            track_pos_prev = [bbox[0] + bbox[2]/2., bbox[1] + bbox[3]/2.]
            # we start the game if there is a hand detected
            game.start(cap, tracker, track_pos_prev)
            frame.start()

    k = cv2.waitKey(1)
    if k == 27:
        break
