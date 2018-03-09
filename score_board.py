import pygame.font
from pygame.sprite import Group

class ScoreBoard():
	''' a class to record and draw scores on the screen'''
	
	def __init__(self, screen, ai_settings, stats):
		''' initialize scoreboard'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.stats = stats

		self.screen_rect = screen.get_rect()

		# setting font for score
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 28)

		# draw score information on the screen
		# self.prep_score()
		self.prep_block()
		self.prep_max_block()

	# def prep_score(self):
	# 	''' convert score information into image'''
	# 	# round the score to the nearest 10 (if the second argument is 1, that means to ronud to nearest 0.1)
	# 	rounded_score = round(self.stats.score, -1)
	# 	# syntax to insert comma to long number
	# 	score_str = "Score: " + "{:,}".format(rounded_score)
	# 	self.score_image = self.font.render(score_str, True, self.text_color, 
	# 		self.ai_settings.background_color)
	# 	self.score_image_rect = self.score_image.get_rect()
	# 	self.score_image_rect.centerx = self.screen_rect.centerx
	# 	self.score_image_rect.top = 10

	def prep_block(self):
		''' convert maximum blocks achieved into image'''
		block_str = "Blocks: " + str(self.stats.number_block)
		self.block_image = self.font.render(block_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.block_image_rect = self.block_image.get_rect()
		self.block_image_rect.left = 5
		self.block_image_rect.centery = self.screen_rect.centery - 20

	def prep_max_block(self):
		''' convert maximum blocks achieved into image'''
		max_block_str = "Max Blocks: " + str(self.stats.max_block)
		self.max_block_image = self.font.render(max_block_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.max_block_image_rect = self.max_block_image.get_rect()
		self.max_block_image_rect.left = 5
		self.max_block_image_rect.centery = self.screen_rect.centery + 20

	def show_score(self):
		''' draw score information on the screen'''
		# self.screen.blit(self.score_image, self.score_image_rect)
		self.screen.blit(self.block_image, self.block_image_rect)
		self.screen.blit(self.max_block_image, self.max_block_image_rect)