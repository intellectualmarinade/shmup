import arcade
import os
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "FRUSTRATIONS"
BULLET_SPEED = 10
SPRITE_SCALING_LASER = 0.8


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

        # bg color
        arcade.set_background_color(arcade.color.BLACK)
        # hide the mouse

        self.set_mouse_visible(False)
        self.frame_count = 0

        # Sprite lists
        self.enemy_list = None
        self.ebullet_list = None
        self.pbullet_list = None
        self.player_list = None

        # Setup the player
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
        self.ebullet_list = arcade.SpriteList()
        self.pbullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Add player ship
        self.player_sprite = Player("./Assets/sprites/container/nextpng.png", 0.08)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

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
        enemy.center_x = 320
        enemy.center_y = 275
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add mid-left enemy ship
        enemy = arcade.Sprite("./Assets/sprites/container/enemy2.png", 1.0)
        enemy.center_x = 175
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
        self.ebullet_list.draw()
        self.pbullet_list.draw()

        output = f"Current Score: {self.score}"
        arcade.draw_text(output, 10, 750, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        # Gunshot sound
        arcade.play_sound(self.gun_sound)
        # Create a bullet
        pbullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

        # The image points to the right, and we want it to point up. So
        # rotate it.
        pbullet.angle = 90

        # Give the bullet a speed
        pbullet.change_y = BULLET_SPEED

        # Position the bullet
        pbullet.center_x = self.player_sprite.center_x
        pbullet.bottom = self.player_sprite.top

        # Add the bullet to the appropriate lists
        self.pbullet_list.append(pbullet)

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        self.frame_count += 1

        # Call update on bullet sprites
        self.pbullet_list.update()

        # Loop through each bullet
        for pbullet in self.pbullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(pbullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1000

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if pbullet.bottom > SCREEN_HEIGHT:
                pbullet.remove_from_sprite_lists()

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
        self.pbullet_list.update()

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