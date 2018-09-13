'''
Author: Fanche Bao
Date: 03/10/2018

Description:
Driver file
User spacebar to drop the building block. Build as high as possible.
'''

import pygame
from pygame.sprite import Group
from settings import Settings
from button import Button
# from rock_stats import RockStats
from score_board import ScoreBoard
import game_functions as gf
from game_stats import GameStats
# from time import clock

def run_game():
	# initialize game and create a screen object.
	
	# initialize game
	pygame.init()

	# create game display
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Tower Builder")

	# create an instance to store game stats
	filename_block = 'max_block.txt'
	filename_score = 'high_score.txt'
	stats = GameStats(ai_settings, filename_block, filename_score)
	
	# the blocks already built and the newly appeared blocks need two different groups
	built_blocks = Group()
	new_blocks = Group()
	messages = Group()

	# blocks specifically for score_board use
	sc_blocks = Group()
	score_board = ScoreBoard(screen, ai_settings, stats, sc_blocks)
	
	# The main loop of the game
	while True:
		gf.check_events(stats, ai_settings, new_blocks, built_blocks, screen, filename_block, filename_score, score_board)
		if stats.game_active:
			gf.update_block(new_blocks, built_blocks, screen, ai_settings, stats, score_board, messages)
		
		# create a play button
		if stats.falls_left == 0:
			msg1 = "Game Over"
		else:
			msg1 = 'Press "Q" to Quit'
		msg2 = 'Press "P" to Play'
		play_button = Button(screen, ai_settings, msg1, msg2)

		gf.update_screen(ai_settings, screen, new_blocks, built_blocks, stats, play_button, score_board, messages)
		
run_game()
