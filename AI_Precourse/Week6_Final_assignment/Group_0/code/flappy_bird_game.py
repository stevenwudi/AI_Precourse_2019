import random, math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
width, height = 400, 400
gap_width, gap_height = 40, 80
gap_pos_min, gap_pos_max = 120, 280
ground_height = 42
center = [width / 2, height / 2]
half_gap = [gap_width / 2, gap_height / 2]

difficulty = 2  # difficulty level, 1:easies, 2:moderate hard, 3: very hard
class Image:
    def __init__(self, url, size):
        self.url = url
        self.size = size
        self.image = simplegui._load_local_image(self.url)
        
    def draw(self, canvas, pos, size, angle=0):
        center = [size[0] / 2.0, size[1] / 2.0]
        canvas.draw_image(self.image, center, size, pos, size, angle)
        
class Sound:
    def __init__(self, url):
        self.url = url
        self.count = 0
        self.sound = {}
        for i in range(3):
            self.sound[i] = simplegui._load_local_sound (self.url)
        
    def play(self):
        self.sound[self.count].play()
        self.count = (self.count + 1) % 3

bird0 = Image('./flappy_bird_image/bird0.png', [30, 22])
bird1 = Image('./flappy_bird_image/bird1.png', [30, 22])
bird2 = Image('./flappy_bird_image/bird2.png', [30, 22])
pipe = Image('./flappy_bird_image/pipe.png', [40, 300])
ground = Image('./flappy_bird_image/ground.png', [400, 8])
background = Image('./flappy_bird_image/background.png', [400, 400])
spacebar = Image('./flappy_bird_image/spacebar.png', [100, 20])
board = Image('./flappy_bird_image/board.png', [78, 158])
coin = simplegui._load_local_sound('./flappy_bird_sound/coin.wav')
bump = simplegui._load_local_sound('./flappy_bird_sound/bump.wav')
end = simplegui._load_local_sound('./flappy_bird_sound/end.wav')
jump = Sound('./flappy_bird_sound/jump.wav')



class Bird:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10
        self.vel = 0
        self.time = 0
        self.image = None

    def between(self, left, right):
        return self.pos[0] + self.radius > left and self.pos[0] - self.radius < right

    def out(self, up, down):
        return self.pos[1] - self.radius < up or self.pos[1] + self.radius > down

    def fly(self):
        self.time = (self.time + 0.2) % (2 * math.pi)
        if 0 <= self.time < math.pi / 2:
            self.image = bird0
        elif math.pi <= self.time < math.pi * 3 / 2:
            self.image = bird2
        else:
            self.image = bird1

    def fall(self):
        self.vel += 0.1
        self.pos[1] += self.vel

    def flap(self):
        self.vel = -1 * difficulty

    def draw(self, canvas):
        self.image.draw(canvas, self.pos, self.image.size, 0.12 * self.vel)

class Pipe:
    def __init__(self, pos, vertical_move_scale=0):
        self.pos = pos # gap center
        self.vertical_center = self.pos[1]
        self.vertical_move = 0
        self.vertical_move_scale = vertical_move_scale

    def move(self):
        self.pos[0] -= 1
        self.vertical_move += 0.01 * self.vertical_move_scale
        self.pos[1] = self.vertical_center + 20 * math.sin(self.vertical_move)

    def draw(self, canvas):
        upper_size = [pipe.size[0], self.pos[1] - half_gap[1]]
        lower_size = [pipe.size[0], (height - ground_height) - (self.pos[1] + half_gap[1])]
        upper_pos = [self.pos[0], upper_size[1] / 2]
        lower_pos = [self.pos[0], height - ground_height - lower_size[1] / 2]
        pipe.draw(canvas, upper_pos, upper_size, math.pi)
        pipe.draw(canvas, lower_pos, lower_size)

