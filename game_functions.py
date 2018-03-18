import sys
import pygame
from pygame.time import get_ticks
from block import Block
from message import Message

def update_block(new_blocks, built_blocks, screen, ai_settings, stats, score_board, messages):
	''' update block behavior'''
	for block in new_blocks.copy():
		# check block edges before it is released
		if not block.drop:
			check_block_edge(block, ai_settings, block.screen_rect.left, block.screen_rect.right)
		# update block position
		block.update()
		# the following only happens when block is dropping
		if block.drop:
			if block.index == 1:
				# first block has different condition compared to the others
				check_first_block(block, new_blocks, built_blocks, screen, ai_settings, stats, score_board, messages)
			else:
				check_other_block(block, new_blocks, built_blocks, screen, ai_settings, stats, score_board, messages)
	
	# move blocks up and down or shift left and right, when conditions satisfy
	adjust_block_position(ai_settings, built_blocks, stats)
			
def shift_block(ai_settings, built_blocks, stats):
	''' shift the build blocks side to side to increase difficulty.
	the extent of shifting determined by the total left and right shifts of each block'''

	for block in built_blocks.sprites():
		# checking the edge of the first block ONLY
		if block.index == 1:
			# if only one block is built, keep it stationary
			if len(built_blocks) <= ai_settings.min_blocks_on_screen:
				return
			# when blocks are shifting, the edge check is DIFFERENT from regular method
			# because the edges here are dynamic, and falling of blocks can cause the edge to shrink while the blocks are still outside the block.
			# when this happens, block direction must not change until blocks to return within the shrunken edges 
			# e.g. if blocks are moving right when edge shrink happens, block must continue moving right until it's within the new edges (even if its current left is more left to the edge, which should cause a change of direction)
			else:
				if block.rect.left <= stats.left_edge:
					if ai_settings.block_shift_direction == -1:
						ai_settings.block_shift_direction = 1
				if block.rect.right >= stats.right_edge:
					if ai_settings.block_shift_direction == 1:
						ai_settings.block_shift_direction = -1
			break
	# shift the blocks	
	shift_range = stats.right_edge - stats.left_edge
	for block in built_blocks.sprites():
		block.lateral_shift(shift_range)	

def update_falls_left(stats, score_board):
	''' update how many falls left player can afford. If no more fall allowed, set the game to inactive'''
	stats.falls_left -= 1
	score_board.prep_falls_left()
	if stats.falls_left == 0:
		# update high score
		if stats.score > stats.high_score:
			stats.high_score = stats.score
			score_board.prep_high_score()
		# update max block
		if stats.number_block > stats.max_block:
			stats.max_block = stats.number_block
			score_board.prep_max_block()
		stats.game_active = False

def check_first_block(block, new_blocks, built_blocks, screen, ai_settings, stats, score_board, messages):
	''' examine conditions of first block hitting the ground'''
	if block.rect.bottom > block.screen_rect.bottom:
		# if first block hit the ground and part of it is outside the screen, remove the block
		if (block.rect.left < block.screen_rect.left or 
			block.rect.right > block.screen_rect.right):
			new_blocks.remove(block)
			# notify player it's a bad landing
			create_message(messages, screen, ai_settings, 'oops')
			# check how many falls left for player
			update_falls_left(stats, score_board)
			# create a new FIRST block
			create_block(new_blocks, screen, ai_settings, 1)
		else:
			# if first block lands within the screen (the rect_correction for first block is only 5 pixels)
			block.rect.bottom = block.screen_rect.bottom + ai_settings.first_block_rect_correction
			# record the initial center position, for side to side shift purpose
			ai_settings.initial_center = block.rect.centerx
			# first block has 0 degree of shifting
			stats.each_shift.append(0)
			# remove it from the new blocks and add to built block
			new_blocks.remove(block)
			built_blocks.add(block)
			
			show_current_block_number(stats, built_blocks, score_board, ai_settings)

			# calculate score
			calculate_first_block_score(block, ai_settings, stats, score_board, messages, screen)

			# create the first non-FIRST block
			create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))

def create_message(messages, screen, ai_settings, flag):
	'''create a message describing how well the building is'''
	message = Message(screen, ai_settings, flag)
	messages.add(message)
	# record when the message was created
	message.time = get_ticks()

