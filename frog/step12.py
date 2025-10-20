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

def reset_frog():
    frog_rect.x = randint(frog_rect.width, SCREEN_WIDTH - frog_rect.width)
    frog_rect.y = SCREEN_HEIGHT - frog_rect.height - 20  # Just above bottom of screen

reset_frog()  # Initial frog position

# Define game zones
WATER_START = 100   # Top of water zone
WATER_END = 360    # Bottom of water zone
ROAD_START = 500   # Top of road zone
ROAD_END = 780     # Bottom of road zone

cars = []
logs = []
num_cars = 10
num_logs = 50
# Create cars
for i in range(num_cars):
    img = pygame.image.load('images/car.png').convert_alpha()
    rect = img.get_rect()
    rect.x = randint(rect.width,SCREEN_WIDTH)
    rect.y = randint(ROAD_START,ROAD_END)
    speed = randint(2,10) * -1
    new_car = {'img': img, 'rect': rect, 'speed': speed}
    cars.append(new_car)
# Create logs
for i in range(num_logs):
    img = pygame.image.load('images/log.png').convert_alpha()
    rect = img.get_rect()
    rect.x = randint(0,SCREEN_WIDTH)
    rect.y = randint(WATER_START,WATER_END)
    speed = randint(2,5)
    new_log = {'img': img, 'rect': rect, 'speed': speed}
    logs.append(new_log)

frog_speed = 10
run = True
death_time = 0
DEATH_DELAY = 1000  # 1 second delay after death
game_state = 'alive'  # Can be 'alive', 'dead', or 'winner'

while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    current_time = pygame.time.get_ticks()
    
    # Only allow movement if frog is alive and not in delay after death
    if game_state == 'alive':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: 
            if frog_rect.x - frog_speed > 0:
                frog_rect.x -= frog_speed
        if keys[pygame.K_RIGHT]: 
            if frog_rect.x + frog_speed < SCREEN_WIDTH - frog_rect.width:
                frog_rect.x += frog_speed
        if keys[pygame.K_UP]: 
            if frog_rect.y - frog_speed > 0:
                frog_rect.y -= frog_speed
        if keys[pygame.K_DOWN]: 
            if frog_rect.y + frog_speed < SCREEN_HEIGHT - frog_rect.height:
                frog_rect.y += frog_speed

    #Move
    for car in cars: 
        car['rect'].x += car['speed']
        if car['rect'].x > SCREEN_WIDTH: car['rect'].x = 0
        if car['rect'].x < 0: car['rect'].x = SCREEN_WIDTH
    for log in logs: 
        log['rect'].x += log['speed']
        if log['rect'].x > SCREEN_WIDTH: log['rect'].x = 0
        if log['rect'].x < 0: log['rect'].x = SCREEN_WIDTH
    
    if game_state == 'alive':
        # Check if frog is in water
        in_water = WATER_START <= frog_rect.y <= WATER_END
        if in_water:
            on_log = False
            for log in logs:
                if frog_rect.colliderect(log['rect']):
                    on_log = True
                    # Move with the log
                    frog_rect.x += log['speed']
                    break
            if not on_log:
                print('Splash! Frog fell in water!')
                game_state = 'dead'
                death_time = current_time

        # Check car collisions
        for car in cars:
            if frog_rect.colliderect(car['rect']):
                print('Crash! Frog hit by car!')
                game_state = 'dead'
                death_time = current_time
                break

        # Check victory
        if frog_rect.y < frog_rect.height + 10:
            print('WINNER! Frog made it!')
            game_state = 'winner'
            death_time = current_time

    # Handle death and reset
    elif game_state in ['dead', 'winner'] and current_time - death_time >= DEATH_DELAY:
        reset_frog()
        game_state = 'alive'

    #Draw
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    for car in cars: screen.blit(car['img'],(car['rect'].x,car['rect'].y))
    for log in logs: screen.blit(log['img'],(log['rect'].x,log['rect'].y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    
    pygame.display.update()
pygame.quit()