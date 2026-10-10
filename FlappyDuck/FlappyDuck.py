from kepoco import display, buttonA, buttonB, buttonU, buttonD, buttonC, Sprite
import random
import time

# constants
# initial value of gravity
INITIAL_GRAVITY = 0.3
# amount the falling increases by
ACCELERATION = 0.2
# how many pixels the jump is
JUMP_HEIGHT = 6
# fps
FPS = 35
# maximum the duck can fly up to
CEILING = 0
# how low the duck can fall
FLOOR = display.height
# gap between the two pipes
PIPE_GAP = 20

# bitmaps
DUCK_BASE = bytearray([24,191,127,191,191,127,191,24])
#ORIGINAL_DUCK = bytearray([240,112,127,255,12,12,12,8])
SMILE_DUCK = bytearray([0,8,17,20,20,17,8,0])
SAD_DUCK = bytearray([0,18,10,8,8,10,18,0])

# gets current high score from txt
high_score_file = open('/Games/FlappyDuck/high_score.txt', 'r')
high_score = int(high_score_file.readline().strip())
high_score_file.close()

# variables for whether to start running the title screen and the game
title_screen = True
game_running = False

display.setFPS(FPS)

# class for the duck
class Duck:
    def __init__(self):
        self.gravity = INITIAL_GRAVITY
        self.duck_sprite = Sprite(8, 8, apply_face(DUCK_BASE, SMILE_DUCK), 0, 18)

    # controls the duck falling
    def move(self):
        if self.duck_sprite.y + self.duck_sprite.height + self.gravity + ACCELERATION < FLOOR:
            self.gravity += ACCELERATION
            self.duck_sprite.y += int(self.gravity)
        else:
            self.duck_sprite.y = FLOOR - self.duck_sprite.height

    # makes the duck jump
    def jump(self):
        if self.duck_sprite.y - JUMP_HEIGHT > CEILING:
            self.gravity = INITIAL_GRAVITY
            self.duck_sprite.y -= JUMP_HEIGHT
        else:
            self.duck_sprite.y = CEILING

    # just draws the sprite to the screen
    def draw(self):
        display.drawSprite(self.duck_sprite)
    
    # changes the look of the duck
    # some help from an llm used
    def change_duck_sprite(self, new_bytearray: bytearray):
        x, y = self.duck_sprite.x, self.duck_sprite.y
        self.duck_sprite = Sprite(8, 8, new_bytearray, x, y)

# class for the pipe
class Pipe():
    def __init__(self, top_pipe: bool, pipe_height: int):
        self.pipe_width = 10
        self.pipe_height = pipe_height
        self.pipe_x = display.width
        self.top_pipe = top_pipe
        # calculates the position to start drawing by taking
        # the display height and subtracting the pipe height
        # if it's the top pipe (rectangle drawn upwards)
        if self.top_pipe:
            self.pipe_y = display.height - self.pipe_height
        else:
            self.pipe_y = 0
        self.passed_by_duck = False
    
    # draws the pipe to the screen
    def draw(self):
        display.drawFilledRectangle(self.pipe_x, self.pipe_y, self.pipe_width, self.pipe_height, display.WHITE)
    
    # moves the pipe forward
    def move(self):
        self.pipe_x -= 1
        
    # check if it's collided with the duck
    # some help from an llm used
    def check_duck_collision(self, duck: Duck) -> bool:
        if (duck.duck_sprite.x < self.pipe_x + self.pipe_width and
            duck.duck_sprite.x + duck.duck_sprite.width > self.pipe_x and
            duck.duck_sprite.y < self.pipe_y + self.pipe_height and
            duck.duck_sprite.y + duck.duck_sprite.height > self.pipe_y):
            return True

        return False
    
    # check if the duck has passed the pipe (returns false if it 
    # already has to avoid counting score multiple times)
    def duck_past_pipe(self, duck: Duck) -> bool:
        if duck.duck_sprite.x >= self.pipe_x + self.pipe_width and not self.passed_by_duck:
            self.passed_by_duck = True
            return True
        else:
            return False

