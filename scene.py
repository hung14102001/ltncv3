from ursina import *
from sea import Plant, Coin
from enemy import Enemy

class Scene():
    def __init__(self):
        self.coin=Coin()
        self.plant = Plant()
        Enemy(Vec2(5,5), '1111', '234', './Ships/ship_5.png')

    


