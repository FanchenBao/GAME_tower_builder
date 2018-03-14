import pygame
from pygame.sprite import Sprite
from random import randint


class Block(Sprite):
	def __init__(self, screen, ai_settings, index):
		super().__init__()
		'''initialize block and determine its original position on screen'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = self.screen.get_rect()

		# a flag indicating whether the block has been dropped
		self.drop = False

		# determine the block's fulcrum position (left or right or none in terms of perfection match)
		# and record fulcrum's x coordinate, except the first block
		self.fulcrum_position = "none"
		self.fulcrum_x = 0

		# store the cumulative leverage of each block, except the first block
		self.sum_leverage = 0
		# store the initial leverage when block first lands
		self.ini_leverage = 0
		
		# flag indicating whether a built block has tipped over and ready to fall
		self.fall = False

		# indexing each block
		self.index = index

		self.x_speed = float(ai_settings.horizontal_speed)
		self.y_speed = 0
		self.shift_frequency = float(ai_settings.shift_frequency)
		
		#load the block image
		self.image = pygame.image.load('images/block.bmp')

		#get block rect
		self.rect = self.image.get_rect()
		
		# new block initial position (actual position is random)
		# also avoid appearing too close to the edge, might result in bug
		self.rect.x = randint(5, self.screen_rect.right - self.rect.width - 5)
		self.rect.y = 0

		# store a decimal value for rock's location for fine tuning position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
	def check_edges(self, left_edge, right_edge):
		'''check whether the block has hit the left or right edge'''
		if self.rect.left <= left_edge:
			return True
		elif self.rect.right >= right_edge:
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
			# remember, everytime the program runs this script, it can be considered unit time (or dt)
			self.y_speed += self.ai_settings.g
			self.y += self.y_speed
		
		self.x += self.x_speed * self.ai_settings.block_direction
		
		# reassign position to rock rect
		self.rect.x = self.x
		self.rect.y = self.y

	def shift(self, shift_range):
		''' update the shifting of built blocks'''
		x_shift_speed = shift_range / (1 / self.shift_frequency)
		self.x += x_shift_speed * self.ai_settings.block_shift_direction
		self.rect.x = self.x
		

	def blitme(self):
		''' draw the alien at its current location'''
		self.screen.blit(self.image, self.rect)