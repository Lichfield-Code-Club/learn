import pygame
import sys
from random import randint, choice, random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 850  # Adjusted to match new safe zone 2

# Game zones
WATER_START = 100
WATER_END = WATER_START + 260
ROAD_START = WATER_END + 90    # Safe zone 1 is 90px
ROAD_END = ROAD_START + 280
BOTTOM_EDGE = ROAD_END + 120   # Safe zone 2 is exactly 120px

def create_noise_texture(width, height, base_color, variation=20):
    """Creates a noise texture based on a color"""
    surface = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            noise = randint(-variation, variation)
            color = [max(0, min(255, c + noise)) for c in base_color]
            surface.set_at((x, y), color)
    return surface

def add_grass_details(surface, rect, density=0.01):
    """Adds random grass details and small plants"""
    for _ in range(int(rect.width * rect.height * density)):
        x = rect.x + randint(0, rect.width-1)
        y = rect.y + randint(0, rect.height-1)
        
        # Random grass tufts
        grass_height = randint(3, 8)
        grass_color = (randint(30, 60), randint(160, 200), randint(30, 60))
        
        # Draw a few blades of grass
        for blade in range(3):
            angle = randint(-30, 30)
            end_x = x + math.sin(math.radians(angle)) * grass_height
            end_y = y - math.cos(math.radians(angle)) * grass_height
            pygame.draw.line(surface, grass_color, (x, y), (end_x, end_y), 1)

def create_water_details(surface, rect):
    """Creates natural-looking water with ripples and lily pads"""
    # Add base water texture
    water_base = create_noise_texture(rect.width, rect.height, (0, 100, 255), 30)
    surface.blit(water_base, rect)
    
    # Add ripples
    for _ in range(50):
        center_x = randint(rect.x, rect.x + rect.width)
        center_y = randint(rect.y, rect.y + rect.height)
        radius = randint(10, 30)
        opacity = randint(20, 60)
        ripple_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(ripple_surface, (255, 255, 255, opacity), (radius, radius), radius, 1)
        surface.blit(ripple_surface, (center_x-radius, center_y-radius))
    
    # Add lily pads
    for _ in range(15):
        x = randint(rect.x, rect.x + rect.width - 30)
        y = randint(rect.y, rect.y + rect.height - 30)
        # Lily pad with slight rotation and size variation
        size = randint(15, 25)
        angle = randint(0, 360)
        pad_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.ellipse(pad_surface, (0, 150, 0, 200), pad_surface.get_rect())
        pad_surface = pygame.transform.rotate(pad_surface, angle)
        surface.blit(pad_surface, (x, y))

def create_road(width, height):
    """Creates a more natural-looking road with wear and tear"""
    road = pygame.Surface((width, height))
    
    # Base road color with noise
    base_road = create_noise_texture(width, height, (60, 60, 60), 15)
    road.blit(base_road, (0, 0))
    
    # Add road wear patterns
    for _ in range(100):
        x = randint(0, width-1)
        y = randint(0, height-1)
        wear_size = randint(5, 20)
        wear_color = (randint(70, 80), randint(70, 80), randint(70, 80))
        pygame.draw.circle(road, wear_color, (x, y), wear_size)
    
    # Add cracks
    for _ in range(20):
        start_x = randint(0, width-1)
        start_y = randint(0, height-1)
        for _ in range(randint(3, 8)):
            end_x = start_x + randint(-20, 20)
            end_y = start_y + randint(-20, 20)
            pygame.draw.line(road, (40, 40, 40), (start_x, start_y), (end_x, end_y), 1)
            start_x, start_y = end_x, end_y
    
    # Add worn yellow lines (dashed)
    line_y = height // 2
    dash_length = 50
    dash_gap = 40
    x = 0
    while x < width:
        # Vary dash appearance for wear
        actual_length = dash_length + randint(-5, 5)
        if random() > 0.1:  # 10% chance of missing dash
            line_color = (200, 200, 0) if random() > 0.3 else (180, 180, 0)  # Vary line color
            pygame.draw.rect(road, line_color, (x, line_y-4, actual_length, 8))
        x += dash_length + dash_gap
    
    # Add sidewalks with variation
    sidewalk_height = 20
    for y in [0, height - sidewalk_height]:
        sidewalk = create_noise_texture(width, sidewalk_height, (180, 180, 180), 20)
        # Add some cracks and wear to sidewalk
        for _ in range(30):
            crack_x = randint(0, width-1)
            crack_y = randint(0, sidewalk_height-1)
            pygame.draw.circle(sidewalk, (160, 160, 160), (crack_x, crack_y), randint(1, 4))
        road.blit(sidewalk, (0, y))
    
    return road

