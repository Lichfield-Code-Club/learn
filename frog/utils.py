import pygame as pg
import yaml
import os
from datetime import datetime
from classes.backgrounds import Background
from classes.frogs import Frog
from classes.cars import Car
from classes.logs import Log

def BaseConfig():
    fpath = 'game_config.yaml'
    with open(fpath,'r') as fr:
        config = yaml.safe_load(fr)
        return config

def GameAssets(config):
    pg.mixer.init()
    pg.font.init()
    assets = {
            'backgrounds': pg.sprite.Group(),
            'frogs':       pg.sprite.Group(),
            'cars':        pg.sprite.Group(),
            'logs':        pg.sprite.Group(),
            'screen':      pg.display.get_surface(),
            'clock':       pg.time.Clock(),
            'large_text':  pg.font.SysFont(config['large_text_font'],config['large_text_size']),
            'medium_text': pg.font.SysFont(config['medium_text_font'],config['medium_text_size']),
            'small_text':  pg.font.SysFont(config['small_text_font'],config['small_text_size'])
            }
    [assets['backgrounds'].add(Background(config,assets['screen'],id)) for id in range(config['num_backgrounds'])]
    [assets['frogs'].add(Frog(config,assets['screen'],id)) for id in range(config['num_frogs'])]
    [assets['cars'].add(Car(config,assets['screen'],id)) for id in range(config['num_cars'])]
    [assets['logs'].add(Log(config,assets['screen'],id)) for id in range(config['num_logs'])]
    return assets

def draw_large_text(assets,text, text_colour, x, y):
    screen = assets['screen']
    font = assets['large_text']
    img = font.render(text, True, text_colour)
    width = img.get_width()
    screen.blit(img, (x,y))
    return width

def draw_small_text(assets,text, text_colour, x, y):
    screen = assets['screen']
    font = assets['small_text']
    img = font.render(text, True, text_colour)
    width = img.get_width()
    screen.blit(img,(x,y))
    return width

def draw_medium_text(assets,text, text_colour, x, y):
    screen = assets['screen']
    font = assets['medium_text']
    img = font.render(text, True, text_colour)
    width = img.get_width()
    screen.blit(img,(x,y))
    return width

def draw_text(screen,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_line(assets, prefix,start,end):
    msg = f"{prefix}: start: {start} ---------------------------------------------------"
    draw_text(assets['screen'],msg,assets['medium_text'], 'white', 40, start)
    msg = f"{prefix}   end: {end} ---------------------------------------------------"
    draw_text(assets['screen'],msg,assets['medium_text'], 'white', 40, end)

def draw_zones(assets,settings):
    draw_line(assets,'base',settings['base_start'],settings['base_end'])
    draw_line(assets,'road',settings['road_start'],settings['road_end'])
    draw_line(assets,'water',settings['water_start'],settings['water_end'])
    #pg.mixer.music.load(config['road_noise_fpath'])
    #pg.mixer.music.set_volume(config['road_noise_volume'])
    #pg.mixer.music.play(-1,config['road_noise_volume'])    

def SaveConfig(config,fpath):
    config['clock'] = None
    with open(fpath,'w') as fw:
        yaml.dump(config['cars'],fw)

def SavePlayer(config):
    fpath = config['player']['fpath']
    backup = f'{fpath}.backup'
    if os.path.exists(fpath):
        os.replace(fpath,backup)
    with open(fpath,'w') as fw:
        yaml.dump(config,fw)

def LoadPlayer(config):
    player = config['player']
    fpath = f"players/{player['name']}.yaml"
    if not os.path.exists(fpath):
        config['player']['fpath'] = fpath
        SavePlayer(config)
    if os.path.exists(fpath):
        with open(fpath,'r') as fr:
            config = yaml.safe_load(fr)
    return config

def log_hit(assets,settings):
    hit = None
    for frog in assets['frogs']:
        if frog.rect.y >= settings['water_end'] and frog.rect.y <= settings['water_start']:
            if pg.sprite.spritecollide(frog, assets['logs'], False):
                hit = True
    return hit

def got_home(assets,settings):
    hit = None
    for frog in assets['frogs']:
        if frog.rect.y <= settings['water_end']:
            hit = True
    return hit

def tstamp():
    dt = datetime.now()
    dt_string = dt.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string