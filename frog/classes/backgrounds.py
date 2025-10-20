import pygame
from random import randint

class Background(pygame.sprite.Sprite):
    def __init__(self,config,screen,id):
        super().__init__()

        self.id      = id
        self.screen  = screen
        self.fpath   = config['background_image_fpath']
        self.surface = pygame.image.load(self.fpath).convert_alpha()
        self.rect    = self.surface.get_rect()
        self.rect.x  = 0
        self.rect.y  = 0

    def update(self):
        self.draw()
        
    def draw(self):
        self.screen.blit(self.surface,(self.rect.x, self.rect.y))

    def move(self,config):
        pass
    