def calculate_first_block_score(block, ai_settings, stats, score_board, messages, screen):
	''' calculate score for first block under different conditions.
	 also create a consummerate message'''
	if block.rect.centerx == block.screen_rect.centerx:
		stats.score += int(ai_settings.perfect_score)
		create_message(messages, screen, ai_settings, 'perfect')

	elif block.rect.centerx > block.screen_rect.width / 4 and block.rect.centerx < block.screen_rect.width / 2:
		stats.score += int(ai_settings.good_score)
		create_message(messages, screen, ai_settings, 'good')

	elif block.rect.centerx > block.screen_rect.width / 2 and block.rect.centerx < block.screen_rect.width * (3/4):
		stats.score += int(ai_settings.good_score)
		create_message(messages, screen, ai_settings, 'good')

	elif block.rect.centerx <= block.screen_rect.width / 4:
		stats.score += int(ai_settings.fair_score)
	elif block.rect.centerx >= block.screen_rect.width * (3/4):
		stats.score += int(ai_settings.fair_score)
	
	score_board.prep_score()


def check_other_block(block_top, new_blocks, built_blocks, screen, ai_settings, stats, score_board, messages):
	''' examine conditions of non-first block dropping'''
	# check for collision of the newly dropped block and the built blocks
	block_bottom = pygame.sprite.spritecollideany(block_top, built_blocks)
	if block_bottom:
		# collision happens
		if (block_top.rect.left < block_top.screen_rect.left or 
			block_top.rect.right > block_top.screen_rect.right):
			# top block doesn't land within the screen, then remove it
			new_blocks.remove(block_top)
			# notify player it's a bad landing
			create_message(messages, screen, ai_settings, 'oops')
			# check how many falls left for player
			update_falls_left(stats, score_board)
			create_block(new_blocks, screen, ai_settings, block_top.index)
		else:
			# block_top lands within the screen
			for block in built_blocks.sprites():
				# to elimiate the situation where top block hit the side of the bottom block and still be considered a good hit
				# 15 here is the error tolerance. If top block hit the side of botoom block within 15 pixels away from bottom block's top edge
				# it will still counts as a hit
				if block_top.rect.bottom > block.rect.top + 15:
					new_blocks.remove(block_top)
					# notify player it's a bad landing
					create_message(messages, screen, ai_settings, 'oops')
					# check how many falls left for player
					update_falls_left(stats, score_board)
					create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))
					return
			
			# position block_top on top of block_bottom with rect correction
			block_top.rect.bottom = block_bottom.rect.top + ai_settings.rect_correction
			
			# find the fulcrum of block_top
			find_fulcrum(block_top, block_bottom, ai_settings, stats)
			# check stability of block_top
			check_falling_block_top(block_top, new_blocks, built_blocks, screen, ai_settings, messages, stats, score_board)		

			if not block_top.fall:
				# the remaining procedures only make sense when block_top stands
				
				# block top not falling, so calculate its score
				calculate_block_top_score(block_top, ai_settings, stats, score_board, screen, messages)

				# find block_top and all built blocks' shift
				find_shift(block_top, built_blocks, stats, ai_settings)

				# remove block_top from new_blocks and put it into built_block
				new_blocks.remove(block_top)
				built_blocks.add(block_top)
				
				# Update each block's leverage, check each built block's leverage to find any that has tipped, and remove it
				# Also update the total left and right shifts, as well as edges.
				check_falling_block(block_top, built_blocks, messages, screen, ai_settings, stats, score_board)

				show_current_block_number(stats, built_blocks, score_board, ai_settings)

				# update shifting edges
				find_shifting_edge(stats, ai_settings, block_top)
				
				# create new block
				create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))
			
	
	elif block_top.rect.top >= block_top.screen_rect.bottom:
		# collision doesn't happen. Remove the dropping block and create a new one
		new_blocks.remove(block_top)
		# notify player it's a bad landing
		create_message(messages, screen, ai_settings, 'oops')
		# check how many falls left for player
		update_falls_left(stats, score_board)
		create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))

def find_shifting_edge(stats, ai_settings, block_top):
	''' calculate the left and right edge of shifting'''
	# total reward from perfect landing
	total_reward = ai_settings.shift_reward * stats.number_perfect
	
	# get left shift (negative value). If there is no left shift, set the value to 0
	left_shift = min(stats.each_shift) + total_reward
	if left_shift > 0:
		left_shift = 0

	# get right shift. Same rule as left shift
	right_shift = max(stats.each_shift) - total_reward
	if right_shift < 0:
		right_shift = 0

	# calculate left and right edge
	stats.left_edge = ai_settings.initial_center + left_shift - block_top.rect.width / 2
	stats.right_edge = ai_settings.initial_center + right_shift + block_top.rect.width / 2

