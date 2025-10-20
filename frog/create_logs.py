def create_logs():
    """Create logs with current level speed"""
    logs = []
    _, _, log_min, log_max = get_level_speeds()
    _, num_logs = get_obstacle_counts()
    
    # Calculate vertical spacing for logs
    water_height = WATER_END - WATER_START
    log_img = pygame.image.load('images/log.png').convert_alpha()
    log_height = log_img.get_rect().height
    
    # Ensure minimum spacing between logs
    usable_height = water_height - (log_height * num_logs)  # Account for log heights
    if usable_height < 0:  # If too many logs for space, adjust number of logs
        num_logs = max(min_logs, water_height // (log_height * 2))  # Ensure minimum number of logs
        usable_height = water_height - (log_height * num_logs)
    
    spacing = usable_height / (num_logs + 1)  # Add 1 to create gaps at top and bottom
    
    for i in range(num_logs):
        rect = log_img.get_rect()
        rect.x = randint(0, SCREEN_WIDTH)
        # Place logs evenly with some randomness within their section
        base_y = WATER_START + (i + 1) * spacing + (i * log_height)
        max_variance = spacing / 2  # Allow some random variation in position
        rect.y = base_y + randint(-int(max_variance), int(max_variance))
        
        # Ensure log stays within water bounds
        rect.y = max(WATER_START, min(WATER_END - log_height, rect.y))
        
        speed = randint(int(log_min * 10), int(log_max * 10)) / 10  # Convert to float
        new_log = {'img': log_img, 'rect': rect, 'speed': speed}
        logs.append(new_log)
    
    return logs