from sys import platform

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
import cv2
hand_pos = [250, 300, 350, 400]  # hand position
hand_convex_number = 2


class ParcourBearGame:
    def __init__(self, cap, tracker):
        self.cap = cap
        self.tracker = tracker
        self.jump_vertical_ratio = 0.008

    def init_parcour_game(self):
        if platform == "win32":
            pyautogui.moveTo(850, 770, 2, pyautogui.easeInQuad)
            pyautogui.click()
            pyautogui.moveTo(800, 600, 2, pyautogui.easeInQuad)
            pyautogui.click()
        elif platform == "darwin":
            autopy.mouse.smooth_move(800, 600)
            autopy.mouse.click()


    def start_game(self, track_pos_prev):
        if platform == "win32":
            pyautogui.moveTo(450, 870, 2, pyautogui.easeInQuad)
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
        vertical_ratio = (track_pos_current[1] - track_pos_prev[1]) / img.shape[1]
        self.track_pos_prev = track_pos_prev
        # we add the velocity is propotional to the hand motion function
        self.flap_up_velocity = vertical_ratio / self.jump_vertical_ratio * 1

        print("Vertical ration is %f" % vertical_ratio)
        # if the ratio is larger than jump_vertical_ratio, then it is a jump
        if vertical_ratio > self.jump_vertical_ratio:
            if platform == "win32":
                pyautogui.click()
            elif platform == "darwin":
                autopy.mouse.click()

        cv2.rectangle(img, (int(pos.right()), int(pos.bottom())), (int(pos.left()), int(pos.top())),
                      (255, 0, 0), 0)
        cv2.imshow('Gesture', img)
        cv2.waitKey(1)
