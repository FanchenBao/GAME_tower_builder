import sys
import pygame
from block import Block
# from bullet import Bullet
# from rock import Rock
# from reward_stats import RewardStats
# from reward import Reward
# from missile import Missile
# from shield import Shield
# from time import clock
# from random import sample

def update_block(new_blocks, built_blocks, screen, ai_settings):
	''' update block behavior'''
	for block in new_blocks.copy():
		# check block edges before it is released
		check_block_edge(block, ai_settings)
		# update block position
		block.update()
		# the following only happens when block is dropping
		if block.drop:
			if block.index == 1:
				# first block has different condition compared to the others
				check_first_block(block, new_blocks, built_blocks, screen, ai_settings)
			else:
				check_other_block(block, new_blocks, built_blocks, screen, ai_settings)
			

def check_first_block(block, new_blocks, built_blocks, screen, ai_settings):
	''' examine conditions of first block hitting the ground'''
	if block.rect.bottom > block.screen_rect.bottom:
		# if first block hit the ground and part of it is outside the screen, remove the block
		if (block.rect.left < block.screen_rect.left or 
			block.rect.right > block.screen_rect.right):
			new_blocks.remove(block)
			# create a new FIRST block
			create_block(new_blocks, screen, ai_settings, 1)
		else:
			# if first block lands within the screen (the rect_correction for first block is only 5 pixels)
			block.rect.bottom = block.screen_rect.bottom + ai_settings.first_block_rect_correction
			# remove it from the new blocks and add to built block
			new_blocks.remove(block)
			built_blocks.add(block)
			# create the first non-FIRST block
			create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))

def check_other_block(block_top, new_blocks, built_blocks, screen, ai_settings):
	''' examine conditions of non-first block dropping'''
	# check for collision of the newly dropped block and the built blocks
	block_bottom = pygame.sprite.spritecollideany(block_top, built_blocks)
	if block_bottom:
		# collision happens
		if (block_top.rect.left < block_top.screen_rect.left or 
			block_top.rect.right > block_top.screen_rect.right):
			# top block doesn't land within the screen, then remove it
			new_blocks.remove(block_top)
			create_block(new_blocks, screen, ai_settings, block.index)
		else:
			# block_top lands within the screen
			for block in built_blocks.sprites():
				# to elimiate the situation where top block hit the side of the bottom block and still be considered a good hit
				# 15 here is the error tolerance. If top block hit the side of botoom block within 10 pixels away from bottom block's top edge
				# it will still counts as a hit
				if block_top.rect.bottom > block.rect.top + 15:
					new_blocks.remove(block_top)
					create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))
					return
			# position block_top on top of block_bottom with rect correction
			block_top.rect.bottom = block_bottom.rect.top + ai_settings.rect_correction
			
			# find the fulcrum of block_top
			find_fulcrum(block_top, block_bottom)
			# check stability of block_top
			check_falling_block_top(block_top, new_blocks, built_blocks, screen, ai_settings)		

			if not block_top.fall:
				# the remaining procedures only make sense when block_top stands
				
				# calculate leverage of each built block underneath
				find_leverage(block_top, built_blocks)

				# remove block_top from new_blocks and put it into built_block
				new_blocks.remove(block_top)
				built_blocks.add(block_top)
				
				# check each built block's leverage to find any that has tipped
				check_falling_block(built_blocks)

				# remove the built blocks that are falling
				remove_falling_block(built_blocks)

				# create new block
				create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))
			
	
	elif block_top.rect.top >= block_top.screen_rect.bottom:
		# collision doesn't happen. Remove the dropping block and create a new one
		new_blocks.remove(block_top)
		create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))

def check_falling_block_top(block_top, new_blocks, built_blocks, screen, ai_settings):
	''' check whether block top can stand. If it cannot, no need to update leverage of the built blocks
	and a new block will be generated'''
	
	# calculate block top leverage
	block_top.leverage += block_top.fulcrum_x - block_top.rect.centerx
	# determine its fate
	if block_top.fulcrum_position == "left" or block_top.fulcrum_position == "none":
		if block_top.leverage >= 0:
			block_top.fall = True
			new_blocks.remove(block_top)
			create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))
	if block_top.fulcrum_position == "right":
		if block_top.leverage <= 0:
			block_top.fall = True
			new_blocks.remove(block_top)
			create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))

