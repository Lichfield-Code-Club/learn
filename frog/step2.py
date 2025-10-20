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
# find it's rectangle, which is x,y,w,h
#   x = x coordinate
#   y = y coordinate
#   w = width of rectangle
#   h = height of rectangle
bg_rect = bg_img.get_rect()
# for debug purpose display the rectangle details
print('Background Image Rectangle', bg_rect)
print('Background Image x coordinate', bg_rect.x)
print('Background Image y coordinate', bg_rect.y)
print('Background Image width', bg_rect.width)
print('Background Image height', bg_rect.height)

# We can control where the image is displayed by
# changing the x and y coordinates
# for backgrounds the x and y coordinates are usually 0,0, which is the top left corner

# line 42: we set a variable called 'run' to True
# line 43: while 'run' is True the game repeatedly loops through lines 43 to 49
# line 45: looks for events
# line 46: checks to see if the event is a QUIT event 
#   the QUIT event is when the x in the top right corner of the window is clicked
# line 47: we set the value of 'run' to False
# line 48: we move the image to the 'display' using blit, BLock Image Transfer
# line 49: update what is shown on the screen

run = True
while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    pygame.display.update()
pygame.quit()
