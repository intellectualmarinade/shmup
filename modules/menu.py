import arcade
import arcade.gui
from arcade.gui import UIManager
import modules.views

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    def on_click(self):
        """ Called when user lets off button """
        print("Click click boom. ")

class SelectView(arcade.View):
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        arcade.start_render()

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 12
        right_column_x = 3 * self.window.width // 4

        # right side elements
        button = MyFlatButton(
            'Start Game',
            center_x=right_column_x,
            center_y=y_slot * 3,
            width=155,
            # height=20
        )
        self.ui_manager.add_ui_element(button)

        button = MyFlatButton(
            'Options',
            center_x=right_column_x,
            center_y=y_slot * 2,
            width=110,
            # height=20
        )
        self.ui_manager.add_ui_element(button)

        button = MyFlatButton(
            'High Scores',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=160,
            # height=20
        )
        self.ui_manager.add_ui_element(button)

if __name__ == '__main__':
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    view = SelectView()
    window.show_view(view)
    arcade.run()