def find_shift(block_top, built_blocks, stats, ai_settings):
	''' calculate the shift of each block_top, and update total shift of built blocks and left right edges'''
	for block in built_blocks.sprites():
		if block.index == 1:
			if block_top.fulcrum_position == 'left':
				# left shift (negative value) equals the left side of block outside the left side of first block
				block_top.shift = (block_top.rect.left - block.rect.left) * ai_settings.shift_coefficient
				stats.each_shift.append(block_top.shift)
			if block_top.fulcrum_position == 'right':
				# right shift (positive value) equals the right side of block outside the right side of first block
				block_top.shift = (block_top.rect.right - block.rect.right) * ai_settings.shift_coefficient
				stats.each_shift.append(block_top.shift)
			if block_top.fulcrum_position == 'none':
				stats.each_shift.append(0)
			return

def calculate_block_top_score(block_top, ai_settings, stats, score_board, screen, messages):
	''' calculate the score of block top'''
	# perfect landing
	if block_top.perfect:
		stats.score += abs(block_top.leverage) * int(ai_settings.perfect_score)
		create_message(messages, screen, ai_settings, 'perfect')
	# all other landing
	else:
		stats.score += abs(block_top.leverage) * int(ai_settings.good_score)
		create_message(messages, screen, ai_settings, 'good')

	score_board.prep_score()

def show_current_block_number(stats, built_blocks, score_board, ai_settings):
	''' update block number and check for leveling up'''
	# record current number of built blocks
	stats.number_block = len(built_blocks)

	if stats.number_block > stats.level * ai_settings.level_up_requirement:
		stats.level += 1
		level_up(ai_settings)

	score_board.prep_block()

def level_up(ai_settings):
	''' update parameters in settings after level up'''
	# game mechanics change, make game more difficult
	ai_settings.horizontal_speed *= ai_settings.scale_factor
	ai_settings.shift_coefficient *= ai_settings.scale_factor
	# scoring system update
	ai_settings.perfect_score *= ai_settings.scale_factor
	ai_settings.good_score *= ai_settings.scale_factor
	ai_settings.fair_score *= ai_settings.scale_factor
	ai_settings.block_points *= ai_settings.scale_factor

def adjust_block_position(ai_settings, built_blocks, stats):
	''' move built blocks down ONE block when there are more than 5 blocks on screen
	also move built blocks up when no block is visible on the screen due to falling'''
	for block in built_blocks.sprites():
		if block.index == len(built_blocks):
			move_block_down(block, built_blocks, ai_settings)
			break
	
	# block shift stops when blocks are moving down or up, then resume after vertical motion ends
	if not ai_settings.blocks_vertical_motion:
		shift_block(ai_settings, built_blocks, stats)

def move_block_down(block_top, built_blocks, ai_settings):
	# move blocks down if there are more than max blocks on screen
	if ((block_top.screen_rect.bottom - block_top.rect.top) > 
		ai_settings.max_blocks_on_screen * block_top.rect.height):
		ai_settings.blocks_vertical_motion = True
		for block in built_blocks.sprites():
			block.rect.bottom += ai_settings.block_adjust_speed
	else:
		move_block_up(block_top, built_blocks, ai_settings)

def move_block_up(block_top, built_blocks, ai_settings):
	# move blocks up if there are less than minimum blocks on screen
	# when there are more than min blocks required on screen, show only the min number of blocks
	if len(built_blocks) >= ai_settings.min_blocks_on_screen:
		if ((block_top.screen_rect.bottom - block_top.rect.top) < 
			ai_settings.min_blocks_on_screen * (block_top.rect.height - ai_settings.rect_correction)):
			ai_settings.blocks_vertical_motion = True
			for block in built_blocks.sprites():
				block.rect.bottom -= ai_settings.block_adjust_speed * 3
		else:
			ai_settings.blocks_vertical_motion = False
	# when there are fewer than min blocks requried on screen, show all blocks
	else:
		if ((block_top.screen_rect.bottom - block_top.rect.top) < 
			len(built_blocks) * (block_top.rect.height - ai_settings.rect_correction)):
			ai_settings.blocks_vertical_motion = True
			for block in built_blocks.sprites():
				block.rect.bottom -= ai_settings.block_adjust_speed * 3
		else:
			ai_settings.blocks_vertical_motion = False


