import arcade
import time
import os
import math
import shelve
import modules.gameover
import modules.audio
import modules.views
import modules.gameover
import modules.infinite_bg as background
from modules.explosion import Explosion
from modules.player import Player

# Scrolling Background Constants
SCREEN_TITLE = "Operation Pew Pew Boom"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
MOVEMENT_SPEED = 5
BULLET_SPEED = 5
SPRITE_SCALING = 0.5
MUSIC_VOLUME = 0.1
window = None

# Game state
GAME_OVER = 1
PLAY_GAME = 0


class GameView(arcade.View):

    def __init__(self):

        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.ARSENIC)

        background.MyGame.setup(self)

        self.frame_count = 0
        self.time_taken = 0

        self.player_list = None
        self.pbullet_list = None
        self.enemy_list = None
        self.ebullet_list = None
        self.player = None
        self.explosions_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.z_pressed = False

        self.music_list = []
        self.current_song = 0
        self.music = None
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")

        self.explosion_texture_list = []
        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"
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
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def setup(self):

        background.MyGame.setup(self)
        self.player_list = arcade.SpriteList()
        self.pbullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.ebullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()

        # Add player ship
        self.player_sprite = Player("./Assets/sprites/container/playership.png", 0.08)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.score = 0

        # Add top-right big-enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy01.png", 1.0)
        enemy.center_x = 440
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add mid-mid enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy02.png", 1.0)
        enemy.center_x = 300
        enemy.center_y = 400
        enemy.angle = 180
        self.enemy_list.append(enemy)

        self.music_list = ["./Assets/Music/electronic-senses-indigo.mp3"]
        self.current_song = 0
        self.play_song()

    def on_draw(self):

        arcade.start_render()
        background.MyGame.on_draw(self)
        self.player_list.draw()
        self.pbullet_list.draw()
        self.enemy_list.draw()
        self.ebullet_list.draw()
        self.explosions_list.draw()

        output = f"Current Score: {self.score}"
        arcade.draw_text(output, 10, 750, arcade.color.WHITE, 14)

        output = f"Leaderboard Rank: {self.score}"
        arcade.draw_text(output, 10, 770, arcade.color.WHITE, 14)

    def update(self, delta_time):

        background.MyGame.update(self, delta_time)
        self.background_list.update()

    def on_update(self, delta_time):

        self.frame_count += 1
        self.explosions_list.update()
        self.ebullet_list.update()
        self.player_list.update()

        if arcade.check_for_collision_with_list(self.player_sprite, self.ebullet_list):
            game_over_view = modules.gameover.GameOverView()
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)


        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.ebullet_list)

        for ebullet in hit_list:
            ebullet.kill()

        if len(hit_list) > 0:
            ebullet.remove_from_sprite_lists()
            explosion = Explosion(self.explosion_texture_list)
            explosion.center_x = hit_list[0].center_x
            explosion.center_y = hit_list[0].center_y
            explosion.update()
            self.explosions_list.append(explosion)

        if len(self.player_list) == 0:
            game_over_view = modules.gameover.GameOverView
            game_over_view.time_taken = self.time_taken
            self.window.show_view(game_over_view)

        # Code specific to background music
        position = self.music.get_stream_position()
        if position == 0.0:
            self.advance_song()
            self.play_song()

        # Code specific for Enemy Aim
        for enemy in self.enemy_list:

            # Rotate the enemy at current location to face the player each frame
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) - 90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                ebullet = arcade.Sprite("Assets/sprites/container/laserRed01.png")
                ebullet.center_x = start_x
                ebullet.center_y = start_y
                ebullet.angle = math.degrees(angle)
                ebullet.change_x = math.cos(angle) * BULLET_SPEED
                ebullet.change_y = math.sin(angle) * BULLET_SPEED

                self.ebullet_list.append(ebullet)

        # Get rid of the bullet when it flies off-screen
        for ebullet in self.ebullet_list:
            if ebullet.top < 0:
                ebullet.remove_from_sprite_lists()

        self.ebullet_list.update()

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

        for pbullet in self.pbullet_list:

            # Check this bullet to see if it hit an enemy (collision detection)
            hit_list = arcade.check_for_collision_with_list(pbullet, self.enemy_list)

            # If it did, then remove the bullet
            if len(hit_list) > 0:
                pbullet.remove_from_sprite_lists()

                # Make an explosion
                explosion = Explosion(self.explosion_texture_list)

                # Move it to the location of the coin
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y

                # Call update() because it sets which image we start on
                explosion.update()

                # Add to a list of sprites that are explosions
                self.explosions_list.append(explosion)

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1000
                self.window.total_score += 1000

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if pbullet.bottom > SCREEN_HEIGHT:
                pbullet.remove_from_sprite_lists()

            # Get rid of the bullet when it flies off-screen
            for pbullet in self.pbullet_list:
                if pbullet.top < 0:
                    pbullet.remove_from_sprite_lists()

            self.pbullet_list.update()

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
            # Gunshot sound
            arcade.play_sound(self.gun_sound, volume=0.1)
            # Create a bullet
            pbullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")

            # This is to point the player's bullet up
            pbullet.angle = 90

            # Give the bullet a speed
            pbullet.change_y = BULLET_SPEED

            # Position the bullet
            pbullet.center_x = self.player_sprite.center_x
            pbullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate lists
            self.pbullet_list.append(pbullet)

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


def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = modules.views.MenuView()
    game_view = GameView()
    window.show_view(start_view)
    window.total_score = 0
    arcade.run()


if __name__ == "__main__":
    main()
