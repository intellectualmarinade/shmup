import arcade
import os
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TEST"
BULLET_SPEED = 10


class MyGame(arcade.Window):
    """ Main application class """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.BLACK)

        self.frame_count = 0

        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
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

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Add player ship
        self.player = arcade.Sprite("./Assets/sprites/container/nextpng.png", 0.07)
        self.player_list.append(self.player)

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

        # Add mid-mid enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy2.png", 1.0)
        enemy.center_x = 100
        enemy.center_y = 400
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Variables used to manage our music. See setup() for giving them
        # values.
        self.music_list = ["./Assets/Music/electronic-senses-indigo.mp3"]
        self.current_song = 0
        self.music = self.music_list

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(MUSIC_VOLUME)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        # time.sleep(0.03)

    def on_draw(self):
        """Render the screen. """

        arcade.start_render()
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

        output = f"Current Score: {self.score}"
        arcade.draw_text(output, 10, 750, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        self.frame_count += 1

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
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 50 == 0:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = y


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()