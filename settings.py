class Settings():
	''' to store all settings for alien_invasion'''
	def __init__(self):
		''' the static settings'''
		self.screen_height = 750
		self.screen_width = 600
		# background needs to be light sky blue at the beginning
		self.background_color = (135, 206, 250)

		

		self.initialize_dynamic_settings()
		

	def initialize_dynamic_settings(self):
		''' the following settings change throughout the game'''
		# block's horizontal speed
		self.horizontal_speed = 3
		# before release, if block hit the left-right edge, change its direction
		self.block_direction = 1
		# gravity
		self.g = 0.2
		