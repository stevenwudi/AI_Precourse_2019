# Pang game
# Ender Kasim December 2013
# All images except the hero sprite are done by me
# Hero sprite is under CC BY SA license from http://lpc.opengameart.org/
# Arrow sound is from www.freesound.org user gezortenplotz
# Pop sound is from soundbible.com user Mark DiAngelo
# The music is "Moduless" by Paza http://freemusicarchive.org/music/Paza/

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# Global Constants

WIDTH = 600
HEIGHT = 400
GRAVITY = 0.1
FRICTION = 0.001
ANIM_SPEED = 5

# Time Limit for each level
TIME_LIMIT = {1: 600, 2: 600, 3: 600, 4: 600, 5: 550,
              6: 550, 7: 550, 8: 550, 9: 500, 10: 500}
# Bubble spawns for each level: Level 1 has 1 size 2 bubble
# Level 5 has 2 size 3.05 bubbles
BUBBLES = {1: [1, 2], 2: [2, 2], 3: [1, 3.05], 4: [3, 2], 5: [4, 2],
           6: [2, 3.05], 7: [1, 4.1], 8: [5, 2], 9: [3, 3.05], 10: [2, 4.1]}

# Global Lists and variables

bubble_list = []
sphere_image = []
harpoon_fired = False
lives = 5
score = 0
current_level = 0
time = 0
message = "GET READY"
mess_age = 0
in_play = False


# Image class
class Image:
    def __init__(self, image_file, center, size, radius=0, lifespan=0, animated=False, tiles=1):
        self.image = simplegui._load_local_image(image_file)
        self.center = center
        self.size = size
        self.radius = radius
        self.tiles = tiles
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_image(self):
        return self.image

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    def get_tiles(self):
        return self.tiles


PREFIX = './image/Pang/'

SOUND_DIR = './sound/Pang/'
# Images
bg_image = Image(PREFIX + "HfReHl5.jpg", [300, 200], [600, 400])
harpoon_image = Image(PREFIX + "VCC6wZL.png", [2, 200], [5, 400], 5, 120, True, 2)
hero_image = Image(PREFIX + "9v5ehnO.png", [32, 32], [64, 64], 25, 0, True, 9)

# Sphere Images in a list.
sphere_image.append(Image(PREFIX + "FDqGDmc.png", [37, 37], [75, 75], 37))
sphere_image.append(Image(PREFIX + "NljADnB.png", [37, 37], [75, 75], 37))
sphere_image.append(Image(PREFIX + "Nl5u05O.png", [37, 37], [75, 75], 37))
sphere_image.append(Image(PREFIX + "IHXoEES.png", [37, 37], [75, 75], 37))
sphere_image.append(Image(PREFIX + "pX44tkA.png", [37, 37], [75, 75], 37))
sphere_image.append(Image(PREFIX + "LdTCEUo.png", [37, 37], [75, 75], 37))
sphere_image.append(Image(PREFIX + "Vlt8FBC.png", [37, 37], [75, 75], 37))

# Sounds
# sounds needs to be .wav format
pop_sound = simplegui._load_local_sound(SOUND_DIR + "pop.wav")
arrow_sound = simplegui._load_local_sound(SOUND_DIR + "arrow.wav")
soundtrack = simplegui._load_local_sound(SOUND_DIR + "paza-moduless.wav")
soundtrack.set_volume(0.3)


