import pygame
from random import randint
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#framerate
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load an image for the background
bg_img = pygame.image.load('images/background.png').convert_alpha()
# load an image for the frog
frog_img = pygame.image.load('images/frog.png').convert_alpha()
# find the rectangles
bg_rect   = bg_img.get_rect()
frog_rect = frog_img.get_rect()
frog_rect.x = 400  # Anywhere from zero to screen width
frog_rect.y = 400  # Anywhere before the road starts

cars = []
logs = []
num_cars = 10
num_logs = 50
# Create cars
for i in range(num_cars):
    img = pygame.image.load('images/car.png').convert_alpha()
    rect = img.get_rect()
    rect.x = randint(rect.width,SCREEN_WIDTH)
    rect.y = randint(500,600 - rect.height)
    new_car = {'img': img, 'rect': rect}
    cars.append(new_car)
# Create logs
for i in range(num_logs):
    img = pygame.image.load('images/log.png').convert_alpha()
    rect = img.get_rect()
    rect.x = randint(0,SCREEN_WIDTH)
    rect.y = randint(100,360)
    new_log = {'img': img, 'rect': rect}
    logs.append(new_log)

# line 64: set a variable called 'speed' to 10 to control how far the frog moves
# line 65: we set a variable called 'run' to True
# line 66: while 'run' is 'True' the game repeatedly loops through lines 43 to 57
# line 68: looks for events
# line 69: checks to see if the event is a QUIT event 
#   the QUIT event is when the x in the top right corner of the window is clicked
# line 70: we set the value of 'run' to False
# line 72: has the RIGHT arrow key been pressed
# line 73: can we move the frog to the right and it still be on the screen
# line 74: move the frog to the right by 'speed' number of pixels
# line 75: has the LEFT arrow key been pressed
# line 76: can we move the frog to the left and it still be on the screen
# line 77: move the frog to the left by 'speed' number of pixels
# line 79: we move the background image to the 'display' using blit, BLock Image Transfer
# line 80: to line 84: draw the cars
# line 85: draw logs, because there's only one action in the 'for' loop it can go on one line
# line 86: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 87: and then update what we see on the screen

speed = 10
run = True
while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if frog_rect.x + speed < SCREEN_WIDTH - frog_rect.width:
                    frog_rect.x += speed
            if event.key == pygame.K_LEFT:
                if frog_rect.x - speed > 0:
                    frog_rect.x -= speed

    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    for car in cars:
        x = car['rect'].x
        y = car['rect'].y
        img = car['img']
        screen.blit(img,(x,y))
    for log in logs: screen.blit(log['img'],(log['rect'].x,log['rect'].y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    pygame.display.update()
pygame.quit()
