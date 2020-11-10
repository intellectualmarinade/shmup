import arcade
import main as gameview

# Scrolling Background Constants
SCREEN_TITLE = "Operation Pew Pew Boom - Level 2"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 800
SCROLL_SPEED = 3
MOVEMENT_SPEED = 5
BULLET_SPEED = 5
SPRITE_SCALING = 0.5
SPRITE_SCALING_LASER = 0.8
MUSIC_VOLUME = 0.1
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
        game_view = gameview.GameView()
        game_view.setup()
        self.window.show_view(game_view)