import os
from ursina import *
import time
from sea import CoinPart


class Player(Entity):
    def __init__(self, position, info, network, coins, sound):

        self.ship = info['type'] + 1

        super().__init__(
            model='quad',
            collider='box',
            texture=os.path.join("Ships", f"ship_{self.ship}_1.png"),
            position=position,
            score=0,
            rotation_z=0,
            z=0,
            scale_x=1,
            scale_y=2,
        )
        self.id = 0
        self.speed = 0.15
        self.reload = time.time()
        self.level = 1
        self.network = network
        self.coins = coins
        self.a = sound

        self.damage = float(info['dmg'])
        self.maxHealth = float(info['hp'])
        self.health = self.maxHealth
        self.death_shown = False

    def update(self):
        if not self.health:
            return
        elif self.health > 0:

            angle = self.rotation_z
            increaseX = 0
            increaseY = 0
            decreaseX = 0
            decreaseY = 0
            if held_keys['up arrow'] or held_keys['w']:
                increaseY = self.speed
                angle = 180

            if held_keys['down arrow'] or held_keys['s']:
                decreaseY = self.speed
                angle = 0
            if held_keys['left arrow'] or held_keys['a']:
                decreaseX = self.speed
                angle = 90
                if held_keys['up arrow'] or held_keys['w']:
                    angle = 135
                    decreaseX = self.speed / 1.414
                    increaseY = self.speed / 1.414
                elif held_keys['down arrow'] or held_keys['s']:
                    angle = 45
                    decreaseX = self.speed / 1.414
                    decreaseY = self.speed / 1.414

            if held_keys['right arrow'] or held_keys['d']:
                increaseX = self.speed
                angle = -90
                if held_keys['up arrow'] or held_keys['w']:
                    angle = -135
                    increaseX = self.speed / 1.414
                    increaseY = self.speed / 1.414

                elif held_keys['down arrow'] or held_keys['s']:
                    angle = -45
                    increaseX = self.speed / 1.414
                    decreaseY = self.speed / 1.414
            if held_keys['g']:
                camera.x = self.x
                camera.y = self.y
                camera.z = -50
            self.rotation_z = angle

            camera.y = self.y
            camera.x = self.x

            if self.health <= self.maxHealth*.3:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_3.png")
            elif self.health <= self.maxHealth*.7:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_2.png")

            try:
                hitinfo = self.intersects()
            except AttributeError as e:
                print(e)
            if hitinfo:
                hitinfo = self.intersects()
                if hitinfo.hit:
                    if isinstance(hitinfo.entity, CoinPart):
                        self.isSounding('pick_item')
                        if not self.death_shown:
                            self.score += 1
                        index = hitinfo.entity.index
                        self.coins.destroy_coin(index)

                        self.network.send_coin(index)

                    x = hitinfo.point.x
                    y = hitinfo.point.y
                    if x == .5:
                        decreaseX = 0
                    if x == -.5:
                        increaseX = 0
                    if y == .5:
                        decreaseY = 0
                    if y == -.5:
                        increaseY = 0

            self.x = self.x + increaseX - decreaseX
            self.y = self.y + increaseY - decreaseY

    def isSounding(self, k):
        if self.a.volume == 1:
            Audio(k, pitch=1, loop=False, autoplay=True)
        else:
            Audio(k, pitch=1, volume=0)
