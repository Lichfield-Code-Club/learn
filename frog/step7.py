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

# line 41: set a varible called 'speed' to 10 to control how far the frog moves
# line 42: we set a variable called 'run' to True
# line 43: while 'run' is 'True' the game repeatedly loops through lines 43 to 57
# line 45: looks for events
# line 46: checks to see if the event is a QUIT event 
#   the QUIT event is when the x in the top right corner of the window is clicked
# line 47: we set the value of 'run' to False
# line 49: has the RIGHT arrow key been pressed
# line 50: can we move the frog to the right and it still be on the screen
# line 51: move the frog to the right by 'speed' number of pixels
# line 52: has the LEFT arrow key been pressed
# line 53: can we move the frog to the left and it still be on the screen
# line 54: move the frog to the left by 'speed' number of pixels
# line 55: we move the background image to the 'display' using blit, BLock Image Transfer
# line 56: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 57: and then update what we see on the screen

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
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    pygame.display.update()
pygame.quit()
