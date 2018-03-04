import pygame
from pygame.sprite import Group
# from settings import Settings
# from piggy import Piggy
# from button import Button
# from rock_stats import RockStats
# from score_board import ScoreBoard
import game_functions as gf
# from game_stats import GameStats
# from time import clock

def run_game():
	# initialize game and create a screen object.
	
	# initialize game
	pygame.init()

	# create game display
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Tower Builder")

	# # create an instance to store game stats
	# filename = 'high_round.txt'

	# stats = GameStats(ai_settings, filename)

	# piggy = Piggy(screen, ai_settings)
	# bullets = Group()
	
	# rocks = Group()
	# rock_stats = RockStats()
	
	# rewards = Group()
	# shields = Group()

	

	# score_board = ScoreBoard(screen, ai_settings, stats)
	
	# gf.create_initial_rocks(screen, ai_settings, rock_stats, rocks)
	
	# The main loop of the game
	while True:
		gf.check_events()
		# if stats.game_active:
		# 	piggy.update()
		# 	gf.fire_bullet(ai_settings, screen, piggy, bullets)
		# 	gf.update_bullets(screen, ai_settings, rocks, bullets, rewards, stats, score_board)
		# 	gf.update_rocks(screen, ai_settings, rock_stats, rocks, piggy, stats, score_board)
		# 	gf.update_rewards(shields, screen, ai_settings, piggy, rewards, score_board)
		# 	gf.update_shields(shields, ai_settings, rocks)
		# 	gf.check_round(stats, score_board, ai_settings)
		
		# # # create a play button
		# # if stats.piggy_hit:
		# # 	msg1 = "Game Over"
		# # else:
		# # 	msg1 = 'Round ' + str(stats.round)
		# # msg2 = 'Press "P" to Play'
		# # play_button = Button(screen, ai_settings, msg1, msg2)

		# gf.update_screen(ai_settings, screen, piggy, bullets, stats, play_button, rocks, rewards, shields, score_board)
		
run_game()