def remove_falling_block(built_blocks):
	''' remove the built block that has the fall flag as True.'''
	for block in built_blocks.copy():
		if block.fall:
			built_blocks.remove(block)

def check_falling_block(built_blocks):
	''' check each block in built_blocks for its leverage and determine whether it is falling'''
	# a list to record all the falling blocks
	list_of_falls = []
	for block in built_blocks.sprites():
		print(block.index, block.leverage)
		if block.index != 1:
			if block.fulcrum_position == "left" or block.fulcrum_position == "none":
				if block.leverage >= 0:
					block.fall = True
					list_of_falls.append(block.index)
			if block.fulcrum_position == "right":
				if block.leverage <= 0:
					block.fall = True
					list_of_falls.append(block.index)
	# find the most bottom block that is going to fall
	if list_of_falls:
		lowest_falling_index = min(list_of_falls)
		# record the centerx value of each fallen block
		fallen_block_center = 0
		# record the number of blocks fallen
		number_of_fallen = 0
		
		# all blocks above the lowest falling block shall also fall
		for block in built_blocks.sprites():
			if block.index != 1:
				if block.index >= lowest_falling_index:
					block.fall = True
					fallen_block_center += block.rect.centerx
					number_of_fallen += 1
		
		# calculate lost leverage for each non-fallen block and update new leverage
		for block in built_blocks.sprites():
			if block.index != 1 and block.fall == False:
				block.leverage -= block.fulcrum_x * number_of_fallen - fallen_block_center

def find_leverage(block_top, built_blocks):
	''' Update the leverage of each built block by subtracting the center of block_top from its fulcrum.'''
	for block in built_blocks.sprites():
		if block.index != 1:
			block.leverage += (block.fulcrum_x - block_top.rect.centerx)


def find_fulcrum(block_top, block_bottom):
	''' determine the fulcrum position and x coordinate on which block_top is balanced on block_bottom'''
	if (block_bottom.rect.left > block_top.rect.left and 
		block_bottom.rect.left < block_top.rect.right):
		block_top.fulcrum_position = "left"
		block_top.fulcrum_x = block_bottom.rect.left
	elif block_bottom.rect.left == block_top.rect.left:
		block_top.fulcrum_position = "none"
		block_top.fulcrum_x = block_bottom.rect.left
	elif block_bottom.rect.left < block_top.rect.left:
		block_top.fulcrum_position = "right"
		block_top.fulcrum_x = block_bottom.rect.right	

def check_block_edge(block, ai_settings):
	if not block.drop:
		if block.check_edges():
			ai_settings.block_direction *= -1

def create_block(blocks, screen, ai_settings, index):
	block = Block(screen, ai_settings, index)
	blocks.add(block)

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

def check_key_down_event(event, new_blocks):
	# determine action when key is pushed down

	if event.key == pygame.K_SPACE:
		# drop a block
		for block in new_blocks.sprites():
			block.drop = True
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


def check_events(new_blocks):
	# an event loop to monitor user's input (press key or move mouse)
	# The one below checks whether user clicks to close the program.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# save high score and then quit
			# record_high_score(stats.high_score, filename)
			sys.exit()
		# check whether the event is a key press
		elif event.type == pygame.KEYDOWN:
			check_key_down_event(event, new_blocks)

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
	
def update_screen(ai_settings, screen, new_blocks, built_blocks):
	# redraw the scren during each pass of the loop
	screen.fill(ai_settings.background_color)

	new_blocks.draw(screen)
	built_blocks.draw(screen)

	
	
	# draw the play button only when game is inactive
	# if not stats.game_active:
	# 	play_button.draw_button()

	# score_board.show_score()

	# display the most recently drawn screen.
	pygame.display.flip()

