class Settings():
	''' to store all settings for alien_invasion'''
	def __init__(self):
		''' the static settings'''
		self.screen_height = 1000
		self.screen_width = 500
		# background needs to be light sky blue at the beginning
		self.background_color = (135, 206, 250)

		self.g = 9.8
		

	def initialize_dynamic_settings(self):
		''' the following settings change throughout the game'''
		self.horizontal_speed = 3

		