# Classes
# Sprite class with rectangular collision, scaling, gravity
# and friction properities.
class Sprite:
    def __init__(self, image, pos, vel, scale=1):
        self.image = image.get_image()
        self.pos = pos
        self.vel = vel
        self.size = image.get_size()
        self.center = image.get_center()
        self.scaled_size = self.scale_size(image.get_size(), scale)
        self.scaled_center = self.scale_size(image.get_center(), scale)
        self.radius = image.get_radius() * scale
        self.lifespan = image.get_lifespan()
        self.animated = image.get_animated()
        self.tiles = image.get_tiles()
        self.age = 0
        self.kill = False
        self.physics = True
        self.scale = scale

    def get_scale(self):
        return self.scale

    def scale_size(self, vector, scale):
        return [int(vector[0] * scale), int(vector[1] * scale)]

    def get_pos(self):
        return self.pos

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_kill(self):
        return self.kill

    def set_physics(self, physics):
        self.physics = physics

    def collide(self, obj):
        crit_x_dist = self.scaled_size[0] / 2 + obj.get_size()[0] / 2
        pos_x_diff = math.fabs(self.pos[0] - obj.get_pos()[0])
        crit_y_dist = self.scaled_size[1] / 2 + obj.get_size()[1] / 2
        pos_y_diff = math.fabs(self.pos[1] - obj.get_pos()[1])
        if pos_x_diff < crit_x_dist and pos_y_diff < crit_y_dist:
            return True
        else:
            return False

    def update(self):
        self.age += 1
        if self.age == self.lifespan:
            self.kill = True
        self.pos = list_add(self.pos, self.vel)
        if self.physics:
            self.vel[1] += GRAVITY
            self.vel[1] *= (1 - FRICTION)
            if self.pos[1] > HEIGHT - self.radius:
                self.vel[1] *= -1
            if self.pos[0] < self.radius or self.pos[0] > WIDTH - self.radius:
                self.vel[0] *= -1

    def draw(self, canvas):
        self.tile_center = list_add(self.center, [(((self.age // ANIM_SPEED) % self.tiles) * self.size[0]) / 2, 0])
        canvas.draw_image(self.image, self.tile_center, self.size, self.pos, self.scaled_size)


# Hero class with harpoon shooting ability.
class Hero:
    def __init__(self, image, pos):
        self.image = image.get_image()
        self.pos = pos
        self.vel = [0, 0]
        self.size = image.get_size()
        self.radius = image.get_radius()
        self.center = image.get_center()
        self.launch = False
        self.age = 0
        self.tiles = image.get_tiles()

    def get_pos(self):
        return self.pos

    def get_size(self):
        return [self.size[0] * 0.5, self.size[1] * 0.7]

    def set_vel(self, amount):
        self.vel[0] += amount
        self.age = 0
        self.launch = False

    def shoot(self):
        global harpoon_fired, harpoon
        harpoon_fired = True
        self.launch = True
        self.age = 0
        harpoon_vel = [0, -6]
        harpoon_pos = [self.pos[0], self.pos[1] + harpoon_image.get_center()[1] / 2]
        harpoon = Sprite(harpoon_image, harpoon_pos, harpoon_vel)
        harpoon.set_physics(False)
        arrow_sound.rewind()
        arrow_sound.play()

    def update(self):
        if self.pos[0] + self.vel[0] > self.size[0] / 5 and self.pos[0] + self.vel[0] < WIDTH - self.size[0] / 5:
            self.pos = list_add(self.pos, self.vel)

    def draw(self, canvas):
        if self.vel[0] > 0:
            tile_center = list_add(self.center, [(self.age // ANIM_SPEED) * self.size[0], 2 * self.size[1]])
        elif self.vel[0] < 0:
            tile_center = list_add(self.center, [(self.age // ANIM_SPEED) * self.size[0], 1 * self.size[1]])
        elif self.vel[0] == 0 and self.launch:
            tile_center = list_add(self.center, [(self.age // ANIM_SPEED) * self.size[0], 0 * self.size[1]])
            if self.age == (self.tiles * ANIM_SPEED) - 1:
                self.launch = False
        else:
            tile_center = self.center

        canvas.draw_image(self.image, tile_center, self.size, self.pos, self.size)
        self.age = self.age % (self.tiles * ANIM_SPEED) + 1


# Helper functions

def msg_pop(message_to_show):
    global message, in_play
    message = message_to_show
    in_play = False
    soundtrack.play()


def new_game():
    global lives, score
    lives = 5
    score = 0
    start_round(1)


def start_round(level):
    global time, current_level, bubble_list
    bubble_list = []
    current_level = level
    time = TIME_LIMIT[level]
    bubble_amount = BUBBLES[level][0]
    bubble_size = BUBBLES[level][1] / 2.0
    for n in range(bubble_amount):
        bubble_list.append(Sprite(sphere_image[random.randrange(0, 7)],
                                  [(n + 1) * (WIDTH / (bubble_amount + 1)), 100],
                                  [random.randrange(20, 40) / 20.0, -3], bubble_size))


def clock_format(t):
    return str(t // 600) + ":" + str((t // 100) % 6) + str((t // 10) % 10) + "." + str(t % 10)


def group_collide(obj, group):
    to_remove = [item for item in group if item.collide(obj)]
    for item in to_remove:
        group.remove(item)
    if len(to_remove) > 0:
        return to_remove[0]
    else:
        return False


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def list_add(l1, l2):
    return [l1[i] + l2[i] for i in range(len(l1))]


def tick():
    global time, lives
    time -= 1
    if time == 0:
        msg_pop("OUT OF TIME!!!!")
        lives -= 1
        start_round(current_level)

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

class PangGame:
    def __init__(self):
        self.my_hero = Hero(hero_image, [300, 372])
        self.jump_vertical_ratio = 0.015
        self.left_ratio = -0.01
        self.right_ratio = 0.01
        self.track_pos_prev = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    # Event Handlers
    def draw(self, canvas):
        global time, score, harpoon_fired, lives, in_play, message, mess_age, current_level
        # Background
        canvas.draw_image(bg_image.get_image(),
                          bg_image.get_center(), bg_image.get_size(),
                          [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])

        # Gameplay main logic
        if in_play:
            # Harpoon
            if harpoon_fired:
                harpoon.draw(canvas)
                harpoon.update()
                pop = group_collide(harpoon, bubble_list)
                if pop != False:
                    pop_sound.play()
                    score += 10
                    time += 10 * int(math.ceil(pop.get_scale()))
                    if pop.get_scale() >= 0.255:
                        rand_speed = random.randrange(20, 40)
                        bubble_list.append(Sprite(sphere_image[random.randrange(0, 7)], pop.get_pos(),
                                                  [rand_speed / 20.0, -(pop.get_pos()[1] * 2) // 100],
                                                  pop.get_scale() / 2))
                        bubble_list.append(Sprite(sphere_image[random.randrange(0, 7)], pop.get_pos(),
                                                  [-rand_speed / 20.0, -(pop.get_pos()[1] * 2) // 100],
                                                  pop.get_scale() / 2))
                    harpoon_fired = False
                if harpoon.get_kill():
                    harpoon_fired = False

            # Hero
            self.my_hero.draw(canvas)
            self.my_hero.update()
            if group_collide(self.my_hero, bubble_list) != False:
                lives -= 1
                msg_pop("BUBBLIZED!!!!!")
                start_round(current_level)

            # Bubbles
            if len(bubble_list) == 0:
                score += time * current_level
                if current_level == 10:
                    msg_pop("YOU WIN!!!! SCORE:" + str(score))
                    new_game()
                else:
                    msg_pop("GET READY FOR LEVEL " + str(current_level + 1))
                    start_round(current_level + 1)
            for bubble in bubble_list:
                bubble.draw(canvas)
                bubble.update()

        # Popup Messages
        else:
            timer.stop()
            canvas.draw_polygon([[100, 100], [WIDTH - 100, 100], [WIDTH - 100, HEIGHT - 100], [100, HEIGHT - 100]], 10,
                                "Orange", "Silver")
            canvas.draw_text(message, [WIDTH / 2 - frame.get_canvas_textwidth(message, 25) / 2, HEIGHT / 2], 25, "Red")
            harpoon_fired = False
            mess_age += 1
            if mess_age == 120:
                in_play = True
                mess_age = 0
                timer.start()
                if lives == 0:
                    msg_pop("YOU LOST, NEW GAME BEGINS")
                    new_game()

                    # UI
        canvas.draw_text("Time Left: " + clock_format(time), [10, 25], 20, "White")
        canvas.draw_text("Lives: " + str(lives), [10, 45], 20, "White")
        canvas.draw_text("Score: " + str(score), [10, 65], 20, "White")
        canvas.draw_text("Level: " + str(current_level), [10, 85], 20, "White")

    def start_game(self, cap, tracker, track_pos_prev):
        self.tracker = tracker
        self.cap = cap
        self.track_pos_prev = track_pos_prev
        new_game()
        soundtrack.play()
        self.track_pos_prev = track_pos_prev

    def update(self):
        ret, img = self.cap.read()
        self.tracker.update(img)
        track_pos_prev = self.track_pos_prev
        pos = self.tracker.get_position()
        track_pos_current = [(pos.left() + pos.right()) / 2., (pos.top() + pos.bottom()) / 2.]
        vertical_ratio = (track_pos_current[1] - track_pos_prev[1]) / img.shape[0]
        horizontal_ratio = (track_pos_current[0] - track_pos_prev[0]) / img.shape[1]
        self.track_pos_prev = track_pos_current

        print("Vertical ration is %f" % vertical_ratio)
        print("Horitontal ration is %f\n" % horizontal_ratio)
        # if the ratio is larger than jump_vertical_ratio, then it is a jump

        if vertical_ratio > self.jump_vertical_ratio:
            if not harpoon_fired and in_play:
                self.my_hero.shoot()
            cv2.putText(img, 'space', (50, 50), self.font, 1, (0, 255, 0), 5)
            print('space')

        if horizontal_ratio > self.right_ratio:
            self.my_hero.set_vel(-5)
            cv2.putText(img, '<-', (50, 50), self.font, 1, (0, 255, 0), 5)
            print('<-')

        if horizontal_ratio < self.left_ratio:
            self.my_hero.set_vel(5)
            cv2.putText(img, '->', (50, 50), self.font, 1, (0, 255, 0), 5)
            print('->')

        cv2.rectangle(img, (int(pos.right()), int(pos.bottom())), (int(pos.left()), int(pos.top())),
                      (0, 255, 0), 3)
        cv2.imshow('Body', img)
        cv2.waitKey(1)


game = PangGame()


count = 0
def draw(canvas):
    global count
    if count>5:
        game.update()
        count = 0
    else:
        count = count + 1
    game.draw(canvas)

# Frame Setup
frame = simplegui.create_frame("Pang", 600, 400)
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)