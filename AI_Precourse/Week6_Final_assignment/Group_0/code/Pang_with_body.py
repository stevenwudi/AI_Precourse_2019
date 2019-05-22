"""
This is the demon program using body detection/tracking to control a mini game: Parcour Bear
http://www.4399.com/flash/172170_4.htm
author: Di Wu
email: stevenwudi@gmail.com
"""
import dlib
import cv2
from classes.pang_class import game, frame
from classes.body_detect import detect_body
from classes.car_crash_game import body_pos


tracker = dlib.correlation_tracker()  # dlib correlation tracker initialisation
cap = cv2.VideoCapture(0)   # capture the video using opencv video capture
#PangGame = PangGame(cap, tracker)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while cap.isOpened():
    ret, img = cap.read()
    body_detected, body_pos_detect = detect_body(img, body_pos, hog)
    if body_detected:
        tracker.start_track(img, dlib.rectangle(body_pos_detect[0], body_pos_detect[1], \
                                                body_pos_detect[2], body_pos_detect[3]))
        pos = tracker.get_position()
        track_pos_prev = [(pos.left() + pos.right()) / 2., (pos.top() + pos.bottom()) / 2.]
        # we start the game if there is a hand detected
        game.start_game(cap, tracker, track_pos_prev)
        frame.start()

    k = cv2.waitKey(1)
    if k == 27:
        break
