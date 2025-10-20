import pygame
from random import randint
pygame.init()
pygame.mixer.init()  # Initialize the sound mixer

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 960

#framerate
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
jump_sound = pygame.mixer.Sound('sounds/frog-jump01.mp3')
splash_sound = pygame.mixer.Sound('sounds/watery-splash.wav')
crash_sound = pygame.mixer.Sound('sounds/car-crash.mp3')

# Load and start background music
pygame.mixer.music.load('sounds/road-noise.wav')
pygame.mixer.music.set_volume(0.3)  # Set background music volume to 30%
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Set sound effect volumes
jump_sound.set_volume(0.4)
splash_sound.set_volume(0.5)
crash_sound.set_volume(0.5)

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
DEATH_DELAY = 500  # Reduced from 1000ms to 500ms (half second)
game_state = 'alive'  # Can be 'alive', 'dead', or 'winner'
last_move_time = 0
MOVE_SOUND_DELAY = 200  # Minimum delay between jump sounds (milliseconds)

# Create a flashing effect for death animation
def draw_death_flash(screen, color):
    flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    flash_surface.fill(color)
    flash_surface.set_alpha(100)  # Semi-transparent
    screen.blit(flash_surface, (0,0))

while run: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    current_time = pygame.time.get_ticks()
    
    # Only allow movement if frog is alive and not in delay after death
    if game_state == 'alive':
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]: 
            if frog_rect.x - frog_speed > 0:
                frog_rect.x -= frog_speed
                moved = True
        if keys[pygame.K_RIGHT]: 
            if frog_rect.x + frog_speed < SCREEN_WIDTH - frog_rect.width:
                frog_rect.x += frog_speed
                moved = True
        if keys[pygame.K_UP]: 
            if frog_rect.y - frog_speed > 0:
                frog_rect.y -= frog_speed
                moved = True
        if keys[pygame.K_DOWN]: 
            if frog_rect.y + frog_speed < SCREEN_HEIGHT - frog_rect.height:
                frog_rect.y += frog_speed
                moved = True
        
        # Play jump sound if moved and enough time has passed since last sound
        if moved and current_time - last_move_time > MOVE_SOUND_DELAY:
            jump_sound.play()
            last_move_time = current_time

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
                splash_sound.play()
                game_state = 'dead'
                death_time = current_time

        # Check car collisions
        for car in cars:
            if frog_rect.colliderect(car['rect']):
                print('Crash! Frog hit by car!')
                crash_sound.play()
                game_state = 'dead'
                death_time = current_time
                break

        # Check victory
        if frog_rect.y < frog_rect.height + 10:
            print('WINNER! Frog made it!')
            jump_sound.play()
            game_state = 'winner'
            death_time = current_time

    #Draw
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    for car in cars: screen.blit(car['img'],(car['rect'].x,car['rect'].y))
    for log in logs: screen.blit(log['img'],(log['rect'].x,log['rect'].y))
    screen.blit(frog_img, (frog_rect.x,frog_rect.y))
    
    # Draw death/victory effects
    if game_state == 'dead':
        # Flash red for death
        if (current_time - death_time) < DEATH_DELAY:
            # Create a pulsing effect based on time
            flash_intensity = abs(((current_time - death_time) % 200) - 100) / 100
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill((255, 0, 0))  # Red flash for death
            flash_surface.set_alpha(int(64 * flash_intensity))  # Pulsing transparency
            screen.blit(flash_surface, (0,0))
    elif game_state == 'winner':
        # Flash green for victory
        if (current_time - death_time) < DEATH_DELAY:
            # Create a pulsing effect based on time
            flash_intensity = abs(((current_time - death_time) % 200) - 100) / 100
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill((0, 255, 0))  # Green flash for victory
            flash_surface.set_alpha(int(64 * flash_intensity))  # Pulsing transparency
            screen.blit(flash_surface, (0,0))

    # Handle death and reset
    if (game_state in ['dead', 'winner'] and 
        current_time - death_time >= DEATH_DELAY):
        reset_frog()
        game_state = 'alive'
    
    pygame.display.update()

# Clean up before quitting
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()