def check_falling_block_top(block_top, new_blocks, built_blocks, screen, ai_settings, messages, stats, score_board):
	''' check whether block top can stand. If it cannot, no need to update leverage of the built blocks
	and a new block will be generated'''
	
	# calculate block top leverage
	block_top.leverage += block_top.fulcrum_x - block_top.rect.centerx
	# determine its fate
	if block_top.fulcrum_position == "left" or block_top.fulcrum_position == "none":
		if block_top.leverage >= 0:
			block_top.fall = True
			new_blocks.remove(block_top)
			# notify player it's a bad landing
			create_message(messages, screen, ai_settings, 'oops')
			# check how many falls left for player
			update_falls_left(stats, score_board)
			create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))
	if block_top.fulcrum_position == "right":
		if block_top.leverage <= 0:
			block_top.fall = True
			new_blocks.remove(block_top)
			# notify player it's a bad landing
			create_message(messages, screen, ai_settings, 'oops')
			# check how many falls left for player
			update_falls_left(stats, score_board)
			create_block(new_blocks, screen, ai_settings, (len(built_blocks) + 1))

def update_added_leverage(block, block_top):
	''' update a block's leverage once a new block lands successfully'''
	new_lev = block.fulcrum_x - block_top.rect.centerx
	# sum of all added leverage
	block.leverage += new_lev
	# record each newly added leverage
	block.each_leverage.append(new_lev)

def update_lost_leverage(built_blocks, lowest_falling_index):
	''' update the leverage of each block after the blocks above them fall'''
	for block in built_blocks.sprites():
		if block.index != 1 and block.fall == False:
			# record the position of the lowest falling block in each_leverage list
			pos = lowest_falling_index - block.index - 1
			# remove all these leverages from the total leverage
			block.leverage -= sum(block.each_leverage[pos:])
			# also remove them individually from the list
			del block.each_leverage[pos:]

def remove_blocks(built_blocks, lowest_falling_index, stats, ai_settings):
	''' remove blocks, starting from the lowest falling block and above. 
	Also update stats on perfect landing, lateral shifts, and scores '''
	for block in built_blocks.copy():
		if block.index != 1:
			if block.index >= lowest_falling_index:
				block.fall = True
				
				# if a fallen block is a perfect land, reduce perfect count
				if block.perfect:
					stats.number_perfect -= 1

				# remove its shift value from the each_shift list
				stats.each_shift.remove(block.shift)
				
				# remove falling blocks
				built_blocks.remove(block)
				
				# update score, decrease the block points for each removed block
				stats.score -= int(ai_settings.block_points)

def check_falling_block(block_top, built_blocks, messages, screen, ai_settings, stats, score_board):
	''' check each block in built_blocks for its leverage and determine whether it is falling
	also update the leverage and left-right shift of remaining blocks'''
	# a list to record all the falling blocks
	list_of_falls = []
	for block in built_blocks.sprites():
		if block.index != 1 and block.index != len(built_blocks):
			# update all blocks' leverages (except first block and block_top)
			update_added_leverage(block, block_top)

			# only allow the blocks visible on screen to fall (make game easier)
			if len(built_blocks) > ai_settings.max_blocks_on_screen:
				# check for block falling on the top 5 blocks
				if block.index >= (len(built_blocks) - ai_settings.max_blocks_on_screen):
					assign_fall(block, list_of_falls)
			else:
				assign_fall(block, list_of_falls)

	# find the lowest block that is going to fall
	if list_of_falls:
		lowest_falling_index = min(list_of_falls)
		
		# all blocks above the lowest falling block shall also fall
		remove_blocks(built_blocks, lowest_falling_index, stats, ai_settings)
		
		score_board.prep_score()
		
		# calculate lost leverage for each non-fallen block and update new leverage
		update_lost_leverage(built_blocks, lowest_falling_index)

		# empty the messages, to prevent double-showing the message: block_top is a good
		# (with message saying 'good'), but blocks beneath fall (with message saying 'oops')
		messages.empty()
		# notify player it's a bad landing
		create_message(messages, screen, ai_settings, 'oops')
		# check how many falls left for player
		update_falls_left(stats, score_board)

def assign_fall(block, list_of_falls):
	if block.fulcrum_position == "left" or block.fulcrum_position == "none":
		if block.leverage >= 0:
			block.fall = True
			list_of_falls.append(block.index)
	if block.fulcrum_position == "right":
		if block.leverage <= 0:
			block.fall = True
			list_of_falls.append(block.index)

