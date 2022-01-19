from ursina import *
from menu import MainMenu
import os

# display the background
app = Ursina()

window.title = 'My game'                # The window title

# Custom window
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen

# Do not show the in-game red X that loses the window
window.exit_button.visible = False
window.fps_counter.enabled = False

Text.default_font = os.path.join('Assets', 'Font', 'aAbstractGroovy.ttf')

main_menu = MainMenu()
# gameover=GameOver()

app.run()
