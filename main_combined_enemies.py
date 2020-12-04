import arcade
import random
import time
import enemy
import modules.infinite_bg as background
from modules.explosion import Explosion

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.8
SPRITE_SCALING_LASER = 0.8
SPRITE_SCALING_ENEMYLASER = 2.2
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Operation Pew Pew Boom"

BULLET_SPEED = 8
ENEMY_SPEED = 3
MOVEMENT_SPEED = 8

MAX_PLAYER_BULLETS = 4
MAX_ENEMY_BULLETS = 6

MUSIC_VOLUME = 0.4

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

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.enemy_textures = None
        self.game_state = PLAY_GAME
        self.player_sprite = None
        self.score = 0
        self.explosions_list = None

        # Enemy movement
        self.enemy_change_x = -ENEMY_SPEED
        self.enemy_change_y = -ENEMY_SPEED

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.music = None

        arcade.set_background_color(arcade.color.BLACK)
        background.MyGame.setup(self)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.z_pressed = False

        self.explosion_texture_list = []
        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    enemy.move_enemy_one
    enemy.move_enemy_two
    enemy.move_enemy_three

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
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite("./Assets/sprites/container/playership.png", 0.08)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        self.music_list = ["./Assets/Music/peritune-rapid4.mp3"]
        self.current_song = 0
        self.play_song()

        enemy.move_enemy_one(self)
        enemy.move_enemy_two(self)
        enemy.move_enemy_three(self)

    def on_draw(self):
        arcade.start_render()
        background.MyGame.on_draw(self)

        # Draw all the sprites.
        self.enemy_list.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.player_list.draw()
        self.explosions_list.draw()

        arcade.draw_text(f'Leaderboard Rank: NULL', 20, 765, arcade.color.WHITE, 14)
        arcade.draw_text(f"Score: {self.score}", 20, 745, arcade.color.WHITE, 14)

        # Draw game over if the game state is such
        if self.game_state == GAME_OVER:
            arcade.draw_text(f"GAME OVER", 140, 400, arcade.color.WHITE, 55)

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

            # Only allow the user so many bullets on screen at a time to prevent
            # them from spamming bullets.
            if len(self.player_bullet_list) < MAX_PLAYER_BULLETS:
                # Gunshot sound
                arcade.play_sound(self.gun_sound)

                # Create a bullet
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

                # The image points to the right, and we want it to point up. So
                # rotate it.
                bullet.angle = 90

                # Give the bullet a speed
                bullet.change_y = BULLET_SPEED

                # Position the bullet
                bullet.center_x = self.player_sprite.center_x
                bullet.bottom = self.player_sprite.top

                # Add the bullet to the appropriate lists
                self.player_bullet_list.append(bullet)

        if self.game_state == GAME_OVER:
            return

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
                    bullet = arcade.Sprite("./Assets/sprites/container/purp_bullet.png", SPRITE_SCALING_ENEMYLASER)

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
            hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list):

                self.game_state = GAME_OVER

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def process_player_bullets(self):

        # Move the bullets
        self.player_bullet_list.update()

        # Loop through each bullet
        for bullet in self.player_bullet_list:

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.update()
                self.explosions_list.append(explosion)

            # For every enemy we hit, add to the score and remove the enemy
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1000

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        background.MyGame.update(self, delta_time)
        self.background_list.update()

        self.explosions_list.update()

        if self.game_state == GAME_OVER:
            return

        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()
        self.process_player_bullets()

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

        if len(self.enemy_list) == 0:
            enemy.move_enemy_one(self)
            enemy.move_enemy_two(self)
            enemy.move_enemy_three(self)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()