import arcade
import random

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY1 = 0.8
SPRITE_SCALING_ENEMY2 = 0.8
SPRITE_SCALING_ENEMY3 = 1.5
SPRITE_SCALING_LASER = 0.8
SPRITE_SCALING_ENEMYLASER = 2.2

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Operation Pew Pew Boom"

BULLET_SPEED = 8
ENEMY_SPEED = 3
MOVEMENT_SPEED = 8

MAX_PLAYER_BULLETS = 4
MAX_ENEMY_BULLETS = 8


def move_enemy_one(self):
    # Load the textures for the enemies, one facing left, one right
    self.enemy_textures = []
    texture1 = arcade.load_texture("./Assets/sprites/container/enemy01.png", mirrored=True)
    self.enemy_textures.append(texture1)
    texture1 = arcade.load_texture("./Assets/sprites/container/enemy01.png")
    self.enemy_textures.append(texture1)

    # Create rows and columns of enemies
    x_count = random.randrange(1, 4)
    x_start = random.randrange(0, 600)
    x_spacing = random.randrange(100, 200)
    y_count = random.randrange(1, 2)
    y_start = 800
    y_spacing = random.randrange(1, 50)
    for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
        for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
            enemy1 = arcade.Sprite()
            enemy1.scale = SPRITE_SCALING_ENEMY1
            enemy1.texture = self.enemy_textures[1]

            # Position the enemy
            enemy1.center_x = x
            enemy1.center_y = y

            # Add the enemy to the lists
            self.enemy_list.append(enemy1)


def move_enemy_two(self):
    # Load the textures for the enemies, one facing left, one right
    self.enemy_textures = []
    texture2 = arcade.load_texture("./Assets/sprites/container/enemy02.png", mirrored=True)
    self.enemy_textures.append(texture2)
    texture2 = arcade.load_texture("./Assets/sprites/container/enemy02.png")
    self.enemy_textures.append(texture2)

    # Create rows and columns of enemies
    x_count = 1
    x_start = random.choice([-100, 700])
    x_spacing = random.randrange(100, 250)
    y_count = random.randrange(1, 3)
    y_start = random.choice([500, 700])
    y_spacing = 100
    for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
        for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
            enemy2 = arcade.Sprite()
            enemy2.scale = SPRITE_SCALING_ENEMY2
            enemy2.texture = self.enemy_textures[1]

            # Position the enemy
            enemy2.center_x = x
            enemy2.center_y = y

            # Add the enemy to the lists
            self.enemy_list.append(enemy2)


def move_enemy_three(self):
    # Load the textures for the enemies, one facing left, one right
    self.enemy_textures = []
    texture3 = arcade.load_texture("./Assets/sprites/container/enemy03.png", mirrored=True)
    self.enemy_textures.append(texture3)
    texture3 = arcade.load_texture("./Assets/sprites/container/enemy03.png")
    self.enemy_textures.append(texture3)

    # Create rows and columns of enemies
    x_count = random.randrange(1, 4)
    x_start = random.choice([-100, 700])
    x_spacing = random.randrange(100, 300)
    y_count = 1
    y_start = random.randrange(650, 700)
    y_spacing = 100
    for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
        for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
            enemy3 = arcade.Sprite()
            enemy3.scale = SPRITE_SCALING_ENEMY3
            enemy3.texture = self.enemy_textures[1]

            # Position the enemy
            enemy3.center_x = x
            enemy3.center_y = y

            # Add the enemy to the lists
            self.enemy_list.append(enemy3)

