import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#framerate
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
while run:
  clock.tick(FPS)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

pygame.quit()
