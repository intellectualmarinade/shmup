import arcade
import random
import math
import modules.infinite_bg as background
from modules.explosion import Explosion

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Operation Pew Pew Boom: Not for Distribution"

BULLET_SPEED = 8
ENEMY_SPEED = 5
ENEMY_SPEED2 = 2
ENEMY_SPEED3 = 0.5
MOVEMENT_SPEED = 8

MAX_PLAYER_BULLETS = 2
MAX_ENEMY_BULLETS = 6

MUSIC_VOLUME = 0.2

# This margin controls how close the enemy gets to the left or right side
# before reversing direction.
ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = SCREEN_WIDTH - ENEMY_VERTICAL_MARGIN
LEFT_ENEMY_BORDER = ENEMY_VERTICAL_MARGIN

# How many pixels to move the enemy down when reversing
ENEMY_MOVE_DOWN_AMOUNT = 5

# Game state
# These numbers represent "states" that the game can be in.
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3

class Enemy1group:

    def __init__(self, MyGame):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_textures = arcade.SpriteList()
        self.enemy_change_x = -ENEMY_SPEED
        self.enemy_change_y = -ENEMY_SPEED
        self.MyGame = MyGame
        self.startenemy1()

    def startenemy1(self):
        # Load the textures for the enemies, one facing left, one right
        self.enemy_textures = []
        texture = arcade.load_texture("./Assets/sprites/container/enemy01.png", mirrored=True)
        self.enemy_textures.append(texture)
        texture = arcade.load_texture("./Assets/sprites/container/enemy01.png")
        self.enemy_textures.append(texture)

        # Create rows and columns of enemies
        x_count = random.randrange(2, 4)
        x_start = random.randrange(0, 600)
        x_spacing = random.randrange(50, 200)
        y_count = random.randrange(1, 3)
        y_start = 800
        y_spacing = random.randrange(30, 60)
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
                enemy = arcade.Sprite()
                enemy.scale = 1
                enemy.texture = self.enemy_textures[0]

                # Position the enemy
                enemy.center_x = x
                enemy.center_y = y

                # Add the enemy to the lists
                self.enemy_list.append(enemy)

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

    def on_draw(self):
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()

    def update_enemies(self):

        # Move the enemy vertically
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        for enemy in self.enemy_list:
            enemy.center_y += self.enemy_change_y

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        # Did we hit the edge above, and need to move the enemy down?
        if move_down:
            # Yes
            for enemy in self.enemy_list:
                # Move enemy down
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT
                # Flip texture on enemy so it faces the other way
                if self.enemy_change_x > 0:
                    enemy.texture = self.enemy_textures[0]
                else:
                    enemy.texture = self.enemy_textures[1]

                if enemy.top < 0:
                    enemy.remove_from_sprite_lists()

    def allow_enemies_to_fire(self):
        """
        See if any enemies will fire this frame.
        """
        # Track which x values have had a chance to fire a bullet.
        # Since enemy list is build from the bottom up, we can use
        # this to only allow the bottom row to fire.
        x_spawn = []
        for enemy in self.enemy_list:
            # Adjust the chance depending on the number of enemies. Fewer
            # enemies, more likely to fire.
            chance = 4 + len(self.enemy_list) * 4

            # Fire if we roll a zero, and no one else in this column has had
            # a chance to fire.
            if len(self.enemy_bullet_list) < MAX_ENEMY_BULLETS:
                if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                    # Create a bullet
                    bullet = arcade.Sprite("./Assets/sprites/container/purp_bullet.png", 2.2)

                    # bullet attributes
                    bullet.angle = 180
                    bullet.change_y = -BULLET_SPEED
                    bullet.center_x = enemy.center_x
                    bullet.top = enemy.bottom

                    # Add the bullet to the appropriate list
                    self.enemy_bullet_list.append(bullet)

            # Ok, this column has had a chance to fire. Add to list so we don't
            # try it again this frame.
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):

        # Move the bullets
        self.enemy_bullet_list.update()

        # Loop through each bullet
        for bullet in self.enemy_bullet_list:
            arcade.check_for_collision_with_list(bullet, self.MyGame.player_list)

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.MyGame.player_sprite, self.enemy_bullet_list):
                self.MyGame.current_state = GAME_OVER

            # Check this bullet to see if it hit the player
            hit_list = arcade.check_for_collision_with_list(bullet, self.MyGame.player_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                self.MyGame.player_sprite.remove_from_sprite_lists()
                explosion = Explosion(self.MyGame.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.update()
                self.MyGame.explosions_list.append(explosion)
                arcade.play_sound(self.MyGame.hit_sound)
                print("You went Boom")

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def on_update(self):
        """ Movement and game logic """

        if len(self.enemy_list) == 0:
            self.startenemy1()


class Enemy2group:

    def __init__(self, MyGame):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_textures = arcade.SpriteList()
        self.enemy_change_x = -ENEMY_SPEED2
        self.enemy_change_y = -ENEMY_SPEED2
        self.MyGame = MyGame
        self.frame_count = 0
        self.startenemy2()

    def startenemy2(self):
        # Load the textures for the enemies, one facing left, one right
        self.enemy_textures = []
        texture = arcade.load_texture("./Assets/sprites/container/enemy02.png", mirrored=True)
        self.enemy_textures.append(texture)
        texture = arcade.load_texture("./Assets/sprites/container/enemy02.png")
        self.enemy_textures.append(texture)

        # Create rows and columns of enemies
        x_count = random.randrange(2, 4)
        x_start = random.randrange(200, 400)
        x_spacing = random.randrange(50, 200)
        y_count = random.randrange(1, 3)
        y_start = random.randrange(600, 750)
        y_spacing = random.randrange(50, 80)
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
                enemy = arcade.Sprite()
                enemy.scale = 1.4
                enemy.texture = self.enemy_textures[0]

                # Position the enemy
                enemy.center_x = x
                enemy.center_y = y

                # Add the enemy to the lists
                self.enemy_list.append(enemy)

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

    def on_draw(self):
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()

    def update_enemies(self):

        # Move the enemy vertically
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        for enemy in self.enemy_list:
            enemy.center_y += self.enemy_change_y

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        # Did we hit the edge above, and need to move the enemy down?
        if move_down:
            # Yes
            for enemy in self.enemy_list:
                # Move enemy down
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT
                # Flip texture on enemy so it faces the other way
                if self.enemy_change_x > 0:
                    enemy.texture = self.enemy_textures[0]
                else:
                    enemy.texture = self.enemy_textures[1]

                if enemy.top < 0:
                    enemy.remove_from_sprite_lists()

    def allow_enemies_to_fire(self):

        # Code specific for Enemy Aim
        for enemy in self.enemy_list:

            # Rotate the enemy at current location to face the player each frame
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.MyGame.player_sprite.center_x
            dest_y = self.MyGame.player_sprite.center_y

            # This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) - 90

            # Shoot every 60 frames change of shooting each frame
            if self.MyGame.frame_count % 45 == 0:
                bullet = arcade.Sprite("Assets/sprites/container/laserRed01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y
                bullet.angle = math.degrees(angle)
                bullet.change_x = math.cos(angle) * 8
                bullet.change_y = math.sin(angle) * 5

                self.enemy_bullet_list.append(bullet)

    def process_enemy_bullets(self):

        # Move the bullets
        self.enemy_bullet_list.update()

        # Loop through each bullet
        for bullet in self.enemy_bullet_list:
            arcade.check_for_collision_with_list(bullet, self.MyGame.player_list)

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.MyGame.player_sprite, self.enemy_bullet_list):
                self.MyGame.current_state = GAME_OVER

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.MyGame.player_list)

            # You exploded
            if len(hit_list) > 0:
                self.MyGame.player_sprite.remove_from_sprite_lists()
                explosion = Explosion(self.MyGame.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.update()
                self.MyGame.explosions_list.append(explosion)
                arcade.play_sound(self.MyGame.hit_sound)
                print("You went Boom")

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def on_update(self):
        """ Movement and game logic """

        self.MyGame.frame_count += 1

        if len(self.enemy_list) == 0:
            self.startenemy2()


class Enemy3group:
    def __init__(self, MyGame):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_textures = arcade.SpriteList()
        self.enemy_change_x = -ENEMY_SPEED3
        self.enemy_change_y = -ENEMY_SPEED3
        self.MyGame = MyGame
        self.frame_count = 0
        self.startenemy3()

    def startenemy3(self):
        # Load the textures for the enemies, one facing left, one right
        self.enemy_textures = []
        texture = arcade.load_texture("./Assets/sprites/container/enemy03.png", mirrored=True)
        self.enemy_textures.append(texture)
        texture = arcade.load_texture("./Assets/sprites/container/enemy03.png")
        self.enemy_textures.append(texture)

        # Create rows and columns of enemies
        x_count = random.randrange(1, 3)
        x_start = random.randrange(0, 600)
        x_spacing = random.randrange(100, 300)
        y_count = random.randrange(1, 3)
        y_start = 800
        y_spacing = random.randrange(100, 250)
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
                enemy = arcade.Sprite()
                enemy.scale = 2.0
                enemy.texture = self.enemy_textures[0]

                # Position the enemy
                enemy.center_x = x
                enemy.center_y = y

                # Add the enemy to the lists
                self.enemy_list.append(enemy)

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

    def on_draw(self):
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()

    def update_enemies(self):

        # Move the enemy vertically
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        for enemy in self.enemy_list:
            enemy.center_y += self.enemy_change_y

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        # Did we hit the edge above, and need to move the enemy down?
        if move_down:
            # Yes
            for enemy in self.enemy_list:
                # Move enemy down
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT
                # Flip texture on enemy so it faces the other way
                if self.enemy_change_x > 0:
                    enemy.texture = self.enemy_textures[0]
                else:
                    enemy.texture = self.enemy_textures[1]

                if enemy.top < 0:
                    enemy.remove_from_sprite_lists()

    def allow_enemies_to_fire(self):

        # Code specific for Enemy Aim
        for enemy in self.enemy_list:

            # Rotate the enemy at current location to face the player each frame
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.MyGame.player_sprite.center_x
            dest_y = self.MyGame.player_sprite.center_y

            # This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) - 90

            # Shoot every 60 frames change of shooting each frame
            if self.MyGame.frame_count % 240 == 0:
                bullet = arcade.Sprite("Assets/sprites/container/yellow_cannon.png")
                bullet.center_x = start_x
                bullet.center_y = start_y
                bullet.angle = math.degrees(angle)
                bullet.change_x = math.cos(angle) * 12
                bullet.change_y = math.sin(angle) * 15

                self.enemy_bullet_list.append(bullet)

    def process_enemy_bullets(self):

        # Move the bullets
        self.enemy_bullet_list.update()

        # Loop through each bullet
        for bullet in self.enemy_bullet_list:
            arcade.check_for_collision_with_list(bullet, self.MyGame.player_list)

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.MyGame.player_sprite, self.enemy_bullet_list):
                self.MyGame.current_state = GAME_OVER

                # Check this bullet to see if it hit a enemy
                hit_list = arcade.check_for_collision_with_list(bullet, self.MyGame.player_list)

                # You exploded
                if len(hit_list) > 0:
                    self.MyGame.player_sprite.remove_from_sprite_lists()
                    explosion = Explosion(self.MyGame.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    explosion.update()
                    self.MyGame.explosions_list.append(explosion)
                    arcade.play_sound(self.MyGame.hit_sound)
                    print("You went Boom")

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def on_update(self):
        """ Movement and game logic """

        self.MyGame.frame_count += 1

        if len(self.enemy_list) == 0:
            self.startenemy3()

