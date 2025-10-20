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

frog_rect.x = 400  # Anywhere from zero to screen width
frog_rect.y = 400  # Anywhere before the road starts

# We can control where the frog is displayed by
# changing the rectangle's x and y coordinates

# line 39: we set a variable called 'run' to True
# line 40: while 'run' is True the game repeatedly loops through lines 40 to 48
# line 42: looks for events
# line 43: checks to see if it's a QUIT event 
#   the quit event is when the x in the top right corner of the window is clicked
# line 44: if it's a quit event, we set the value of 'run' to False
# line 45: move the frog 1 pixel to the right
# line 46: we move the background image to the 'display' using blit, BLock Image Transfer
# line 47: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 48: and then update what we see on the screen

run = True
while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    frog_rect.x += 1
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    pygame.display.update()
pygame.quit()
