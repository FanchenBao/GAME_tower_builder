class GameStats():
	'''track game statistics for alien invasion'''
	def __init__(self, ai_settings, filename):
		self.ai_settings = ai_settings
		self.game_active = False
		self.reset_stats()
		self.read_max_block(filename)


	def reset_stats(self):
		'''initialize statistics that can change during game'''
		# record game score
		self.score = 0
		self.number_block = 0

	def read_max_block(self, filename):
		'''import all time high score'''
		with open(filename) as file_object:
			content = file_object.read()
		self.max_block = int(content)