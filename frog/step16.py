import pygame
from random import randint
import math
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

# Initialize game level and difficulty settings
current_level = 1
base_car_speed = 1  # Starting speed for cars
base_log_speed = 1  # Starting speed for logs
speed_increase_per_level = 0.4  # How much speed increases per level

def get_level_speeds():
    """Calculate speeds for current level"""
    car_min = base_car_speed + (current_level - 1) * speed_increase_per_level
    car_max = car_min + 3  # Always 3 more than min for consistent challenge
    log_min = base_log_speed + (current_level - 1) * (speed_increase_per_level * 0.5)  # Logs increase slower
    log_max = log_min + 2  # Always 2 more than min for consistent challenge
    return car_min, car_max, log_min, log_max

def reset_frog():
    frog_rect.x = randint(frog_rect.width, SCREEN_WIDTH - frog_rect.width)
    frog_rect.y = SCREEN_HEIGHT - frog_rect.height - 20  # Just above bottom of screen

def create_cars():
    """Create cars with current level speed"""
    cars = []
    car_min, car_max, _, _ = get_level_speeds()
    for i in range(num_cars):
        img = pygame.image.load('images/car.png').convert_alpha()
        rect = img.get_rect()
        rect.x = randint(rect.width, SCREEN_WIDTH)
        rect.y = randint(ROAD_START, ROAD_END)
        speed = -(randint(int(car_min * 10), int(car_max * 10)) / 10)  # Convert to float
        new_car = {'img': img, 'rect': rect, 'speed': speed}
        cars.append(new_car)
    return cars

def create_logs():
    """Create logs with current level speed"""
    logs = []
    _, _, log_min, log_max = get_level_speeds()
    for i in range(num_logs):
        img = pygame.image.load('images/log.png').convert_alpha()
        rect = img.get_rect()
        rect.x = randint(0, SCREEN_WIDTH)
        rect.y = randint(WATER_START, WATER_END)
        speed = randint(int(log_min * 10), int(log_max * 10)) / 10  # Convert to float
        new_log = {'img': img, 'rect': rect, 'speed': speed}
        logs.append(new_log)
    return logs

def draw_level_text():
    """Draw current level on screen"""
    font = pygame.font.Font(None, 74)
    text = font.render(f'Level {current_level}', True, (255, 255, 255))
    text_rect = text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    # Draw black outline for visibility
    outline = font.render(f'Level {current_level}', True, (0, 0, 0))
    for dx, dy in [(-2,-2), (-2,2), (2,-2), (2,2)]:  # Draw outline
        screen.blit(outline, (text_rect.x + dx, text_rect.y + dy))
    screen.blit(text, text_rect)

reset_frog()  # Initial frog position

# Define game zones
WATER_START = 100   # Top of water zone
WATER_END = 360    # Bottom of water zone
ROAD_START = 500   # Top of road zone
ROAD_END = 780     # Bottom of road zone

num_cars = 10
num_logs = 50
cars = create_cars()
logs = create_logs()

frog_speed = 10
run = True
death_time = 0
DEATH_DELAY = 500  # Half second
game_state = 'alive'  # Can be 'alive', 'dead', or 'winner'
last_move_time = 0
MOVE_SOUND_DELAY = 200  # Minimum delay between jump sounds (milliseconds)
death_rotation = 0  # Current rotation angle for death animation
death_scale = 1.0   # Current scale for death animation
death_type = None   # 'water' or 'car'

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
                death_type = 'water'
                death_rotation = 0
                death_scale = 1.0

        # Check car collisions
        for car in cars:
            if frog_rect.colliderect(car['rect']):
                print('Crash! Frog hit by car!')
                crash_sound.play()
                game_state = 'dead'
                death_time = current_time
                death_type = 'car'
                death_rotation = 0
                death_scale = 1.0
                break

        # Check victory
        if frog_rect.y < frog_rect.height + 10:
            print(f'WINNER! Level {current_level} completed!')
            jump_sound.play()
            game_state = 'winner'
            death_time = current_time

    #Draw
    screen.blit(bg_img, (bg_rect.x,bg_rect.y))
    for car in cars: screen.blit(car['img'],(car['rect'].x,car['rect'].y))
    for log in logs: screen.blit(log['img'],(log['rect'].x,log['rect'].y))
    
    # Draw level indicator
    draw_level_text()
    
    # Draw frog with animation if dead
    if game_state == 'dead':
        progress = (current_time - death_time) / DEATH_DELAY
        if death_type == 'car':
            # Spinning animation for car crash
            death_rotation = progress * 720  # Spin twice
            death_scale = 1.0 - progress * 0.5  # Shrink to 50%
        else:  # water
            # Spinning while sinking for water death
            death_rotation = progress * 360  # Spin once
            death_scale = 1.0 - progress * 0.8  # Shrink to 20%

        # Scale and rotate the frog image
        scaled_size = (int(frog_img.get_width() * death_scale), 
                      int(frog_img.get_height() * death_scale))
        scaled_frog = pygame.transform.scale(frog_img, scaled_size)
        rotated_frog = pygame.transform.rotate(scaled_frog, death_rotation)
        
        # Get the new rect for the transformed frog
        new_rect = rotated_frog.get_rect(center=frog_rect.center)
        screen.blit(rotated_frog, new_rect)

        # Draw death flash effect
        flash_intensity = abs(((current_time - death_time) % 200) - 100) / 100
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        if death_type == 'car':
            flash_surface.fill((255, 0, 0))  # Red flash for car crash
        else:
            flash_surface.fill((0, 0, 255))  # Blue flash for water
        flash_surface.set_alpha(int(64 * flash_intensity))
        screen.blit(flash_surface, (0,0))
    elif game_state == 'winner':
        # Victory animation
        flash_intensity = abs(((current_time - death_time) % 200) - 100) / 100
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash_surface.fill((0, 255, 0))  # Green flash for victory
        flash_surface.set_alpha(int(64 * flash_intensity))
        screen.blit(flash_surface, (0,0))
        screen.blit(frog_img, frog_rect)
    else:
        # Normal frog drawing
        screen.blit(frog_img, frog_rect)

    # Handle death and reset
    if game_state == 'dead' and current_time - death_time >= DEATH_DELAY:
        reset_frog()
        game_state = 'alive'
    elif game_state == 'winner' and current_time - death_time >= DEATH_DELAY:
        current_level += 1
        print(f"Starting Level {current_level}")
        # Create new cars and logs with updated speeds
        cars = create_cars()
        logs = create_logs()
        reset_frog()
        game_state = 'alive'
    
    pygame.display.update()

# Clean up before quitting
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()