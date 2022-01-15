import os

from re import A, escape
from ursina import *
from random import randint
from cannonball import CannonBall
from player import Player
from sea import Sea, Plant, Coin
from minimap import MiniMap
# from network import Network
from ursina.camera import Camera
from enemy import Enemy

# from ursina import texture

# input
def input(key):
    if key == 'esc':
        app.running = False
    # move left if hold arrow left

    if mouse.left:
        # Audio('audios/shot.wav').play()
        if time.time() - player.reload > 1:
            player.reload = time.time()
            CannonBall(player,player.x, player.y, mouse.x, mouse.y)
    

# display the background
app = Ursina()
player = Player(-15,-15)
background = Sea()

plant = Plant()
coin = Coin()
minimap = MiniMap(player, background)
# camera.z = -100
Enemy(Vec2(5,5), '1111', '234', './Ships/ship_4.png')

app.run()