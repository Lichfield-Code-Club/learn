# Frogger Game Logic

## Game Overview
This is a recreation of the classic Frogger arcade game where players guide a frog across a hazardous road and river to reach safety at the top of the screen.

## Screen Layout
The game screen is divided into several zones from bottom to top:
- Safe Zone (Bottom): Starting area for the frog
- Road Zone (Middle): Contains moving cars
- Water Zone (Top): Contains moving logs
- Victory Zone (Very Top): The goal area

## Game Objects

### Frog
- Controlled by arrow keys (Up, Down, Left, Right)
- Movement speed: 10 pixels per keypress
- Can move in all four directions within screen boundaries
- Must ride logs to cross water
- Dies upon collision with cars or falling into water

### Cars
- Number of cars: 10
- Random spawn positions on the road (y: 500-780 pixels)
- Random speeds: 2-10 pixels per frame (moving left)
- Wrap around screen edges
- Collision with frog is fatal

### Logs
- Number of logs: 50
- Random spawn positions in water (y: 100-360 pixels)
- Random speeds: 2-5 pixels per frame (moving right)
- Wrap around screen edges
- Frog must use these to cross water safely

## Core Game Mechanics

### Movement System
```python
# Frog movement with boundary checks
if keys[pygame.K_LEFT]: 
    if frog_rect.x - frog_speed > 0: 
        frog_rect.x -= frog_speed
# Similar for other directions
```

### Collision Detection
```python
# Car collision
if frog_rect.colliderect(car['rect']):
    print('Frog Collided with car')
    # Should reset frog position

# Log collision (required for water survival)
if frog_rect.colliderect(log['rect']):
    print('Frog Collided with log')
    # Should move frog with log
```

### Victory Condition
```python
if frog_rect.y < frog_rect.height + 10:
    print('Frog made it','WINNER')
    # Should reset frog for next attempt
```

## Game States
The game can be in one of several states:
1. Playing: Normal gameplay
2. Collision: When frog hits a car or falls in water
3. Victory: When frog reaches the top
4. Game Over: When quitting the game

## Improvement Areas
Current version (`step11.py`) has room for enhancement:

1. **Death Mechanics**
   - Currently only prints messages for collisions
   - Should reset frog position after death
   - Could add death animation or delay

2. **Log Riding**
   - Logs move but don't carry the frog
   - Should make frog move with log when in contact

3. **Water Physics**
   - No consequence for being in water without a log
   - Should reset frog if in water without log support

4. **Score System**
   - Could add points for:
     - Successfully crossing road
     - Reaching the top
     - Time-based bonuses

5. **Visual Feedback**
   - Could add animations for:
     - Death
     - Victory
     - Log riding
     - Water splashes

## Technical Implementation

### Game Loop
The main game loop handles:
1. Event processing (quit and keyboard input)
2. Game object updates (movement of cars and logs)
3. Collision detection
4. Screen drawing

### Movement Patterns
- Cars move left at varying speeds
- Logs move right at varying speeds
- All objects wrap around screen edges
```python
# Object wrapping logic
if object_rect.x > SCREEN_WIDTH: object_rect.x = 0
if object_rect.x < 0: object_rect.x = SCREEN_WIDTH
```

### Frame Rate Control
- Game runs at 60 FPS (frames per second)
- Movement speeds are balanced for this frame rate
- Clock ensures consistent game speed across different systems

## Future Enhancements
Potential improvements for future versions:
1. Multiple lives system
2. Score display
3. Multiple levels with increasing difficulty
4. Sound effects
5. Power-ups
6. Multiple frogs (multiplayer)
7. Time limit per level
8. High score system