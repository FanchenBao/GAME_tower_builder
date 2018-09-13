'''
Author: Fanche Bao
Date: 03/10/2018

Description:
Settings class. Default settings.
'''

class Settings():
	''' to store all settings for the game'''
	def __init__(self):
		''' the static settings'''
		self.screen_height = 750
		self.screen_width = 700
		# background needs to be light sky blue at the beginning
		self.background_color = (135, 206, 250)

		# gravity (not scaling up because a small gravity makes game harder)
		self.g = 0.3

		# the rect for block has an edge of a few pixels. this is to remove such edge
		# for all the other blocks, such edge is set at 8 pixels. But the first block 
		# only need to remove 5 pixels.
		self.rect_correction = 8
		self.first_block_rect_correction = 5

		# max and min number of blocks visible on screen
		self.max_blocks_on_screen = 4
		self.min_blocks_on_screen = 3

		# each player is allowed any type of block fall for maximum 3 times
		self.max_falls_allowed = 3

		# speed in which built blocks move down to exit screen
		self.block_adjust_speed = 1
		# the amount of time taken for one shift from left to right
		self.shift_duration = 50
		# record the initial center position of the first block, for side to side shift purpose
		self.initial_center = 0
		# flag to indicate whether the blocks are moving down or up (to prevent horizontal shift and vertical motion happen at the same time)
		self.blocks_vertical_motion = False

		# the amount of shift reduction if a landing is deemed perfect
		self.shift_reward = 5
		# when a block lands within the error margin for a perfect landing, it will be considered perfect landing
		self.perfect_margin = 3


		# once level up, certain game parameters scale up, make game harder
		self.scale_factor = 1.2
		# every 10 blocks built, level up
		self.level_up_requirement = 10
		
		self.initialize_dynamic_settings()
		

	def initialize_dynamic_settings(self):
		''' the following settings change throughout the game'''
		# block's horizontal speed
		self.horizontal_speed = 3
		# before release, if block hit the left-right edge, change its direction
		self.block_direction = 1
		# change direction specifically for built block shifting
		self.block_shift_direction = 1
		
		# the scaling factor of left or right shift
		self.shift_coefficient = 1

		# the scoring system. Score refers to each successful building attempt
		self.perfect_score = 1000
		self.good_score = 100
		self.fair_score = 5
		# points refer to the value of each block
		self.block_points = 500
	
		