def find_fulcrum(block_top, block_bottom, ai_settings, stats):
	''' determine the fulcrum position and x coordinate on which block_top is balanced on block_bottom'''
	if (block_bottom.rect.left > block_top.rect.left and 
		block_bottom.rect.left < block_top.rect.right):
		# let a landing be perfect if it's within the error margin
		if (block_bottom.rect.left - block_top.rect.left) <= ai_settings.perfect_margin:
			block_top.rect.left = block_bottom.rect.left
			block_top.fulcrum_position = 'none'
			block_top.perfect = True
			# update number of perfect landing
			stats.number_perfect += 1
		else:
			block_top.fulcrum_position = "left"
		block_top.fulcrum_x = block_bottom.rect.left
	elif block_bottom.rect.left == block_top.rect.left:
		block_top.fulcrum_position = "none"
		block_top.perfect = True
		# update number of perfect landing
		stats.number_perfect += 1
		block_top.fulcrum_x = block_bottom.rect.left
	elif block_bottom.rect.left < block_top.rect.left:
		# let a landing be perfect if it's within the error margin
		if (block_top.rect.left - block_bottom.rect.left) <= ai_settings.perfect_margin:
			block_top.rect.left = block_bottom.rect.left
			block_top.fulcrum_position = 'none'
			block_top.perfect = True
			# update number of perfect landing
			stats.number_perfect += 1
			block_top.fulcrum_x = block_bottom.rect.left
		else:
			block_top.fulcrum_position = "right"
			block_top.fulcrum_x = block_bottom.rect.right	

def check_block_edge(block, ai_settings, left_edge, right_edge):
	if block.check_edges(left_edge, right_edge):
		ai_settings.block_direction *= -1

def create_block(blocks, screen, ai_settings, index):
	block = Block(screen, ai_settings, index)
	blocks.add(block)

def check_key_down_event(event, stats, ai_settings, new_blocks, built_blocks, screen, filename_block, filename_score, score_board):
	# determine action when key is pushed down

	if event.key == pygame.K_SPACE:
		# drop a block
		for block in new_blocks.sprites():
			block.drop = True
	elif event.key == pygame.K_q:
		# save high score and max block and then quit
		record_achievement(stats.max_block, filename_block)
		record_achievement(stats.high_score, filename_score)
		sys.exit()

	# press "P" to play the game	
	elif event.key == pygame.K_p:
		if not stats.game_active:
		 	# restart or start a new game
			game_restart(stats, ai_settings, new_blocks, built_blocks, screen, score_board)
			# hide the mouse cursor
			pygame.mouse.set_visible(False)


def check_events(stats, ai_settings, new_blocks, built_blocks, screen, filename_block, filename_score, score_board):
	# an event loop to monitor user's input (press key or move mouse)
	# The one below checks whether user clicks to close the program.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# save high score and then quit
			record_achievement(stats.max_block, filename_block)
			record_achievement(stats.high_score, filename_score)
			sys.exit()
		# check whether the event is a key press
		elif event.type == pygame.KEYDOWN:
			check_key_down_event(event, stats, ai_settings, new_blocks, built_blocks, screen, filename_block, filename_score, score_board)

		# check for mouseclick on play button
		# elif event.type == pygame.MOUSEBUTTONDOWN:
		# 	mouse_x, mouse_y = pygame.mouse.get_pos()
		# 	check_play_button(play_button, stats, mouse_x, mouse_y, aliens, bullets, screen, ai_settings, ship)

def record_achievement(achievement, filename):
	'''record high level in a separate file so that each new game starts with a previous high level'''
	str_achievement = str(achievement)
	with open(filename, 'w') as file_object:
		file_object.write(str_achievement)

def game_restart(stats, ai_settings, new_blocks, built_blocks, screen, score_board):
	# restart the game by resetting stats and clearing out remnants of previous game
	stats.game_active = True

	# reset all the stats
	stats.reset_stats()
	ai_settings.initialize_dynamic_settings()

	# reset all the scoreboard images
	prep_scoreboard_images(score_board)

	# empty out all blocks
	new_blocks.empty()
	built_blocks.empty()

	# create new first block
	create_block(new_blocks, screen, ai_settings, 1)
	
def prep_scoreboard_images(score_board):
	score_board.prep_score()
	score_board.prep_block()
	score_board.prep_falls_left()
	score_board.prep_high_score()
	score_board.prep_max_block()
	
def update_screen(ai_settings, screen, new_blocks, built_blocks, stats, play_button, score_board, messages):
	# redraw the scren during each pass of the loop
	screen.fill(ai_settings.background_color)

	new_blocks.draw(screen)
	built_blocks.draw(screen)

	for message in messages.copy():
		message.blitme()
		# each frame message is blit, get its time
		current_time = get_ticks()
		# when message is displayed for more than 1 second, remove it
		if (current_time - message.time) / 1000 >= 1:
			messages.remove(message)
	
	# draw the play button only when game is inactive
	if not stats.game_active:
		play_button.draw_button()

	score_board.show_score()

	# display the most recently drawn screen.
	pygame.display.flip()

