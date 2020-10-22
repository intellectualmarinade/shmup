import arcade
import time
import os
import math

SPRITE_SCALING = 0.5
SPRITE_SCALING_LASER = 0.8

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Operation Pew Pew Boom - Basic Movement & Firing"
MUSIC_VOLUME = 0.1
MOVEMENT_SPEED = 8
BULLET_SPEED = 9
window = None

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


class GameView(arcade.View):

    def __init__(self):

        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.ARSENIC)

        self.frame_count = 0

        # Variables that will hold sprite lists
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

        self.player_list = arcade.SpriteList()
        self.pbullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.ebullet_list = arcade.SpriteList()

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
        self.player_list.draw()
        self.pbullet_list.draw()
        self.enemy_list.draw()
        self.ebullet_list.draw()

        output = f"Current Score: {self.score}"
        arcade.draw_text(output, 10, 750, arcade.color.WHITE, 14)

    def on_update(self, delta_time):

        self.frame_count += 1

        position = self.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()



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
