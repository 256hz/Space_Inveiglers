# import the pygame module, so you can use it
import pygame, os.path, random
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
transparent_color = (255, 0, 5)
screen_res = (640, 480)
SCREENRECT = pygame.Rect(0, 0, screen_res[0], screen_res[1])
BADGUY_RELOAD = 12	 

def load_image(file):
	'''loads an image, prepares it for play'''
	file = os.path.join(main_dir, 'images', file)
	surface = pygame.image.load(file)
	surface.set_colorkey(transparent_color)
	return surface.convert()

def load_images(*files):
	'''sends multiple images to load_image'''
	imgs = []
	for file in files:
		imgs.append(load_image(file))
	return imgs

class Player(pygame.sprite.Sprite):
	'''dats u'''
	speed = 10
	bounce = 24
	images = []
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
		self.reloading = 0
		self.origtop = self.rect.top

	def move(self, direction):
		self.rect.move_ip(direction*self.speed, 0)
		self.rect = self.rect.clamp(SCREENRECT)
		self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

class Badguy(pygame.sprite.Sprite):
	speed = 5
	animcycle = 12
	images = []
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		# pick a random badguy to be
		self.image = self.images[random.randint(0,4)-1] 
		self.rect = self.image.get_rect()
		self.frame = 0
		self.direction = 1

	def update(self):
		self.rect.move_ip(self.direction*self.speed, 0)
		if not SCREENRECT.contains(self.rect):
			# classic centipede motion
			self.rect.top = self.rect.bottom + 5
			self.direction = -1 * self.direction
			self.rect = self.rect.clamp(SCREENRECT)
			if self.rect.bottom >= screen_res[1]:
				self.kill()
		
def main():
	pygame.init()
	
	# set resolution, decorate window
	screen = pygame.display.set_mode(screen_res)
	logo = load_image('logo32x32.png')
	pygame.display.set_icon(logo)
	pygame.display.set_caption('SPACE INVEIGLERS')
	
	running = True
	
	# load images, assign sprites
	background = load_image('background.png')
	Player.image = load_image('playerlg.png')
	Badguy.images = load_images('badguy1lg.png', 'badguy2lg.png', 'badguy3lg.png', 'badguy4lg.png')

	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	# init game groups
	badguys = pygame.sprite.Group()
	all = pygame.sprite.RenderUpdates()

	# assign default groups to each sprite class
	Player.containers = all
	Badguy.containers = badguys, all
	badguyreload = BADGUY_RELOAD
	clock = pygame.time.Clock()

	#initialize our starting sprites
	player = Player()
	Badguy() #note, this 'lives' because it goes into a sprite group
	
	# main loop
	while player.alive():
		screen.blit(background, (0,0))
		#get input
		for event in pygame.event.get():
			if event.type == QUIT or \
				(event.type == KEYDOWN and event.key == K_ESCAPE):
					return
		keystate = pygame.key.get_pressed()

		# clear/erase the last drawn sprites
		all.clear(screen, background)

		#update all the sprites
		all.update()

		#handle player input
		direction = keystate[K_RIGHT] - keystate[K_LEFT]
		player.move(direction)

		# Create new badguy
		if badguyreload:
			badguyreload = badguyreload - 1
		elif not int(random.random() * 50):
			Badguy()
			badguyreload = BADGUY_RELOAD

		#draw the scene
		screen.blit(background, (0,0))
		dirty = all.draw(screen)
		pygame.display.update(dirty)

		#cap the framerate
		clock.tick(40)
	 
	 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()