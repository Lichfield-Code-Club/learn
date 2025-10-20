import pygame

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
# === PUT CODE HERE TO SET THE COORDINATES OF THE FROG IMAGE HERE ====
frog_rect.x = 400  # Anywhere from zero to screen width
frog_rect.y = 400  # Anywhere before the road starts

# line 38: we set a variable called 'run' to True
# line 39: while 'run' is 'True' the game repeatedly loops through lines 39 to 51
# line 41: looks for events
# line 42: checks to see if the event is a QUIT event 
#   the QUIT event is when the x in the top right corner of the window is clicked
# line 43: we set the value of 'run' to False
# line 44: and line 45: comment out moving to the right
# line 46: if the frog's x coordinate is greater than 1
# line 47:   move the frog 1 pixel to the left
# line 48: we move the background image to the 'display' using blit, BLock Image Transfer
# line 49: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 50: and then update what we see on the screen

run = True
while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #if frog_rect.x +1 < SCREEN_WIDTH - frog_rect.width:
    #    frog_rect.x += 1
    if frog_rect.x -1 > 0:
        frog_rect.x -= 1
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    pygame.display.update()
pygame.quit()
