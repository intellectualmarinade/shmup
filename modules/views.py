import arcade
import main_merging as gameview
import arcade.gui
from arcade.gui import UIManager
import modules.menu

# Scrolling Background Constants
SCREEN_TITLE = "Operation Pew Pew Boom - Level 2"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    def on_click(self):
        """ Called when user lets off button """
        print("Click click boom. ")

class MenuView(arcade.View):

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        self.texture = arcade.load_texture("./Assets/title.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.ui_manager = UIManager()

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        arcade.start_render()

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

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

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("./Assets/intro.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = gameview.MyGame()
        game_view.setup()
        self.window.show_view(game_view)