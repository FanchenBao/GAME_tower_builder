# GAME_tower_builder
Developed with pygame

_Major project inspired by Chapter 12 of "Python Crash Course" and a phone game I enjoyed a lot in the pre-smart phone days._

* __tower_builder.py__ is the driver file.
* Player moves can only use spacebar to drop a block as it moves left and right on the top. Player should aim to perfectly land a new block on the original block. There is no end to the game. Try to build the tower as high as possible.
* Player can press ‘Q’ to quit the game any time during the game.
* Default state is one block going from left to right at the top, waiting for player to press spacebar and drop it.
* If it hits the left or right edge, or if it fails to land properly on the existing tower, the block disappears and player has one fewer block to play with.
* Imperfect landing causes the tower to shift left and right. The amount of shift is determined by how many pixels combined are the imperfect landing on the left and right side. The combined left and right pixels, along with the coordinate of the bottom block, determines the shifting range. Apparently, the more imperfect the landing, the larger the shift and the more difficult the game.
* Perfect landing can reduce shifting range, thus aiming for perfect landing could potentially make the game easier, though making a perfect landing is not that easy.
* The game allows error margin when considering for perfect landing. i.e. if the landing block’s edge is within the error margin misaligned with the block beneath it, it is still considered a perfect landing.
* There are required upper and lower limit of number of blocks allowed for display on the screen. If the current number of blocks in the tower exceeds the upper limit, the entire tower would appear to drop down to create more room in the air for further building.
* Scoring system (two records are kept, one for the actual high score, the other highest number of blocks built):
  * Perfect landing: +1000 pts
  * Good landing: +500 pts
  * Fair landing: +5 pts
  * Building of each block: +500 pts
* Major game stats scale up, including speed of drop, shifting, and scoring system, once game levels up. By default, every 10 blocks built equals one level up.
