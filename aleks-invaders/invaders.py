import pygame

large_alien_file = 'assets/LargeAlien.png'
#shoot_sound_file = 'assets/Falling_putter.ogg'
shoot_sound_file = 'assets/shot.wav'
background_file  = "assets/background.png"
spaceship_file   = "assets/spaceship.png"
#missile_file     = "assets/missile2.png"
missile_file     = "assets/bullet.png"

foe1=pygame.image.load(large_alien_file)
foe1=pygame.transform.scale(foe1,(47,34))

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800
pygame.mixer.init()
shoot_sound=pygame.mixer.Sound(shoot_sound_file)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Spacey')

rows,cols=5,5

red=(255,0,0)
green=(0,255,0)

bg = pygame.image.load(background_file)
bg = pygame.transform.scale(bg,(screen_width,screen_height))
def draw_bg():
	screen.blit(bg, (0, 0))
	
class ship(pygame.sprite.Sprite):
	def __init__(self, x,y,health):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(spaceship_file)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y] 
		self.health_start=health
		self.health_remain=health
		self.last_shot=pygame.time.get_ticks()

	def update(self):
		speed=8
		cooldown=500

		key=pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left>=0:
			self.rect.x-=speed
		if key[pygame.K_RIGHT] and self.rect.right<screen_width:
			self.rect.x+=speed
		time_now = pygame.time.get_ticks()
		if key[pygame.K_SPACE] and time_now-self.last_shot>cooldown:
			bullet=bullets(self.rect.centerx,self.rect.top)
			bullet_group.add(bullet)
			self.last_shot = time_now
			shoot_sound.play()


		#healthbar
		pygame.draw.rect(screen,red,(self.rect.x,(self.rect.bottom+10),self.rect.width,15))
		if self.health_remain>0:
			pygame.draw.rect(screen,green,(self.rect.x,(self.rect.bottom+10),int(self.rect.width*(self.health_remain/self.health_start)),15))
class bullets(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(missile_file)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y] 

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom<0:
			self.kill
class aliens(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image= foe1 
		self.rect = self.image.get_rect()
		self.rect.center=[x,y]
	def update(self):
		pass
	
spaceship_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
alien_group=pygame.sprite.Group()

def create_aliens():
	for number in range(rows):
		for item in range(cols):
			alien=aliens(100+item*100,100+number*70)
			alien_group.add(alien)

create_aliens()

	
spaceship=ship(int(screen_width/2),screen_height-100,3)
spaceship_group.add(spaceship)

run = True
# Main game loop - comment added for Git demo.
# and this one
while run:
	clock.tick(fps)
	draw_bg()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	spaceship.update()
	bullet_group.update()
	alien_group.update()
	pygame.display.update()
	
pygame.quit()