import turtle as t
from turtle import Screen
import os
import datetime

##############################################################################################
# Function definitions
##############################################################################################
def GetCoordinates(startx, starty, line_length,forward_amount):
    coordinates = []
    t.penup()
    t.goto(startx,starty)
    coordinates.append(t.pos())

    for x in range(180): # Draw right arc
        t.forward(forward_amount)
        t.left(1)
        coordinates.append(t.pos())

    t.forward(line_length) # Draw top line
    coordinates.append(t.pos())

    for x in range(180): # Draw left arc
        t.forward(forward_amount)
        t.left(1)
        coordinates.append(t.pos())

    t.forward(line_length) # draw bottom line
    coordinates.append(t.pos())

    return coordinates

def DigitCoordinates():
    coordinates = []
    coordinates.append(( -10, -245)) # 1 o'clock
    coordinates.append(( 120, -245)) # 2 o'clock
    coordinates.append(( 240, -235)) # 3 o'clock
    coordinates.append(( 340, -195)) # 4 o'clock
    coordinates.append(( 420, -105)) # 5 o'clock
    coordinates.append(( 446,  -25)) # 6 o'clock
    coordinates.append(( 430,   85)) # 7 o'clock
    coordinates.append(( 370,  195)) # 8 o'clock
    coordinates.append(( 280,  255)) # 9 o'clock
    coordinates.append(( 140,  275)) # 10 o'clock
    coordinates.append(( -10,  275)) # 11 o'clock
    coordinates.append((-140,  275)) # 12 o'clock
    coordinates.append((-260,  265)) # 13 o'clock
    coordinates.append((-360,  215)) # 14 o'clock
    coordinates.append((-440,   85)) # 15 o'clock
    coordinates.append((-460,  -25)) # 16 o'clock
    coordinates.append((-420, -125)) # 17 o'clock
    coordinates.append((-350, -195)) # 18 o'clock
    coordinates.append((-260, -235)) # 19 o'clock
    coordinates.append((-140, -245)) # 20 o'clock
    return coordinates

def DrawClock(coordinates):
    first_y = coordinates[0][1]

    t.penup()
    t.fillcolor(seconds_day_colour)
    t.home()
    t.begin_fill()
    for coord in coordinates[81:280]:
        x = coord[0]
        y = coord[1]
        if x >= 0 and y >= 0:
            t.goto(coord)
        elif x <= 0 and y >= 0:
            t.goto(coord)
        elif x >= 0 and y <=0:
            t.goto(x,0)
        elif x <= 0 and y <= 0:
            t.goto(x,0)
        else:
            print(coord)
    t.home()
    t.end_fill()

    t.fillcolor(day_draw_colour)
    t.home()
    t.begin_fill()
    for coord in coordinates[270:361]:
        if coord[1] < 1:
            t.goto(coord)
    t.goto(0,first_y)
    t.end_fill()

    t.fillcolor(day_draw_colour)
    t.begin_fill()
    t.home()
    t.goto(0,first_y)
    for coord in coordinates[10:89]:
        if coord[1] < 0:
            t.goto(coord)
    t.home()
    t.end_fill()

def DrawHours(coordinates):
    for hour,coord in enumerate(coordinates): 
        t.penup()
        t.goto(coord)
        t.pendown()
        t.write(f'{hour+1}',font=(fixed_font, 24, 'normal', 'bold', 'italic'))
        t.penup()
    t.home()

def DrawOval(coordinates):
    t.width(12)
    t.penup()
    t.goto(coordinates[0])
    t.pendown()
    for coord in coordinates:
        x = coord[0]
        y = coord[1]
        if y < 1 : # Night time
            t.color(night_draw_colour)
        else:
            t.color(day_draw_colour)
        t.goto(coord)
    t.penup()

def MinutesTick(coord,colour):
    MinutesHand.penup()
    MinutesHand.goto(coord)
    MinutesHand.color(colour)
    MinutesHand.circle(second_hand_radius)

def SecondsTick(coord,colour):
    SecondsHand.penup()
    SecondsHand.goto(coord)
    SecondsHand.color(colour)
    SecondsHand.circle(second_hand_radius)

def DigitalDisplay(hours,minutes,seconds):
    time_now = f'{hours:02}:{minutes:02}:{seconds:03}'
    fixed_font = 'Courier'

    DigitalFrame.clear()
    DigitalFrame.penup()
    DigitalFrame.goto(DigitalFrame_x,DigitalFrame_y)
    DigitalFrame.write(f'{time_now}',font=(fixed_font, 32, 'normal', 'bold', 'italic'))
    DigitalFrame.home()

def DigitalTime():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_now = (now - midnight).seconds

    seconds_per_hour = seconds_per_minute * minutes_per_hour

    current_hour    = int(seconds_now / seconds_per_hour)
    seconds_till_hour = current_hour * seconds_per_hour
    seconds_remaining = seconds_now - seconds_till_hour
    current_minutes = int(seconds_remaining / seconds_per_minute)
    current_seconds = int(seconds_remaining % seconds_per_minute)
    return current_hour, current_minutes, current_seconds

