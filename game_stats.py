class GameStats():
	'''track game statistics for alien invasion'''
	def __init__(self, ai_settings, filename_block, filename_score):
		self.ai_settings = ai_settings
		self.game_active = False		
		self.reset_stats()
		self.read_max_block(filename_block)
		self.read_high_score(filename_score)


	def reset_stats(self):
		'''initialize statistics that can change during game'''
		# record game score and block number
		self.score = 0
		self.number_block = 0
		self.falls_left = self.ai_settings.max_falls_allowed
		# level up every certain number of blocks built (see settings), level info not shown to player
		self.level = 1
		
		# stats related to blocks shifting side to side
		# list of shifts from all blocks
		self.each_shift = []
		# store the left and right edge of shift
		self.left_edge = 0
		self.right_edge = 0

		# record the number of landing that is perfect
		self.number_perfect = 0

	def read_max_block(self, filename_block):
		'''import all time high score'''
		with open(filename_block) as file_object:
			content = file_object.read()
		self.max_block = int(content)

	def read_high_score(self, filename_score):
		'''import all time high score'''
		with open(filename_score) as file_object:
			content = file_object.read()
		self.high_score = int(content)