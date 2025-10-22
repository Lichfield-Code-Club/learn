#PONG pygame

# The following import lines include other python libraries to your code
# This allows you to call functions that you have not written.
# For example the function set_caption belongs to the Pygame library and
# we use it here to set the games window caption to 'Pong'

import random
import pygame, sys
from pygame.locals import *

# The following line initialises the Pygame engine.

pygame.init()
pygame.font.init()

# The following line sets up the 'Frames Per Second'
# This determines how fast the screen is drawn in the main game loop

fps = pygame.time.Clock()

# Here we define some colour constant

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

# Here we define some global variables to represent various bits of the game.
# Global means they can be read anywhere in our code.

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

GAME_IN_PLAY = True
maxScore=2


# The variables above refer to the following game elements
# WIDTH is the width of the screen in pixels
# HEIGHT is the height of the screen in pixels
# BALL_RADIUS is the radius (size) of the ball.
# PAD_WIDTH is the width of the bats in pixels
# PAD_HEIGHT is the height of the bats in pixels
# HALF_PAD_WIDTH is the pad width divided by 2 
# HALF_PAD_HEIGHT is the pad height divided by 2
# ball_pos is a vector variable that holds the X and Y position of the ball in pixels
# ball_vel is a vector variable that holds the X and Y velocity of the ball (This is how many pixels the ball moves in each direction per frame)
# paddle1_vel is the velocity of bat 1 (Why do you think that this is a simple variable and not a vector variable as before)
# paddle2_vel is the velocity of bat 2
# l_score is the left players score
# r_score is the right players score



#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# Set the caption on the top of our game window.
pygame.display.set_caption('Pong')

# Here we define a function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left

def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH//2,HEIGHT//2]

# horz and vert hold the vertical (Y) and horizontal (X) velocity of the ball.
# We call the random function to set the horz speed between 2 and 4 and the vertical speed between 1 and 3
    
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)

# The code below decides if the ball should go to the right or the left based on a random value passed into this function
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# Here we define our functions and event handlers

# The function below sets up some initial values and decides where the paddles and ball are placed on the screen.

def init():

    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints

# the following lines set the position of the two paddles

    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]

# the following lines set the scores to zero

    l_score = 0
    r_score = 0

# generate a random number and call the ball_init() function with a parameter based on the random number

    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


# Here we define a function to draw on the canvas

def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score, GAME_IN_PLAY
           
    canvas.fill(BLACK)

    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    if(GAME_IN_PLAY):

            # update paddle's vertical position, keep paddle on the screen
            
            if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
                paddle1_pos[1] += paddle1_vel
            elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
                paddle1_pos[1] += paddle1_vel
            elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
                paddle1_pos[1] += paddle1_vel
            
            if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
                paddle2_pos[1] += paddle2_vel
            elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
                paddle2_pos[1] += paddle2_vel
            elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
                paddle2_pos[1] += paddle2_vel

            #update ball

            ball_pos[0] += int(ball_vel[0])
            ball_pos[1] += int(ball_vel[1])

            #draw paddles and ball

            pygame.draw.circle(canvas, RED, ball_pos, BALL_RADIUS, 0)
            pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
            pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

            #ball collision check on top and bottom walls

            if int(ball_pos[1]) <= BALL_RADIUS:
                ball_vel[1] = - ball_vel[1]
            if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
                ball_vel[1] = -ball_vel[1]
            
            #ball collison check on gutters or paddles

            if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH) and (ball_pos[1] in range(paddle1_pos[1] - HALF_PAD_HEIGHT, paddle1_pos[1] + HALF_PAD_HEIGHT,1)):
                ball_vel[0] = -ball_vel[0]
                ball_vel[0] *= 1.1
                ball_vel[1] *= 1.1
            elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
                r_score += 1
                ball_init(True)
                
            if ball_pos[0] >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and ball_pos[1] in range(paddle2_pos[1] - HALF_PAD_HEIGHT, paddle2_pos[1] + HALF_PAD_HEIGHT,1):
                ball_vel[0] = -ball_vel[0]
                ball_vel[0] *= 1.1
                ball_vel[1] *= 1.1
            elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
                l_score += 1
                ball_init(False)

            #update scores

            myfont1 = pygame.font.SysFont("Times New Roman", 27)
            label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
            canvas.blit(label1, (50,20))

            myfont2 = pygame.font.SysFont("Times New Roman", 27)
            label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
            canvas.blit(label2, (470, 20))

    myfont3 = pygame.font.SysFont("Times new Roman", 75)
#check for end of game

    if((l_score >= maxScore) or (r_score >= maxScore)):

        GAME_IN_PLAY = False
        
        label3 = myfont3.render("Game Over", 1, (255,0,0))
        canvas.blit(label3, (130,25))

        myfont4 = pygame.font.SysFont("Times New Roman", 50)
        myfont5 = pygame.font.SysFont("Times New Roman", 50)

        if((l_score > r_score)):
            label4 = myfont4.render("Left Player Wins!", 1, (255,128,128))
            canvas.blit(label4, (130,120))
        elif(r_score > l_score):
            label5 = myfont5.render("Right Player Wins!", 1, (255,128,128))
            canvas.blit(label5, (130,120))


    
    
#keydown handler

def keydown(event):
    global paddle1_vel, paddle2_vel, GAME_IN_PLAY
    
    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8
    elif event.key == K_r:
        if not GAME_IN_PLAY:
            init()
            GAME_IN_PLAY = True
    elif event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()

#keyup handler

def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0



# The following line calls our init() function to intialise the variables.

init()


#game loop

while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
# The following line flips the previously displayed screen for the new one.

    pygame.display.update()

    fps.tick(60)
