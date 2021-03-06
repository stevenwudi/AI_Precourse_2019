"""
This is the demon program using hand detection/tracking to control a mini game: flappy bird

author: Di Wu
email: stevenwudi@gmail.com
"""

import dlib
import cv2
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from classes.flappy_bird_classes import draw, game, frame
from classes.flappy_bird_classes import width, height, hand_pos, hand_convex_number
from classes.hand_detect import detect_hand

track_flag = False  # track flag indicate whether we have a hand detected and start tracking
tracker = dlib.correlation_tracker()  # dlib correlation tracker initialisation

cap = cv2.VideoCapture(0)   # capture the video using opencv video capture

while cap.isOpened():
    ret, img = cap.read()
    if not track_flag:
        count_defects = detect_hand(img, hand_pos)
        if count_defects > hand_convex_number:
            cv2.destroyWindow('Thresholded')
            tracker.start_track(img, dlib.rectangle(hand_pos[0], hand_pos[1], hand_pos[2], hand_pos[3]))
            track_flag = True
            pos = tracker.get_position()
            track_pos_prev = [(pos.left() + pos.right()) / 2., (pos.top() + pos.bottom()) / 2.]
            # we start the game if there is a hand detected
            game.start(cap, tracker, track_pos_prev)
            frame.start()

    k = cv2.waitKey(1)
    if k == 27:
        break
