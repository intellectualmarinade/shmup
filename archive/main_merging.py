import arcade
import time
import os
import random
import math
import modules.gameover
import modules.audio
import modules.views
import modules.gameover
import modules.infinite_bg as background
from modules.explosion import Explosion

# Scrolling Background Constants
SCREEN_TITLE = "Operation Pew Pew Boom"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
MUSIC_VOLUME = 0.5
window = None

BULLET_SPEED = 8
ENEMY_SPEED = 5
ENEMY_SPEED2 = 2
ENEMY_SPEED3 = 0.5
MOVEMENT_SPEED = 8

MAX_PLAYER_BULLETS = 2
MAX_ENEMY_BULLETS = 6

# This margin controls how close the enemy gets to the left or right side
# before reversing direction.
ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = SCREEN_WIDTH - ENEMY_VERTICAL_MARGIN
LEFT_ENEMY_BORDER = ENEMY_VERTICAL_MARGIN

# How many pixels to move the enemy down when reversing
ENEMY_MOVE_DOWN_AMOUNT = 5

# Game state
GAME_OVER = 1
PLAY_GAME = 0

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
                game_over_view = modules.gameover.GameOverView()
                main.window.show_view(game_over_view)

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

            if arcade.check_for_collision_with_list(self.MyGame.player_sprite, self.enemy_bullet_list):

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

                if len(self.player_list) == 0:
                    game_over_view = modules.gameover.GameOverView
                    self.window.show_view(game_over_view)

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def on_update(self):
        """ Movement and game logic """

        self.MyGame.frame_count += 1

        if len(self.enemy_list) == 0:
            self.startenemy3()


class MyGame(arcade.View):

    def __init__(self):

        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.player_bullet_list = None
        self.game_state = PLAY_GAME
        self.player_sprite = None
        self.score = 0
        self.explosions_list = None
        self.frame_count = 0

        # Populate enemies
        self.enemy1group = None
        self.enemy2group = None
        self.enemy2group = None

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound("./Assets/sounds/rumble.wav")
        self.music = None

        arcade.set_background_color(arcade.color.BLACK)
        background.MyGame.setup(self)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.z_pressed = False

        self.explosion_texture_list = []
        columns = 8
        count = 64
        sprite_width = 256
        sprite_height = 256
        file_name = "./Assets/sprites/container/Tile.png"
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        print(f"Playing {self.music_list[self.current_song]}")
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(MUSIC_VOLUME)
        time.sleep(0.03)

    def setup(self):
        background.MyGame.setup(self)
        self.game_state = PLAY_GAME
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.enemy1group = Enemy1group(self)
        self.enemy2group = Enemy2group(self)
        self.enemy3group = Enemy3group(self)

        self.music_list = ["./Assets/Music/mmpm.mp3"]
        self.current_song = 0
        self.play_song()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("./Assets/sprites/container/playership.png", 0.06)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        background.MyGame.on_draw(self)
        self.player_bullet_list.draw()
        self.player_list.draw()
        self.explosions_list.draw()
        self.enemy1group.on_draw()
        self.enemy2group.on_draw()
        self.enemy3group.on_draw()

        arcade.draw_text(f'Current Leaderboard Rank: NULL', 20, 765, arcade.color.WHITE, 14)
        arcade.draw_text(f"Score: {self.score}", 20, 745, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        if key == arcade.key.Z:
            self.z_pressed = True
            print("Pew")

            # Only allow the user so many bullets on screen at a time to prevent
            # them from spamming bullets.
            if len(self.player_bullet_list) < MAX_PLAYER_BULLETS:
                arcade.play_sound(self.gun_sound)
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 1.0)
                bullet.angle = 90
                bullet.change_y = BULLET_SPEED
                bullet.center_x = self.player_sprite.center_x
                bullet.bottom = self.player_sprite.top
                self.player_bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

        if key == arcade.key.Z:
            self.z_pressed = False

    def process_player_bullets(self):

        # Move the bullets
        self.player_bullet_list.update()

        # Loop through each bullet
        for bullet in self.player_bullet_list:

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy1group.enemy_list)
            hit_list2 = arcade.check_for_collision_with_list(bullet, self.enemy2group.enemy_list)
            hit_list3 = arcade.check_for_collision_with_list(bullet, self.enemy3group.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.update()
                self.explosions_list.append(explosion)

            if len(hit_list2) > 0:
                bullet.remove_from_sprite_lists()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list2[0].center_x
                explosion.center_y = hit_list2[0].center_y
                explosion.update()
                self.explosions_list.append(explosion)

            if len(hit_list3) > 0:
                bullet.remove_from_sprite_lists()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list3[0].center_x
                explosion.center_y = hit_list3[0].center_y
                explosion.update()
                self.explosions_list.append(explosion)

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 150
                arcade.play_sound(self.hit_sound)
                print("Boom")

            for enemy in hit_list2:
                enemy.remove_from_sprite_lists()
                self.score += 400
                arcade.play_sound(self.hit_sound)
                print("Boom")

            for enemy in hit_list3:
                enemy.remove_from_sprite_lists()
                self.score += 1000
                arcade.play_sound(self.hit_sound)
                print("Boom")

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.frame_count += 1

        background.MyGame.update(self, delta_time)
        self.background_list.update()
        self.explosions_list.update()
        self.player_bullet_list.update()
        self.process_player_bullets()

        self.enemy1group.enemy_list.on_update()
        self.enemy1group.enemy_bullet_list.on_update()
        self.enemy1group.update_enemies()
        self.enemy1group.allow_enemies_to_fire()
        self.enemy1group.process_enemy_bullets()

        self.enemy2group.enemy_list.on_update()
        self.enemy2group.enemy_bullet_list.on_update()
        self.enemy2group.update_enemies()
        self.enemy2group.allow_enemies_to_fire()
        self.enemy2group.process_enemy_bullets()

        self.enemy3group.enemy_list.on_update()
        self.enemy3group.enemy_bullet_list.on_update()
        self.enemy3group.update_enemies()
        self.enemy3group.allow_enemies_to_fire()
        self.enemy3group.process_enemy_bullets()

        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy1group.enemy_bullet_list):
            game_over_view = modules.gameover.GameOverView()
            self.main.window.show_view(game_over_view)

        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy2group.enemy_bullet_list):
            game_over_view = modules.gameover.GameOverView()
            main.window.show_view(game_over_view)

        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy3group.enemy_bullet_list):
            game_over_view = modules.gameover.GameOverView()
            main.window.show_view(game_over_view)

        if len(self.player_list) == 0:
            game_over_view = modules.gameover.GameOverView
            main.window.show_view(game_over_view)

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        self.player_list.update()

        if len(self.enemy1group.enemy_list) == 0:
            self.enemy1group.startenemy1()
        if len(self.enemy2group.enemy_list) == 0:
            self.enemy2group.startenemy2()
        if len(self.enemy3group.enemy_list) == 0:
            self.enemy3group.startenemy3()

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        output_total = f"Total Score: {self.total_score}"
        arcade.draw_text(output_total, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 45, arcade.color.WHITE, font_size=35, anchor_x="center")

        arcade.draw_text("Click to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, arcade.color.WHITE, font_size=24, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = gameview.GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = modules.views.MenuView()
    mygame = MyGame()
    window.show_view(start_view)
    window.total_score = 0
    arcade.run()


if __name__ == "__main__":
    main()
