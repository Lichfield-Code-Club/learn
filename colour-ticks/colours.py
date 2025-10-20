import pygame
from colorsys import hsv_to_rgb
    
def get_rgb_colour_list(num_colours=5, saturation=1.0, value=1.0):
    rgb_colours = []
    hsv_colours = [[float(x / num_colours), saturation, value] for x in range(num_colours)]
    
    for hsv in hsv_colours:
       hsv = [int(x * 255) for x in hsv_to_rgb(*hsv)]
       rgb_colours.append(hsv)
    
    return rgb_colours

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))

colour_list = get_rgb_colour_list(num_colours=60)
colour_list_index = 0

# Time variables
change_colour_every_ms = 200  # Total time to change from one colour to the next
last_change_time = pygame.time.get_ticks()
increment = 1

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current time
    current_time = pygame.time.get_ticks()

    if (current_time - last_change_time) > change_colour_every_ms:
        last_change_time = current_time
        colour_list_index += increment
        if colour_list_index > len(colour_list) - 1:
            increment = increment * -1
            colour_list_index += increment
        if colour_list_index < 0:
            increment = increment * -1
            colour_list_index += increment

    rgb_colour = colour_list[colour_list_index]


    # Fill the screen with the interpolated colour
    screen.fill(rgb_colour)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
