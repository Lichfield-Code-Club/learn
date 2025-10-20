import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#framerate
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# line 22: we set a variable called 'run' to True
# line 22: while 'run' is True the game repeatedly loops through lines 23 to 28
# line 24: looks for events
# line 25: checks to see if the event is a QUIT event 
#   the quit event is when the x in the top right corner of the window is clicked
# line 26: we set the value of 'run' to False .. which allows the 'while' loop to end

run = True
while run: 
  clock.tick(FPS)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

pygame.quit()
