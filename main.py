import arcade
import random
import math
import time
import timeit
import modules.infinite_bg as background
from modules.explosion import Explosion
from modules.enemy import Enemy1group
from modules.enemy import Enemy2group
from modules.enemy import Enemy3group

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

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.frame_count = 0
        print("MyGame class Started")

        # Variables that will hold sprite lists
        self.player_list = None
        self.player_bullet_list = None
        self.player_sprite = None
        self.score = 0
        self.explosions_list = None

        # Start 'state' will be showing the first page of instructions.
        self.current_state = INSTRUCTIONS_PAGE_0

        # Variables used to calculate frames per second
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

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

        # STEP 1: Put each instruction page in an image. Make sure the image
        # matches the dimensions of the window, or it will stretch and look
        # ugly. You can also do something similar if you want a page between
        # each level.
        self.instructions = []
        texture = arcade.load_texture("./Assets/title.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("./Assets/intro.png")
        self.instructions.append(texture)

    def setup(self):
        background.MyGame.setup(self)
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.enemy1group = Enemy1group(self)
        self.enemy2group = Enemy2group(self)
        self.enemy3group = Enemy3group(self)

        self.set_mouse_visible(False)

        self.music_list = ["./Assets/Music/peritune-rapid4.mp3"]
        self.current_song = 0
        self.play_song()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("./Assets/sprites/container/playership.png", 0.06)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        start_x = 300
        start_y = 500
        arcade.draw_text("Mission Failed",
                         start_x, start_y, arcade.color.WHITE, 54, width=500, align="center",
                         anchor_x="center", anchor_y="center")

        start_x = 300
        start_y = 450
        arcade.draw_text(f"Your Final Score: {self.score}",
                         start_x, start_y, arcade.color.WHITE, 24, width=500, align="center",
                         anchor_x="center", anchor_y="center")

        start_x = 300
        start_y = 20
        arcade.draw_text("CLICK TO RESTART GAME",
                         start_x, start_y, arcade.color.WHITE, 14, width=500, align="center",
                         anchor_x="center", anchor_y="center")

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

    def draw_game(self):
        background.MyGame.on_draw(self)

        # Draw all the sprites.
        self.player_bullet_list.draw()
        self.player_list.draw()
        self.explosions_list.draw()
        self.enemy1group.on_draw()
        self.enemy2group.on_draw()
        self.enemy3group.on_draw()

        # --- Calculate FPS

        fps_calculation_freq = 60
        # Once every 60 frames, calculate our FPS
        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, 20, 745, arcade.color.WHITE, 14)

        arcade.draw_text(f"Current Score: {self.score}", 20, 765, arcade.color.WHITE, 14)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        else:
            self.draw_game_over()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING

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
                arcade.play_sound(self.gun_sound, 0.2)
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
                arcade.play_sound(self.hit_sound, 0.4)
                print("Boom")

            for enemy in hit_list2:
                enemy.remove_from_sprite_lists()
                self.score += 400
                arcade.play_sound(self.hit_sound, 0.4)
                print("Boom")

            for enemy in hit_list3:
                enemy.remove_from_sprite_lists()
                self.score += 1000
                arcade.play_sound(self.hit_sound, 0.4)
                print("Boom")

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.frame_count += 1
        self.explosions_list.update()

        if self.current_state == GAME_RUNNING:
            background.MyGame.update(self, delta_time)
            self.background_list.update()
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

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
