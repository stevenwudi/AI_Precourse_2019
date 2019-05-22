from sys import platform
import cv2

if platform == "linux" or platform == "linux2":
    # linux
    assert("linux not tested!")
elif platform == "darwin":
    # OS X: because Wudi cannot install pyautogui on my mac--sad
    # https://github.com/msanders/autopy/
    import autopy
elif platform == "win32":
    # Windows...
    import pyautogui

body_pos = [0.5, 0.7, 0.1, 0.25]  # body position, size in relative


class CarCrashGame:
    def __init__(self, cap, tracker):
        self.cap = cap
        self.tracker = tracker
        self.jump_vertical_ratio = 0.015
        self.left_ratio = -0.01
        self.right_ratio = 0.01
        self.track_pos_prev = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def start_game(self, track_pos_prev):
        if platform == "win32":
            pyautogui.moveTo(650, 520)
            pyautogui.click()
            # following is to restart the game
            pyautogui.moveTo(850, 420)
            pyautogui.click()
        elif platform == "darwin":
            autopy.mouse.smooth_move(300, 600)
            autopy.mouse.click()
        self.track_pos_prev = track_pos_prev

    def update(self, track_pos_prev):
        ret, img = self.cap.read()
        self.tracker.update(img)
        pos = self.tracker.get_position()
        track_pos_current = [(pos.left() + pos.right()) / 2., (pos.top() + pos.bottom()) / 2.]
        vertical_ratio = (track_pos_current[1] - track_pos_prev[1]) / img.shape[0]
        horizontal_ratio = (track_pos_current[0] - track_pos_prev[0]) / img.shape[1]
        self.track_pos_prev = track_pos_prev

        print("Vertical ration is %f" % vertical_ratio)
        print("Horitontal ration is %f\n" % horizontal_ratio)
        # if the ratio is larger than jump_vertical_ratio, then it is a jump
        if vertical_ratio > self.jump_vertical_ratio:
            if platform == "win32":
                pyautogui.press('j')
            elif platform == "darwin":
                autopy.key.type_string('j')

            cv2.putText(img, 'J', (50, 50), self.font, 1, (0, 255, 0), 5)
            print('J')

        if horizontal_ratio > self.right_ratio:
            if platform == "win32":
                pyautogui.press('a')
            elif platform == "darwin":
                autopy.key.type_string('a')

            cv2.putText(img, 'A', (50, 50), self.font, 1, (0, 255, 0), 5)
            print('A')

        if horizontal_ratio < self.left_ratio:
            if platform == "win32":
                pyautogui.press('d')
            elif platform == "darwin":
                autopy.key.type_string('d')

        cv2.putText(img, 'D', (50, 50), self.font, 1, (0, 255, 0), 5)
        print('D')

        cv2.rectangle(img, (int(pos.right()), int(pos.bottom())), (int(pos.left()), int(pos.top())),
                      (0, 255, 0), 3)
        cv2.imshow('Body', img)
        cv2.waitKey(1)
