import pygame
from random import randint
pygame.init()

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 960

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
frog_rect.x = randint(frog_rect.width,SCREEN_WIDTH)  # Anywhere from zero to screen width
frog_rect.y = randint(820,SCREEN_HEIGHT-frog_rect.height)  # Anywhere before the road starts

cars = []
logs = []
num_cars = 10
num_logs = 50
# Create cars
for i in range(num_cars):
    img = pygame.image.load('images/car.png').convert_alpha()
    rect = img.get_rect()
    rect.x = randint(rect.width,SCREEN_WIDTH)
    rect.y = randint(500,780)
    speed = randint(2,10) * -1
    new_car = {'img': img, 'rect': rect, 'speed': speed}
    cars.append(new_car)
# Create logs
for i in range(num_logs):
    img = pygame.image.load('images/log.png').convert_alpha()
    rect = img.get_rect()
    rect.x = randint(0,SCREEN_WIDTH)
    rect.y = randint(100,360)
    speed = randint(2,5)
    new_log = {'img': img, 'rect': rect, 'speed': speed}
    logs.append(new_log)

frog_speed = 10
run = True
while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        if frog_rect.x - frog_speed > 0: frog_rect.x -= frog_speed
    if keys[pygame.K_RIGHT]: 
        if frog_rect.x + frog_speed < SCREEN_WIDTH - frog_rect.width: frog_rect.x += frog_speed
    if keys[pygame.K_UP]: 
        if frog_rect.y - frog_speed > 0: frog_rect.y -= frog_speed
    if keys[pygame.K_DOWN]: 
        if frog_rect.y + frog_speed < SCREEN_HEIGHT - frog_rect.height : frog_rect.y += frog_speed

    #Move
    for car in cars: 
        car['rect'].x += car['speed']
        if car['rect'].x > SCREEN_WIDTH: car['rect'].x = 0
        if car['rect'].x < 0: car['rect'].x = SCREEN_WIDTH
    for log in logs: 
        log['rect'].x += log['speed']
        if log['rect'].x > SCREEN_WIDTH: log['rect'].x = 0
        if log['rect'].x < 0: log['rect'].x = SCREEN_WIDTH
    
    # Collision
    for car in cars:
        if frog_rect.colliderect(car['rect']): print('Frog Collided with car','Argh!')
    for log in logs:
        if frog_rect.colliderect(log['rect']): print('Frog Collided with log', 'Yay!')
    if frog_rect.y < frog_rect.height + 10: print('Frog made it','WINNER')

    #Draw
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    for car in cars: screen.blit(car['img'],(car['rect'].x,car['rect'].y))
    for log in logs: screen.blit(log['img'],(log['rect'].x,log['rect'].y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    
    pygame.display.update()
pygame.quit()
