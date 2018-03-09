import pygame.font

class Button():
	def __init__(self, screen, ai_settings, msg1, msg2):
		'''initialize button'''
		self.screen = screen
		self.screen_rect = screen.get_rect()
		# dimension and property of the botton
		self.width = 250
		self.height = 90
		self.button_color = (0, 0, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 38)

		# position the botom to the center screen
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# put message to the botton
		self.prep_msg1(msg1)
		self.prep_msg2(msg2)

	def prep_msg1(self, msg1):
		''' render a msg into an image'''
		self.msg1_image = self.font.render(msg1, True, self.text_color, 
			self.button_color)
		self.msg1_image_rect = self.msg1_image.get_rect()
		self.msg1_image_rect.centerx = self.rect.centerx
		self.msg1_image_rect.top = self.rect.top + 13

	def prep_msg2(self, msg2):
		''' render a msg into an image'''
		self.msg2_image = self.font.render(msg2, True, self.text_color, 
			self.button_color)
		self.msg2_image_rect = self.msg2_image.get_rect()
		self.msg2_image_rect.centerx = self.rect.centerx
		self.msg2_image_rect.bottom = self.rect.bottom - 13

	def draw_button(self):
		''' draw the blank button and then the msg'''
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg1_image, self.msg1_image_rect)
		self.screen.blit(self.msg2_image, self.msg2_image_rect)
