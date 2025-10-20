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
# find it's rectangle, which is x,y,w,h
#   x = x coordinate
#   y = y coordinate
#   w = width of rectangle
#   h = height of rectangle
bg_rect   = bg_img.get_rect()
frog_rect = frog_img.get_rect()
# for debug purpose display the rectangle details
print('Background Image Rectangle',    bg_rect)
print('Background Image x coordinate', bg_rect.x)
print('Background Image y coordinate', bg_rect.y)
print('Background Image width',        bg_rect.width)
print('Background Image height',       bg_rect.height)
# === PUT CODE HERE TO SET THE COORDINATES OF THE FROG IMAGE HERE ====

# We can control where the image is displayed by
# changing the x and y coordinates
# for backgrounds it's usually 0,0, which is top left corner

# line 48: we set a variable call 'run' to True
# line 49: while 'run' is True the game repeatedly loops through lines 48 to 55
# line 50: looks for events
# line 51: checks to see if the event is a QUIT event 
#   the QUIT event is when the x in the top right corner of the window is clicked
# line 52: we set the run value to False
# line 53: we move the background image to the 'display' using blit, BLock Image Transfer
# line 54: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 55: and then update what we see on the screen

run = True
while run: 
   clock.tick(FPS)
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
       run = False
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    pygame.display.update()
pygame.quit()
