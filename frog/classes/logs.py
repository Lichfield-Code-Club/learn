import pygame
from random import randint

class Log(pygame.sprite.Sprite):
    def __init__(self,config,screen,id):
        super().__init__()

        self.id      = id
        self.screen  = screen
        self.config  = config
        self.fpath   = config['log_image_fpath']
        self.surface = pygame.image.load(self.fpath).convert_alpha()
        self.jump_fx = config['log_jump_sound']
        self.speed   = randint(config['log_min_speed'],config['log_max_speed'])
        self.rect    = self.surface.get_rect()
        self.mask    = pygame.mask.from_surface(self.surface)
        self.rect.x, self.rect.y = self.init_coords()
        self.initial_rect = self.rect

    def init_coords(self):
        x = randint(self.rect.width,self.config['screen_width'] - self.rect.width)
        y = randint(self.config['water_end'], self.config['water_start'] - self.rect.height)
        return x,y

    def update(self):
        self.draw()
        self.move()

    def draw(self):
        self.screen.blit(self.surface,(self.rect.x, self.rect.y))

    def move(self):
        if self.rect.x - self.speed > 0:
            self.rect.x -= self.speed
        else:
            self.rect.x = self.config['screen_width']
