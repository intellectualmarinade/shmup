import arcade
import random

SCREEN_TITLE = "Operation Pew Pew Boom"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
MOVEMENT_SPEED = 5
BULLET_SPEED = 5
SPRITE_SCALING = 0.5
MUSIC_VOLUME = 0.8
window = None
SCALE = 1
DIFFICULTY = 5
ENEMY_COUNT_INITIAL = DIFFICULTY + 2
ENEMY_SPEED = 2 + (DIFFICULTY/10)
SPACE_OFFSCREEN = 1
LIMIT_LEFT = -SPACE_OFFSCREEN
LIMIT_RIGHT = SCREEN_WIDTH + SPACE_OFFSCREEN
LIMIT_BOTTOM = -SPACE_OFFSCREEN
LIMIT_TOP = SCREEN_HEIGHT + SPACE_OFFSCREEN
SCREEN_FROM_DATABASE = False
ID_SCREEN = 1

SCALE = 1
DIFFICULTY = 5
ENEMY_COUNT_INITIAL = DIFFICULTY + 2
ENEMY_SPEED = 2 + (DIFFICULTY/10)

SPACE_OFFSCREEN = 1
LIMIT_LEFT = -SPACE_OFFSCREEN
LIMIT_RIGHT = SCREEN_WIDTH + SPACE_OFFSCREEN
LIMIT_BOTTOM = -SPACE_OFFSCREEN
LIMIT_TOP = SCREEN_HEIGHT + SPACE_OFFSCREEN
SCREEN_FROM_DATABASE = False
ID_SCREEN = 1

# Sprite that represents an enemy.
class EnemySprite(arcade.Sprite):
    # Initialize enemy size, movement-type timers, and speed
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
        self.timer_rand = 0
        self.timer_smart = 0
        self.speed = 2 + (DIFFICULTY/10)

    # Move the enemy.
    def update(self):
        # If enemy hits screen boundary,
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