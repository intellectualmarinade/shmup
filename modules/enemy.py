import arcade # Game-making-oriented library for Python.
import math # For various math functions.
import random # For various random number generation.
import os # For getting resource files into the game.
import pyautogui # For getting monitor resolution.
from datetime import datetime, timedelta # For random seed.

# Set up constants
DIFFICULTY = 5
ENEMY_COUNT_INITIAL = DIFFICULTY + 2
ENEMY_SPEED = 2 + (DIFFICULTY/10)
SCALE = 0.25
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
MONITOR_RES_WIDTH, MONITOR_RES_HEIGHT = pyautogui.size()
#   Make sure SCREEN_WIDTH is not bigger than monitor width.
if SCREEN_WIDTH > MONITOR_RES_WIDTH:
    SCREEN_WIDTH = MONITOR_RES_WIDTH
#   Make sure SCREEN_HEIGHT is not bigger than monitor width.
if SCREEN_HEIGHT > MONITOR_RES_HEIGHT:
    SCREEN_HEIGHT = MONITOR_RES_HEIGHT
#   Number of ice blocks based on the screen width.
BLOCKS_NUMBER = int(SCREEN_WIDTH/24)
#   Limit enemies to edges of screen.
SPACE_OFFSCREEN = 1
LIMIT_LEFT = -SPACE_OFFSCREEN
LIMIT_RIGHT = SCREEN_WIDTH + SPACE_OFFSCREEN
LIMIT_BOTTOM = -SPACE_OFFSCREEN
LIMIT_TOP = SCREEN_HEIGHT + SPACE_OFFSCREEN

# MAKE THE ENEMIES
# Create a Python list of strings for storing four image URLs:
image_list = ("./resources/images/walrus-red.png",
                "./resources/images/walrus-blue.png",
                "./resources/images/walrus-purple.png",
                "./resources/images/walrus-green.png")
