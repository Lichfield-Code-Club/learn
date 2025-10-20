import pygame as pg
from states import States
from utils import BaseConfig, GameAssets, draw_zones, log_hit, got_home

class Game(States):
    def __init__(self):
        States.__init__(self)
        if States.settings == None: States.settings = BaseConfig()
        if States.assets   == None: States.assets   = GameAssets(States.settings)
        self.next = 'login'

    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: 
                self.done = True
    def update(self, screen, dt):
        self.draw(screen,dt)

    def draw(self, screen,dt):
        States.assets['backgrounds'].update()
        States.assets['cars'].update()
        States.assets['logs'].update()
        States.assets['frogs'].update()
        draw_zones(States.assets,States.settings)
