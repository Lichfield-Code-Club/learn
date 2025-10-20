import pygame as pg
from control import Control
from menu import Menu
from game import Game
from classes.login import Login

import sys

settings = {
    'size':(1280,960),
    'fps' :60
}
  
app = Control(**settings)
state_dict = {
    'menu': Menu(),
    'game': Game(),
    'login': Login()
}
pg.init()
app.setup_states(state_dict, 'login')
app.main_game_loop()
pg.quit()
sys.exit()