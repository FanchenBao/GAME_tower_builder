class GameStats():
	'''track game statistics for alien invasion'''
	def __init__(self, ai_settings, filename):
		self.ai_settings = ai_settings
		self.game_active = False
		self.reset_stats()
		self.read_high_level(filename)


	def reset_stats(self):
		'''initialize statistics that can change during game'''
		# record game score
		self.score = 0
		self.level = 0

	def read_high_level(self, filename):
		'''import all time high score'''
		with open(filename) as file_object:
			content = file_object.read()
		self.high_level = int(content)