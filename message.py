import pygame
from pygame.sprite import Sprite


class Message(Sprite):
	def __init__(self, screen, ai_settings, flag):
		super().__init__()
		'''initialize message and determine its original position on screen'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = self.screen.get_rect()
		self.flag = flag

		self.time = 0

		if flag == 'perfect':
			self.image = pygame.image.load('images/perfect.bmp')
		if flag == 'good':
			self.image = pygame.image.load('images/good.bmp')

		self.rect = self.image.get_rect()
		self.rect.centery = self.screen_rect.centery
		self.rect.right = self.screen_rect.right - 20


		

	def blitme(self):
		''' draw the alien at its current location'''
		self.screen.blit(self.image, self.rect)