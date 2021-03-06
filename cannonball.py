import os
import math
from enemy import Enemy
from ursina import *
from sea import CoinPart
from helper import createAnimation


class CannonBall(Entity):
    def __init__(self, player, position, rediffX, rediffY, damage, network, enemy=None):

        super().__init__(
            model='quad',
            texture=os.path.join("Cannon", "cannonBall.png"),
            position=position,
            z=0,
            scale_x=0.18,
            scale_y=0.18,
            collider='sphere'
        )

        self.rediffX = rediffX
        self.rediffY = rediffY

        try:
            self.rad = math.atan(rediffY/rediffX)
        except ZeroDivisionError:
            self.rad = math.atan(rediffY/0.0001)

        self.player = player
        self.enemy = enemy
        self.network = network
        self.damage = damage

        self.speed = 0.3

        destroy(self, delay=10)

    def update(self):
        if not hasattr(self, 'rediffX'):
            return
        if self.rediffX < 0:
            self.x -= math.cos(self.rad)*self.speed
            self.y -= math.sin(self.rad)*self.speed
        else:
            self.x += math.cos(self.rad)*self.speed
            self.y += math.sin(self.rad)*self.speed

        if self.enemy:
            hitinfo = self.intersects(ignore=(self, self.enemy))
        else:
            hitinfo = self.intersects(ignore=(self, self.player))
        if hitinfo.hit:
            if not self.enemy:
                if isinstance(hitinfo.entity, Enemy):
                    hitinfo.entity.health -= self.damage
                    self.network.send_health(hitinfo.entity)
                elif isinstance(hitinfo.entity, CoinPart):
                    destroy(hitinfo.entity)

                from menu import MainMenu
                mm = MainMenu.getInstance()
                if mm.a.volume == 1:
                    Audio('stuff_explosion', loop=False, autoPlay=True)
                    
                else:
                    Audio('stuff_explosion',volume = 0)
                    
                createAnimation(self.x, self.y, os.path.join(
                    'Assets', 'Effects', 'explosion'))

            destroy(self)