def add_bushes(surface, rect, count=8):
    for _ in range(count):
        bush_x = randint(rect.x, rect.x + rect.width - 60)
        bush_y = randint(rect.y, rect.y + rect.height - 40)
        bush_width = randint(40, 60)
        bush_height = randint(30, 40)
        bush_color = (randint(20, 80), randint(120, 180), randint(20, 80))
        pygame.draw.ellipse(surface, bush_color, (bush_x, bush_y, bush_width, bush_height))
        # Add some shadow
        shadow_color = (bush_color[0]//2, bush_color[1]//2, bush_color[2]//2)
        pygame.draw.ellipse(surface, shadow_color, (bush_x+8, bush_y+bush_height//2, bush_width//2, bush_height//3))

def add_litter(surface, rect, count=12):
    for _ in range(count):
        x = randint(rect.x, rect.x + rect.width - 8)
        y = randint(rect.y, rect.y + rect.height - 8)
        color = choice([(200,200,200), (180,180,100), (120,120,120), (220,180,140)])
        pygame.draw.rect(surface, color, (x, y, randint(3,8), randint(2,6)))

def add_muddy_patches(surface, rect, count=6):
    for _ in range(count):
        x = randint(rect.x, rect.x + rect.width - 40)
        y = randint(rect.y, rect.y + rect.height - 20)
        width = randint(20, 40)
        height = randint(10, 20)
        color = (randint(80, 120), randint(60, 80), randint(40, 60))
        pygame.draw.ellipse(surface, color, (x, y, width, height))
        # Add some darker spots
        for _ in range(randint(2, 5)):
            dx = randint(0, width)
            dy = randint(0, height)
            pygame.draw.circle(surface, (60, 40, 30), (x+dx, y+dy), randint(2, 5))

def add_victory_spots(surface, y, count=5, recess_width=60, recess_height=30):
    gap = (SCREEN_WIDTH - count * recess_width) // (count + 1)
    for i in range(count):
        x = gap + i * (recess_width + gap)
        # Draw recess
        pygame.draw.rect(surface, (30, 100, 30), (x, y, recess_width, recess_height), border_radius=12)
        # Draw inner pad
        pygame.draw.ellipse(surface, (0, 180, 0), (x+10, y+8, recess_width-20, recess_height-16))
        # Optional: add a little shadow
        pygame.draw.ellipse(surface, (0, 80, 0), (x+10, y+recess_height-16, recess_width-20, 8))

# Create the main surface
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create and apply grass texture for safe zones
grass_texture = create_noise_texture(SCREEN_WIDTH, SCREEN_HEIGHT, (40, 180, 40), 30)
screen.blit(grass_texture, (0, 0))

# Add grass details to safe zones
add_grass_details(screen, pygame.Rect(0, WATER_END, SCREEN_WIDTH, ROAD_START - WATER_END))
add_grass_details(screen, pygame.Rect(0, ROAD_END, SCREEN_WIDTH, BOTTOM_EDGE - ROAD_END))

# Create and add water section
water_rect = pygame.Rect(0, WATER_START, SCREEN_WIDTH, WATER_END - WATER_START)
create_water_details(screen, water_rect)

# Create and add road
road = create_road(SCREEN_WIDTH, ROAD_END - ROAD_START)
screen.blit(road, (0, ROAD_START))

# Add bushes, litter, and muddy patches to safe zones
add_bushes(screen, pygame.Rect(0, WATER_END, SCREEN_WIDTH, ROAD_START - WATER_END), count=6)
add_bushes(screen, pygame.Rect(0, ROAD_END, SCREEN_WIDTH, BOTTOM_EDGE - ROAD_END), count=4)
add_litter(screen, pygame.Rect(0, ROAD_START, SCREEN_WIDTH, ROAD_END - ROAD_START), count=10)
add_muddy_patches(screen, pygame.Rect(0, ROAD_END, SCREEN_WIDTH, BOTTOM_EDGE - ROAD_END), count=4)

# Add victory spots (recesses) at the top safe zone
add_victory_spots(screen, y=WATER_START-35, count=5, recess_width=60, recess_height=30)

# Save the image
pygame.image.save(screen, "images/background_new.png")
print("New background image saved as 'images/background_new.png'")