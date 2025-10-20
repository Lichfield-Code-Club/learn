import pygame as pg

pg.font.init()

class States(object):
    settings = None
    assets = None

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.btn_settings = {
        "clicked_font_color" : (0,0,0),
        "hover_font_color"   : (205,195, 100),
        'font'               : pg.font.Font(None,16),
        'font_color'         : (0,0,0),
        'border_color'       : (0,0,0),
        }

    def switch_state(self):
        self.done = True