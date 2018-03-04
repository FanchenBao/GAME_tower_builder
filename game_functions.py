import sys
import pygame
from bullet import Bullet
from rock import Rock
from reward_stats import RewardStats
from reward import Reward
# from missile import Missile
from shield import Shield
# from time import clock
# from random import sample


def check_reward_piggy_collision(shields, screen, ai_settings, piggy, rewards, score_board):
	# check whether a reward has hit the piggy
	# record the reward
	reward = pygame.sprite.spritecollideany(piggy, rewards)
	if reward:
		check_offensive_reward(reward.reward_flag, ai_settings)
		check_defensive_reward(reward.reward_flag, shields, screen, ai_settings, piggy)
		# remove the reward that has hit the ship
		rewards.remove(reward)
	score_board.prep_shield()
	score_board.prep_power_up()

def check_key_down_event(event):
	# determine action when key is pushed down

	if event.key == pygame.K_SPACE:
		# drop a block
		pass
	elif event.key == pygame.K_q:
		# save high round and then quit
		# record_high_round(stats.high_round, filename)
		sys.exit()

	# press "P" to play the game	
	# elif event.key == pygame.K_p:
	# 	if not stats.game_active:
	# 	 	# restart or start a new game
	# 		game_restart(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename)
	# 		# hide the mouse cursor
	# 		pygame.mouse.set_visible(False)


def check_events():
	# an event loop to monitor user's input (press key or move mouse)
	# The one below checks whether user clicks to close the program.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# save high score and then quit
			# record_high_score(stats.high_score, filename)
			sys.exit()
		# check whether the event is a key press
		elif event.type == pygame.KEYDOWN:
			check_key_down_event(event)

		# check for mouseclick on play button
		# elif event.type == pygame.MOUSEBUTTONDOWN:
		# 	mouse_x, mouse_y = pygame.mouse.get_pos()
		# 	check_play_button(play_button, stats, mouse_x, mouse_y, aliens, bullets, screen, ai_settings, ship)

def record_high_round(high_round, filename):
	'''record high round in a separate file so that each new game starts with a previous high score'''
	str_high_round = str(high_round)
	with open(filename, 'w') as file_object:
		file_object.write(str_high_round)

def game_restart(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename):
	# restart the game by resetting stats and clearing out remnants of previous game
	stats.game_active = True
	
	if stats.piggy_hit:
		# reset all the stats
		stats.reset_stats()
		ai_settings.reset_reward_settings()
		ai_settings.initialize_dynamic_settings()

		# reset all the scoreboard images
		prep_scoreboard_images(score_board)

		# empty out any remaining rocks, bullets, shields
		rocks.empty()
		bullets.empty()
		shields.empty()
		rewards.empty()

		# create new rocks
		create_initial_rocks(screen, ai_settings, rock_stats, rocks)
		
		#reposition piggy to right center position
		piggy.center_x = piggy.screen_rect.right - piggy.rect.width / 2
		piggy.center_y = piggy.screen_rect.centery

def prep_scoreboard_images(score_board):
	score_board.prep_score()
	score_board.prep_target_score()
	score_board.prep_round()
	score_board.prep_high_round()
	score_board.prep_power_up()
	score_board.prep_shield()
	
def update_screen(ai_settings, screen, piggy, bullets, stats, play_button, rocks, rewards, shields, score_board):
	# redraw the scren during each pass of the loop
	screen.fill(ai_settings.background_color)
	# draw each bullet BEHIND the ship, so bullet drawn ahead of ship
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	piggy.blitme()
	rocks.draw(screen)
	rewards.draw(screen)
	shields.draw(screen)
	
	# draw the play button only when game is inactive
	if not stats.game_active:
		play_button.draw_button()

	score_board.show_score()

	# display the most recently drawn screen.
	pygame.display.flip()

