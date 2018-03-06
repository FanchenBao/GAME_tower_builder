import pygame
from pygame.sprite import Sprite
from random import randint


class Block(Sprite):
	def __init__(self, screen, ai_settings):
		super().__init__()
		'''initialize block and determine its original position on screen'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = self.screen.get_rect()

		# a flag indicating whether the block has been dropped
		self.drop = False
		
		
		self.x_speed = float(ai_settings.horizontal_speed)
		self.y_speed = 0
		#load the block image
		self.image = pygame.image.load('images/block.bmp')

		#get block rect
		self.rect = self.image.get_rect()
		
		# new block initial position (actual position is random)
		self.rect.x = randint(0, self.screen_rect.right - self.rect.width)
		self.rect.y = 0

		# store a decimal value for rock's location for fine tuning position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
	def check_edges(self):
		'''check whether the block has hit the left or right edge'''
		if self.rect.left <= 0:
			return True
		elif self.rect.right >= self.screen_rect.right:
			return True
		else:
			return False

	def update(self):
		''' update current rock position'''
		if not self.drop:
			# if block is not dropped, it moves side to side at the top
			self.y = 0
		else:
			# if block is dropped, it falls freely with regular g while maintaining the horizontal speed
			self.y_speed += self.ai_settings.g
			self.y += self.y_speed
		
		self.x += self.x_speed * self.ai_settings.block_direction
		
		# reassign position to rock rect
		self.rect.x = self.x
		self.rect.y = self.y

		

	def blitme(self):
		''' draw the alien at its current location'''
		self.screen.blit(self.image, self.rect)