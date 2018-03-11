class Settings():
	''' to store all settings for alien_invasion'''
	def __init__(self):
		''' the static settings'''
		self.screen_height = 750
		self.screen_width = 700
		# background needs to be light sky blue at the beginning
		self.background_color = (135, 206, 250)

		# the rect for block has an edge of a few pixels. this is to remove such edge
		# for all the other blocks, such edge is set at 8 pixels. But the first block 
		# only need to remove 5 pixels.
		self.rect_correction = 8
		self.first_block_rect_correction = 5

		# max and min number of blocks visible on screen
		self.max_blocks_on_screen = 5
		self.min_blocks_on_screen = 3

		# speed in which built blocks move down to exit screen
		self.block_adjust_speed = 1
		
		self.initialize_dynamic_settings()
		

	def initialize_dynamic_settings(self):
		''' the following settings change throughout the game'''
		# block's horizontal speed
		self.horizontal_speed = 3
		# before release, if block hit the left-right edge, change its direction
		self.block_direction = 1
		# gravity
		self.g = 0.3

		# the scoring system. Score refers to each successful building attempt
		self.perfect_score = 100
		self.good_score = 10
		self.fair_score = 5
		# points refer to the value of each block
		self.block_points = 500
		