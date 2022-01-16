import os

from ursina import *
from random import randint
from ursina.camera import Camera
from menu import MainMenu
from endgame import GameOver

# display the background
app = Ursina()

window.title = 'My game'                # The window title

# Custom window
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen

# Do not show the in-game red X that loses the window
window.exit_button.visible = False
window.fps_counter.enabled = False

Text.default_font  = 'Font/aAbstractGroovy.ttf'

main_menu = MainMenu()
#gameover=GameOver()

app.run()