import os
from ursina import *
import time
from sea import CoinPart, Coin, Restrictor


class Player(Entity):
    def __init__(self, position, ship, network, coins):

        super().__init__(
            model='quad',
            collider='box',
            texture=os.path.join("Ships", f"ship_{ship}_1.png"),
            position=position,
            score=0,
            rotation_z=0,
            z=0,
            scale_x=1,
            scale_y=2,
        )
        self.ship = ship
        self.id = 0
        self.speed = 0.15
        self.reload = time.time()
        self.level = 1
        self.network = network
        self.coins = coins

        self.health = 100
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

            if self.health <= 30:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_3.png")
            elif self.health <= 70:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_2.png")

            try:
                hitinfo = self.intersects()
            except AttributeError as e:
                print(e)
            if hitinfo:
                hitinfo = self.intersects()
                if hitinfo.hit:
                    if isinstance(hitinfo.entity, CoinPart):
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
