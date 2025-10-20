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
frog_rect.x = 400  # Anywhere from zero to screen width
frog_rect.y = 400  # Anywhere before the road starts

# We can control where the image is displayed by
# changing the x and y coordinates
# for backgrounds it's usually 0,0, which is top left corner

# line 51: we set a variable called 'run' to True
# line 52: while 'run' is True the game repeatedly loops through lines 52 to 61
# line 54: looks for events
# line 55: checks to see if the event is a QUIT event 
#    the QUIT event is when the x in the top right of the window is clicked
# line 56: we set the value of 'run' to False
# line 57: if the right hand edge of the from rectangle hasn't reach the screen edge
# line 58:    increase the x coordinate by 1 pixel
# line 59: we move the background image to the 'display' using blit, BLock Image Transfer
# line 60: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 61: and then update what we see on the screen

run = True
while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if frog_rect.x +1 < SCREEN_WIDTH - frog_rect.width:
        frog_rect.x += 1
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    pygame.display.update()
pygame.quit()
