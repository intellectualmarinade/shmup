import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 800
SCROLL_SPEED = 0.25

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):

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

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()

    def update(self, delta_time):

        #reset the images when they go past the screen
        if self.background_sprite.bottom == -IMAGE_HEIGHT:
            self.background_sprite.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT // 2

        if self.background_sprite_2.bottom == -IMAGE_HEIGHT:
            self.background_sprite_2.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT // 2

        self.background_list.update()

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()