def DrawButton():
    ExitButton.penup()
    ExitButton.goto(ExitButton_x,ExitButton_y)
    ExitButton.pendown()
    ExitButton.forward(ExitButton_w)
    ExitButton.left(90)
    ExitButton.forward(ExitButton_h)
    ExitButton.left(90)
    ExitButton.forward(ExitButton_w)
    ExitButton.left(90)
    ExitButton.forward(ExitButton_h)
    ExitButton.penup()
    ExitButton.goto(ExitButton_x+20,ExitButton_y+10)
    ExitButton.pendown()
    ExitButton.write('EXIT',font=(fixed_font, 24, 'normal', 'bold', 'italic'))
    ExitButton.penup()

# method to perform action
def ButtonFunc(x, y):
    global RunClock
    if x >= ExitButton_x and x <= ExitButton_x + ExitButton_w and y >= ExitButton_y and y <= ExitButton_y + ExitButton_h:
        RunClock = False

def mapRange(value, inMin, inMax, outMin, outMax):
    mapped = outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))
    intval = int(mapped)
    return intval

def main():
    OuterCoordinates = GetCoordinates(200,-250,400,5) # Outer oval
    HoursCoordinates = GetCoordinates(180,-190,350,4) # Hour oval
    MinutesCoordinates = HoursCoordinates # same number of hours and minutes
    SecondsCoordinates = GetCoordinates(150,-130,300,3) # Seconds oval
    DigitsCoordinates = DigitCoordinates()

    NumMinutesCordinates = len(MinutesCoordinates)
    NumSecondsCoordinate = len(SecondsCoordinates)
    NumDigitsCoordinates = len(DigitsCoordinates)

    s.onclick(ButtonFunc)
    DrawButton()
    
    DrawClock(OuterCoordinates)
    DrawOval(OuterCoordinates) # Outer oval
    DrawOval(HoursCoordinates) # Hours oval
    DrawOval(SecondsCoordinates) # Minutes oval
    DrawHours(DigitsCoordinates)

    prev_seconds = None
    minutes_draw_colour = None
    seconds_draw_colour = None
    prev_coord = None
    prev_seconds_index = None
    prev_seconds_coord = None
    prev_minutes_coord = None
    prev_minutes_index = None

    while RunClock == True:
        hours,minutes,seconds = DigitalTime()
        seconds_index = mapRange(seconds,0,seconds_per_minute,0,NumSecondsCoordinate -1)
        seconds_coord = SecondsCoordinates[seconds_index]
        #minutes_index = mapRange(minutes,0,minutes_per_hour,0,NumMinutesCordinates - 1)
        minutes_index = mapRange(minutes,0,minutes_per_hour,0,NumDigitsCoordinates - 1)
        minutes_coord = DigitsCoordinates[minutes_index]

        if minutes < 6 or minutes > 16: 
            minutes_draw_colour = minutes_night_colour
            seconds_draw_colour = seconds_night_colour
        else: 
            minutes_draw_colour = minutes_tick_colour
            seconds_draw_colour = seconds_tick_colour

        if not prev_seconds or prev_seconds != seconds:
            DigitalDisplay(hours,minutes,seconds)
            prev_seconds = seconds

        if not prev_seconds_index or seconds_index != prev_seconds_index:
            if prev_seconds_coord: SecondsTick(prev_seconds_coord,day_draw_colour)
            if seconds_coord: SecondsTick(seconds_coord,seconds_draw_colour)
            prev_seconds_index = seconds_index

        if not prev_minutes_index or minutes_index != prev_minutes_index:
            if prev_coord: MinutesTick(prev_minutes_coord,minutes_night_colour)
            MinutesTick(minutes_coord,minutes_draw_colour)
            prev_minutes_index = minutes_index

        prev_minutes_coord = minutes_coord
        prev_seconds_coord = seconds_coord

##############################################################################################
# Main part of script
##############################################################################################
hours_per_day = 20
minutes_per_hour = 20
seconds_per_day = 86400

seconds_per_hour = int(seconds_per_day / hours_per_day)
seconds_per_minute = int(seconds_per_hour / minutes_per_hour)

period = seconds_per_minute / hours_per_day
period = 0.1 # debug ... go faster

background_colour = 'White'
night_draw_colour = 'Yellow'
day_draw_colour = 'Black'

seconds_tick_colour = 'Red'
seconds_day_colour = 'Cyan'
seconds_night_colour = 'Cyan'

minutes_tick_colour = 'Blue'
minutes_day_colour = 'Red'
minutes_night_colour = 'Cyan'

second_hand_radius = 50.0
fixed_font = 'Courier'

minutes_night_colour = 'Green'
minutes_day_colour = 'Blue'

MinutesHand = t.Turtle()
MinutesHand.width(4)
MinutesHand.shape("circle")

SecondsHand = t.Turtle()
SecondsHand.width(4)
SecondsHand.shape("circle")

DigitalFrame = t.Turtle()
DigitalFrame.width(4)
DigitalFrame.shape("circle")
DigitalFrame_x = -100
DigitalFrame_y = 10

ExitButton = t.Turtle()
ExitButton.width(4)
ExitButton.shape('classic')
ExitButton_x = -520
ExitButton_y = 280
ExitButton_w = 120
ExitButton_h = 60

s = Screen()
s.delay(0.0001)
s.title("CLock 2 by Oats Jenkins")
s.bgcolor(background_colour)
s.setup(width=1080,height=720)

RunClock = True

main()
