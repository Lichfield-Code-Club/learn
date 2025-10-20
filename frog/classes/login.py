# http://www.codingwithruss.com/pygame/getting-multi-line-text-input-in-pygame/
import pygame as pg
import os
from states import States
from utils import draw_large_text, draw_medium_text, LoadPlayer
from classes.button import Button

class Login(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        self.logged_in = False
        self.login_btn = Button(rect=(10,10,105,25), command=self.validate_login, text='login', **self.btn_settings)
        self.back_btn  = Button(rect=(10,10,105,25), command=self.switch_state, text='back', **self.btn_settings)
        self.play_btn  = Button(rect=(10,10,105,25), command=self.switch_state, text='play', **self.btn_settings)
        self.runs_shown = False

    def get_event(self,event):
        if event.type == pg.QUIT: self.done = True
        if event.type == pg.TEXTINPUT:
            if States.settings['player']['name'] == None:
                States.settings['player']['name'] = ''
            if len(States.settings['player']['name']) < States.settings['player']['max_name_len']:
                States.settings['player']['name'] += event.text
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                States.settings['player']['name'] = States.settings['player']['name'][:-1]
            if event.key == pg.K_ESCAPE: self.done = True
        self.login_btn.get_event(event)
        self.back_btn.get_event(event)
        self.play_btn.get_event(event)

    def update(self, screen, dt):
        self.draw(screen)
    
    def draw(self, screen):
        screen.fill((0,0,255))
        self.draw_name()
        if self.logged_in: 
            self.draw_stats()
            self.draw_play()
        else:
            self.draw_login()

    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('Game startupstuff')

    def validate_login(self):
        player = States.settings['player']
        if player['name'] and len(player['name']) > 0 and len(player['name']) < player['max_name_len']:
            self.logged_in = True
            States.settings = LoadPlayer(States.settings)
        else:
            x = player['name_box_x']
            y = player['name_box_y']
            h = player['name_box_h']
            draw_large_text(States.assets,'Name Invalid','red',x,y+h+20)

    def draw_login(self):
        screen = States.assets['screen']
        player = States.settings['player']
        x = player['name_box_x']
        y = player['name_box_y']
        w = player['name_box_w']
        self.login_btn.rect.x = x 
        self.login_btn.rect.y = y + 50
        self.login_btn.draw(screen)
        self.back_btn.rect.x = x + w - 100
        self.back_btn.rect.y = y + 50
        self.back_btn.draw(screen)
    
    def draw_play(self):
        screen = States.assets['screen']
        player = States.settings['player']
        x = player['history_box_x']
        y = player['history_box_y']
        w = player['history_box_w']
        h = player['history_box_h']
        self.play_btn.rect.x = x 
        self.play_btn.rect.y = y + h + 10
        self.play_btn.draw(screen)
        self.back_btn.rect.x = x + w - 100
        self.back_btn.rect.y = y + h + 10
        self.back_btn.draw(screen)
    
    def draw_name(self):
        PROMPT_COLOUR = (246, 247, 246)
        TEXT_COLOUR = (0, 0, 0)
        player = States.settings['player']
        name = player['name']
        x = player['name_box_x']
        y = player['name_box_y']
        w = player['name_box_w']
        h = player['name_box_h']
        rect = pg.Rect(x,y,w,h)

        prompt = 'Name'
        pg.draw.rect(States.assets['screen'],'white',rect)
        draw_large_text(States.assets,prompt,PROMPT_COLOUR,x-110,y)
        draw_large_text(States.assets,name,TEXT_COLOUR,x+20,y)

    def draw_stats(self):
        player = States.settings['player']
        screen = States.assets['screen']
        TEXT_COLOUR = ['black','green']
        TEXT_COLOUR = ['black','blue']
        x = player['history_box_x']
        y = player['history_box_y']
        w = player['history_box_w']
        h = player['history_box_h']
        rect = pg.Rect(x,y,w,h)

        pg.draw.rect(screen,'white',rect)
        runs = player['runs']
        runs.reverse()
        latest = runs[:5]
        draw_medium_text(States.assets, 'Score', 'white', x      , y - 30)
        draw_medium_text(States.assets, 'Start', 'white', x + 100, y - 30)
        draw_medium_text(States.assets, 'End'  , 'white', x + 400, y - 30)
        for n,run in enumerate(latest):
            draw_medium_text(States.assets,f"{run['score']}" ,TEXT_COLOUR[n%2],x,    600 + (n * 20))
            draw_medium_text(States.assets,f"{run['start']}" ,TEXT_COLOUR[n%2],x+100,600 + (n * 20))
            draw_medium_text(States.assets,f"{run['end']}"   ,TEXT_COLOUR[n%2],x+400,600 + (n * 20))
