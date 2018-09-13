'''
Author: Fanche Bao
Date: 03/10/2018

Description:
ScoreBoard class, prepare messages for display
'''

import pygame.font
from pygame.sprite import Group
from block import Block

class ScoreBoard():
	''' a class to record and draw scores on the screen'''
	
	def __init__(self, screen, ai_settings, stats, sc_blocks):
		''' initialize scoreboard'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.stats = stats
		self.sc_blocks = sc_blocks

		self.screen_rect = screen.get_rect()

		# setting font for score
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 24)

		# draw score information on the screen
		self.prep_score()
		self.prep_block()
		self.prep_max_block()
		self.prep_high_score()
		self.prep_falls_left()

	def prep_falls_left(self):
		self.sc_blocks.empty()
		for fall in range(self.stats.falls_left):
			sc_block = Block(self.screen, self.ai_settings, 0, True)
			sc_block.rect.top = 5
			sc_block.rect.left = fall * sc_block.rect.width + 5
			self.sc_blocks.add(sc_block)

	def prep_score(self):
		''' convert score information into image'''
		# round the score to the nearest 10 (if the second argument is 1, that means to ronud to nearest 0.1)
		rounded_score = round(self.stats.score, -1)
		# syntax to insert comma to long number
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.score_image_rect = self.score_image.get_rect()
		self.score_image_rect.right = self.screen_rect.right - 10
		self.score_image_rect.top = 5

	def prep_high_score(self):
		''' convert score information into image'''
		rounded_score = round(self.stats.high_score, -1)
		# syntax to insert comma to long number
		high_score_str = "High Score: " + "{:,}".format(rounded_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.high_score_image_rect = self.high_score_image.get_rect()
		self.high_score_image_rect.centerx = self.screen_rect.centerx
		self.high_score_image_rect.top = 5

	def prep_block(self):
		''' convert maximum blocks achieved into image'''
		block_str = "Blocks: " + str(self.stats.number_block)
		self.block_image = self.font.render(block_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.block_image_rect = self.block_image.get_rect()
		self.block_image_rect.right = self.screen_rect.right - 10
		self.block_image_rect.top = 35

	def prep_max_block(self):
		''' convert maximum blocks achieved into image'''
		max_block_str = "Max Blocks: " + str(self.stats.max_block)
		self.max_block_image = self.font.render(max_block_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.max_block_image_rect = self.max_block_image.get_rect()
		self.max_block_image_rect.centerx = self.screen_rect.centerx
		self.max_block_image_rect.top = 35

	def show_score(self):
		''' draw score information on the screen'''
		# self.screen.blit(self.score_image, self.score_image_rect)
		self.screen.blit(self.block_image, self.block_image_rect)
		self.screen.blit(self.max_block_image, self.max_block_image_rect)
		self.screen.blit(self.score_image, self.score_image_rect)
		self.screen.blit(self.high_score_image, self.high_score_image_rect)
		self.sc_blocks.draw(self.screen)