# draws all the objects to the display and also the score
def update_display(objects: list, score: int):
    display.fill(display.BLACK)

    for object in objects:
        object.draw()
    
    display.drawText(str(score), 48, 0, display.WHITE)
    display.update()

# moves all the objects (makes pipes move forward and duck fall)
def move_objects(objects: list):
    for object in objects:
        object.move()

# geenrates new pipes when needed
def generatePipes() -> tuple[Pipe, Pipe]:
    # random height for the top pipe
    height_one = random.randint(5, 10)
    pipe1 = Pipe(True, height_one)
    
    # calculates the height for the bottom pipe
    height_two = display.height - height_one - PIPE_GAP
    pipe2 = Pipe(False, height_two)
    return (pipe1, pipe2)

# function that uses bitwises to apply facial expressions
def apply_face(base: bytearray, facial_expression: bytearray) -> bytearray:
    return bytearray((base[i] & facial_expression[i]) ^ base[i] for i in range(len(base)))

# title screen
while title_screen:
    display.drawText("FLAPPYDUCK", 0, 0, display.WHITE)
    display.drawText("A TO PLAY", 0, 9, display.WHITE)
    display.drawText("B TO EXIT", 0, 18, display.WHITE)
    if buttonA.justPressed():
        game_running = True
        title_screen = False
    if buttonB.justPressed():
        game_running = False
        title_screen = False
    display.update()

display.fill(display.BLACK)

# main game loop
while game_running:
    scroll_position = 0  # controls the position the scrollable text is drawn at for the end screen
    new_high_score_achieved = False
    duck = Duck()
    pipe1, pipe2 = generatePipes()
    objects = [duck, pipe1, pipe2]
    score = 0
    
    while True:
        move_objects(objects)
        
        # checks if either pipe has collided with the duck
        if pipe1.check_duck_collision(duck) or pipe2.check_duck_collision(duck):
            duck.change_duck_sprite(apply_face(DUCK_BASE, SAD_DUCK))
            update_display(objects, score)
            time.sleep(1)
            break
        
        # jumps if botton is pressed
        if buttonA.justPressed():
            duck.jump()
    
        # adds score if duck has passed the pipe
        if pipe1.duck_past_pipe(duck):
            score += 1
        
        # generates new pipes if the pipes have moved off screen
        if pipe1.pipe_x + pipe1.pipe_width <= 0:
            pipe1, pipe2 = generatePipes()
            objects[1], objects[2] = pipe1, pipe2
        
        update_display(objects, score)
    
    display.fill(display.BLACK)
    
    # game over screen
    # button c chosen because i kept pressing button a by accident
    # when the game was over
    while not buttonC.justPressed():
        display.fill(display.BLACK)
        
        # controls the scrolling
        if buttonD.pressed() and scroll_position < 36:
            scroll_position += 1
        if buttonU.pressed() and scroll_position > 0:
            scroll_position -= 1
        
        # shows the score
        display.drawText("GAME OVER", 0, 0 - scroll_position, display.WHITE)
        display.drawText("Score: " + str(score), 0, 9 - scroll_position, display.WHITE)
        
        # handles the high score
        if score > high_score:
            high_score = score
            high_score_file = open("/Games/FlappyDuck/high_score.txt", "w")
            high_score_file.write(str(high_score))
            high_score_file.close()
            new_high_score_achieved = True
            
        # new_high_score_achieved exists to prevent other text being drawn over
        # high score text
        if new_high_score_achieved:
            display.drawText("HIGH SCORE!", 0, 18 - scroll_position, display.WHITE)
        else:
            display.drawText("High Score: ", 0, 18 - scroll_position, display.WHITE)
            display.drawText(str(high_score), 0, 27 - scroll_position, display.WHITE)
        
        display.drawText("CLICK STICK", 0, 36 - scroll_position, display.WHITE)
        display.drawText("2 PLAY AGAIN", 0, 45 - scroll_position, display.WHITE)
        display.drawText("B TO EXIT", 0, 54 - scroll_position, display.WHITE)
        
        # quits the game
        if buttonB.justPressed():
            game_running = False
            break
        
        display.update()
