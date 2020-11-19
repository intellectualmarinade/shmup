import arcade
import main as gameview
import modules.scores

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 45, arcade.color.WHITE, font_size=35, anchor_x="center")

        arcade.draw_text("Click to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, arcade.color.WHITE, font_size=24, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = gameview.GameView()
        self.window.show_view(game_view)
