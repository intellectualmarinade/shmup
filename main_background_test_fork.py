import arcade
import time
import os
import math

SPRITE_SCALING = 0.5
SPRITE_SCALING_LASER = 0.8

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Operation Pew Pew Boom - Level 2"

# Scrolling Background
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 800
SCROLL_SPEED = 3

MUSIC_VOLUME = 0.1
MOVEMENT_SPEED = 5
BULLET_SPEED = 5
window = None


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Operation Pew Pew Boom", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=35, anchor_x="center")
        arcade.draw_text("Imagine mindblowing graphics here.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Use the arrow keys for movement.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press the z key to fire.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)


class GameView(arcade.View):

    def __init__(self):

        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.ARSENIC)

        self.frame_count = 0

        # Variables that will hold sprite lists
        self.background_list = None
        self.player_list = None
        self.pbullet_list = None
        self.enemy_list = None
        self.ebullet_list = None
        self.player = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        # Load sounds
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.z_pressed = False

        # Variables used to manage our music. See setup() for giving them
        # values.
        self.music_list = []
        self.current_song = 0
        self.music = None

        # Pre-load the animation frames of explosions. We don't do this in the __init__
        # of the explosion sprite because it
        # takes too long and would cause the game to pause.
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
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

        self.background_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.pbullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.ebullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()

        # first background image
        self.background_list = arcade.SpriteList()

        self.background_sprite = arcade.Sprite("./Assets/sprites/container/seamlessspace_0.png")

        self.background_sprite.center_x = IMAGE_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_sprite.change_y = -SCROLL_SPEED

        self.background_list.append(self.background_sprite)

        # second background image
        self.background_sprite_2 = arcade.Sprite("./Assets/sprites/container/seamlessspace_0.png")

        self.background_sprite_2.center_x = SCREEN_WIDTH // 2
        self.background_sprite_2.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT // 2
        self.background_sprite_2.change_y = -SCROLL_SPEED

        self.background_list.append(self.background_sprite_2)

        # Add player ship
        self.player_sprite = Player("./Assets/sprites/container/nextpng.png", 0.08)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.score = 0

        # Add top-left big-enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy.png", 1.0)
        enemy.center_x = 240
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add top-right big-enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy.png", 1.0)
        enemy.center_x = 440
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add mid-right enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy2.png", 1.0)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = 400
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add mid-left enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy2.png", 1.0)
        enemy.center_x = 100
        enemy.center_y = 400
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add mid-mid enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy2.png", 1.0)
        enemy.center_x = 300
        enemy.center_y = 400
        enemy.angle = 180
        self.enemy_list.append(enemy)

        self.music_list = ["./Assets/Music/electronic-senses-indigo.mp3"]
        self.current_song = 0
        self.play_song()

    def on_draw(self):

        arcade.start_render()
        self.background_list.draw()
        self.player_list.draw()
        self.pbullet_list.draw()
        self.enemy_list.draw()
        self.ebullet_list.draw()
        self.explosions_list.draw()

        output = f"Current Score: {self.score}"
        arcade.draw_text(output, 10, 750, arcade.color.WHITE, 14)

    def update(self, delta_time):

        #reset the images when they go past the screen
        if self.background_sprite.bottom == -IMAGE_HEIGHT:
            self.background_sprite.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT // 2

        if self.background_sprite_2.bottom == -IMAGE_HEIGHT:
            self.background_sprite_2.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT // 2

        self.background_list.update()

    def on_update(self, delta_time):

        self.frame_count += 1
        self.explosions_list.update()

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.ebullet_list.update()
        self.player_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.ebullet_list)

        # Loop through each colliding sprite, remove it
        for ebullet in hit_list:
            ebullet.kill()

        if len(hit_list) > 0:
            ebullet.remove_from_sprite_lists()

            # Make an explosion
            explosion = Explosion(self.explosion_texture_list)

            # Move it to the location of the coin
            explosion.center_x = hit_list[0].center_x
            explosion.center_y = hit_list[0].center_y

            # Call update() because it sets which image we start on
            explosion.update()

            # Add to a list of sprites that are explosions
            self.explosions_list.append(explosion)

        # If we've collected all the games, then move to a "GAME_OVER"
        # state.
        if len(self.player_list) == 0:
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

        # Code specific to background music
        position = self.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()

        # Code specific for Enemy Aim
        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
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

                # Angle the bullet sprite
                ebullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
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
            arcade.play_sound(self.gun_sound)
            # Create a bullet
            pbullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

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


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