class Ground:
    def __init__(self, y):
        self.x1 = center[0]
        self.x2 = center[0] * 3
        self.y = y

    def move(self):
        self.x1 -= 1
        self.x2 -= 1
        if self.x1 == - center[0]:
            self.x1 = center[0] * 3
        if self.x2 == - center[0]:
            self.x2 = center[0] * 3

    def draw(self, canvas):
        ground.draw(canvas, [self.x1, self.y], ground.size)
        ground.draw(canvas, [self.x2, self.y], ground.size)

class Game:
    def __init__(self):
        self.bird = None
        self.pipes = None
        self.ground = Ground(364)
        self.score = None
        self.best = 0
        self.new = ''
        self.phase = {}
        for i in range(4):
            self.phase[i] = False

    def start(self):
        self.bird = Bird([180, height / 2])
        self.pipes = [Pipe([500, random.randrange(gap_pos_min, gap_pos_max)]),
                 Pipe([650, random.randrange(gap_pos_min, gap_pos_max)]),
                 Pipe([800, random.randrange(gap_pos_min, gap_pos_max)])]
        self.score = 0
        self.time = 0
        self.phase[0] = True

    def update(self):
        if self.phase[3]:
            return

        if self.bird.out(-float('inf'), height - 42):
            end.play()
            self.phase[1] = False
            self.phase[2] = False
            self.phase[3] = True
            return

        if self.pipes[0].pos[0] + half_gap[0] < 0:
            self.pipes.pop(0)
            x = self.pipes[-1].pos[0] + 150
            self.pipes.append(Pipe([x, random.randrange(gap_pos_min, gap_pos_max)], random.randrange(-5, 5)))

        if self.phase[0]:
            self.bird.fly()
            self.bird.pos[1] = height / 2 + 4 * math.sin(self.bird.time)
            self.ground.move()

        elif self.phase[1]:
            self.bird.fly()
            self.bird.fall()
            self.ground.move()
            for pipe in self.pipes:
                pipe.move()
                if pipe.pos[0] == self.bird.pos[0]:
                    coin.play()
                    self.score += 1
                if self.bird.between(pipe.pos[0] - half_gap[0], pipe.pos[0] + half_gap[0]):
                    if self.bird.out(pipe.pos[1] - half_gap[1], pipe.pos[1] + half_gap[1]):
                        bump.play()
                        self.bird.vel = 0
                        self.phase[1] = False
                        self.phase[2] = True
                        if self.score > self.best:
                            self.best = self.score
                            self.new = 'new'
                        else:
                            self.new = ''

        elif self.phase[2]:
            self.bird.fall()

    def draw(self, canvas):
        background.draw(canvas, center, background.size)
        self.ground.draw(canvas)
        for pipe in self.pipes:
            pipe.draw(canvas)
        self.bird.draw(canvas)
        if self.phase[0]:
            spacebar.draw(canvas, [200, 240], spacebar.size)
        elif self.phase[3]:
            board.draw(canvas, center, board.size)
            canvas.draw_text(str(self.score), [190, 180], 24, 'Chocolate', 'sans-serif')
            canvas.draw_text(str(self.best), [190, 240], 24, 'Chocolate', 'sans-serif')
            canvas.draw_text(str(self.new), [170, 196], 10, 'Red', 'sans-serif')
        else:
            canvas.draw_text(str(self.score), [200, 80], 30, 'DeepSkyBlue', 'sans-serif')

game = Game()

def keydown(key):
    if key == simplegui.KEY_MAP['space']:
        if game.phase[0] or game.phase[1]:
            jump.play()
            game.bird.flap()
            if game.phase[0]:
                game.phase[0] = False
                game.phase[1] = True
        elif game.phase[3]:
            game.phase[3] = False
            game.start()

def draw(canvas):
    game.update()
    game.draw(canvas)

frame = simplegui.create_frame("Flappy", width, height)
frame.set_keydown_handler(keydown)
frame.set_draw_handler(draw)

game.start()
frame.start()