# Iterate through a number of enemies, in this case,
# we are using the ENEMY_COUNT_INITIAL constant we set
# up above.
for i in range(ENEMY_COUNT_INITIAL):
    # For random colors:
    image_no = random.randint(0,3)
    # For non-random, use "image_no = i" in this spot.
    # The "EnemySprite" call you see below is a class we will
    # create down below.
    enemy_sprite = EnemySprite(image_list[image_no], SCALE)
    # Initialize our "timers", which are more like counters for
    #   making sure the Sprite continues for some time in the
    #   direction/manner we'll determine later.
    enemy_sprite.timer_rand = 0
    enemy_sprite.timer_smart = 0
    # Set random starting positions for each enemy Sprite.
    enemy_sprite.center_y = random.randint(LIMIT_BOTTOM, LIMIT_TOP+1)
    enemy_sprite.center_x = random.randint(LIMIT_LEFT, LIMIT_RIGHT+1)
    # Set a random movement direction for each enemy Sprite.
    enemy_sprite.change_x = int(random.random() * 2 + (DIFFICULTY/10) - 1)
    enemy_sprite.change_y = int(random.random() * 2 + (DIFFICULTY/10) - 1)
    # Set enemy Sprite size.
    enemy_sprite.size = 4
    # Add current Sprite to the list of all Sprites.
    self.list_all_sprites.append(enemy_sprite)
    # Add current Sprite to the list of all enemy Sprites.
    self.list_enemies.append(enemy_sprite)


    # Class for the Sprite that represents an enemy.
    class EnemySprite(arcade.Sprite):
        # Initialize enemy size, movement-type timers, and speed
        def __init__(self, image_file_name, scale):
            super().__init__(image_file_name, scale=scale)
            self.size = 0
            self.timer_rand = 0
            self.timer_smart = 0
            self.speed = 2 + (DIFFICULTY / 10)

        # Move the enemy.
        def update(self):
            # If enemy is at a screen boundary,
            # cause a "bounce" toward opposite direction.
            super().update()
            if self.center_x < LIMIT_LEFT:
                self.center_x = LIMIT_LEFT
                self.change_x *= -1
            if self.center_x > LIMIT_RIGHT:
                self.center_x = LIMIT_RIGHT
                self.change_x *= -1
            if self.center_y > LIMIT_TOP:
                self.center_y = LIMIT_TOP
                self.change_y *= -1
            if self.center_y < LIMIT_BOTTOM:
                self.center_y = LIMIT_BOTTOM
                self.change_y *= -1

        def on_update(self, x_delta):
            # Calculate frames per second and call the variable "fps".
            fps = x_delta * 3600
            # print("fps: " + str(fps))
            # Set up enemy_speedy variable for local-to-this-function use.
            enemy_speedy = 2 + (self.player_sprite.difficulty / 12)

            if not self.game_over:
                # Update all Sprites for Arcade.
                self.list_all_sprites.update()
                # If the player not respawning (invulnerable):
                if not self.player_sprite.respawning:
                    # Get the player Sprite's position so enemies can move toward player, if
                    # intelligent mode is picked.
                    player_pos_x = self.player_sprite.center_x
                    player_pos_y = self.player_sprite.center_y

                    # ENEMY MOVEMENT
                    # Cycle through each enemy in the enemy Sprite list.
                    for enemy in self.list_enemies:
                        # Reset the random seed using the current time, so
                        # we get more truly random numbers when we use the randint()
                        # function below.
                        random.seed(datetime.now() + timedelta(0, enemy_number))
                        # Update the two enemy movement timers in a countdown fashion.
                        enemy.timer_rand -= 1
                        enemy.timer_smart -= 1

                        # Set up/reset variables for enemy direction of movement.
                        dir_x = 0
                        dir_y = 0

                        # Did both enemy movement direction timers run out?
                        if enemy.timer_rand < 1 and enemy.timer_smart < 1:
                            # Random number based on difficulty so below
                            # we can decide if the enemy will move randomly
                            # or toward the Player.
                            random_or_smart = random.randint(1, 20 + (self.player_sprite.difficulty * 2))
                        else:
                            # Make sure no random movment happens.
                            random_or_smart = 1000

                        # Decide whether to move enemy randomly or "intellligently".
                        # Lower the "20" if you want random movement more often.
                        if random_or_smart < 20:
                            # How long to continue in the random direction?
                            enemy.timer_rand = int(fps * 6)  # ~ 6 seconds
                            enemy.timer_smart = 0
                            # Random 8 directions N, S, E, W, NE, SE, NW, SW
                            direction = random.randint(1, 8)
                            if direction == 1:
                                dir_y = 1
                            elif direction == 2:
                                dir_x = 1
                                dir_y = 1
                            elif direction == 3:
                                dir_x = 1
                            elif direction == 4:
                                dir_x = 1
                                dir_y = 1
                            elif direction == 5:
                                dir_y = 1
                            elif direction == 6:
                                dir_y = 1
                                dir_x = 1
                            elif direction == 7:
                                dir_x = 1
                            elif direction == 8:
                                dir_x = 1
                                dir_y = 1
                            enemy.change_x = dir_x * (enemy_speedy - 2)
                            enemy.change_y = dir_y * (enemy_speedy - 2)
                        elif enemy.timer_rand < 1:
                            enemy.timer_rand = 0
                            # If the movement timer for smart movement runs out,
                            # reset it here.
                            if enemy.timer_smart < 1:
                                # Set smart movement timer to random number between
                                # 1 second and 3 seconds.
                                enemy.timer_smart = random.randint(int(fps * 1), int(fps * 3))
                            y_pos = enemy.center_y
                            x_pos = enemy.center_x
                            # If Player Sprite is above enemy, set y direction to up.
                            if player_pos_y > y_pos:
                                dir_y = 1
                            # If Player Sprite is to the right of enemy, set x direction to right.
                            if player_pos_x > x_pos:
                                dir_x = 1
                            # If Player Sprite is below enemy, set y direction to down.
                            if player_pos_y < y_pos:
                                dir_y = -1
                            # If Player Sprite is to the left of enemy, set x direction to left.
                            if player_pos_x < x_pos:
                                dir_x = -1
                            # Set the current enemy Sprite's x and y directions based on above
                            # four tests, modified with speed.
                            enemy.change_x = dir_x * (enemy_speedy - 2)
                            enemy.change_y = dir_y * (enemy_speedy - 2)
                        # Set a new x/y position on the screen for THIS enemy.
                        enemy.center_x += enemy.change_x
                        enemy.center_y += enemy.change_y