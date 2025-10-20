import pygame as pg
from random import randint
from states import States

class Frog(pg.sprite.Sprite):
    def __init__(self,config,screen,id):
        super().__init__()

        self.id      = id
        self.screen  = screen
        self.config  = config
        self.fpath   = self.config['frog_image_fpath']
        self.surface = pg.image.load(self.fpath).convert_alpha()
        self.rect    = self.surface.get_rect()
        self.mask    = pg.mask.from_surface(self.surface)
        self.rect.x, self.rect.y = self.init_coords()
        self.min_y   = 0
        self.max_y   = self.config['screen_height'] - self.rect.height
        self.min_x   = 0
        self.max_x   = self.config['screen_width'] - self.rect.width
        self.initial_rect = self.rect
        self.speed   = randint(self.config['frog_min_speed'], self.config['frog_max_speed'])
        self.jump_fx = self.config['frog_jump_sound']
        self.jump_speed   = self.config['frog_jump_speed']
        self.loghit  = False
        self.log_miss_img = pg.image.load(States.settings['car_crash_fpath']).convert_alpha()
        self.log_miss_fx = None
        self.log_miss_rect = self.log_miss_img.get_rect()
        self.log_miss_time = 0
        self.carhit  = False
        self.car_crash_img = pg.image.load(States.settings['car_crash_fpath']).convert_alpha()
        self.car_crash_fx = None
        self.car_crash_rect = self.car_crash_img.get_rect()
        self.car_crash_time = 0

    def init_coords(self):
        x = randint(self.rect.width,self.config['screen_width'] - self.rect.width)
        y = randint(self.config['base_end'], self.config['base_start'] - self.rect.height)
        return x,y
    
    def update(self):
        if self.rect.y >= States.settings['road_end'] and self.rect.y <= States.settings['road_start']:
            if not self.carhit:
                self.carhit = self.car_hit()
                self.move()
                self.car_crash_time = pg.time.get_ticks()
            if self.carhit:
                if pg.time.get_ticks() < self.car_crash_time + 5000:
                    self.car_crash_animate()
                else:
                    self.rect.x, self.rect.y = self.init_coords()
                    self.carhit = False
        if self.rect.y >= States.settings['water_end'] and self.rect.y <= States.settings['water_start']:
            if self.log_hit(): self.move()
            else:
                print('Frog missed a log')
                # allow frog to move until miss logic worked out
                self.move()

            #    self.loghit = self.log_hit()
            #    self.log_miss_time = pg.time.get_ticks()
            #if not self.loghit:
            #    if pg.time.get_ticks() < self.log_miss_time + 5000:
            #        self.log_miss_animate()
            #    else:
            #        self.rect.x, self.rect.y = self.init_coords()
            #        self.loghit = False
            pass
        if self.rect.y <= States.settings['water_end'] :
            print('SUCCESS!!!')
        else:
            self.move()
        self.draw()

    def draw(self):
        self.screen.blit(self.surface,(self.rect.x, self.rect.y))

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and keys[pg.K_LSHIFT]:
            jump = 2 * self.jump_speed
            if self.rect.y - jump > self.min_y: self.rect.y -= jump
        else:
            jump = self.speed
            if self.rect.y - jump > self.min_y and keys[pg.K_UP]: self.rect.y -= jump
            if self.rect.y + jump < self.max_y and keys[pg.K_DOWN]: self.rect.y += jump
            if self.rect.x - jump > self.min_x and keys[pg.K_LEFT]: self.rect.x -= jump
            if self.rect.x + jump < self.max_x and keys[pg.K_RIGHT]: self.rect.x += jump    

    def car_hit(self):
        if pg.sprite.spritecollide(self, States.assets['cars'], False):
            return True
        return False

    def log_hit(self):
        hit = False
        for frog in States.assets['frogs']:
            if frog.rect.y >= States.settings['water_end'] and frog.rect.y <= States.settings['water_start']:
                if pg.sprite.spritecollide(frog, States.assets['logs'], False):
                    print('Frog landed on a log')
                    hit = True
        return hit

    def car_crash_animate(self):
        self.screen.blit(self.car_crash_img,self.rect.topleft)

    def log_miss_animate(self):
        self.screen.blit(self.log_miss_img,self.rect.topleft)
