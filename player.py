import os
from ursina import *
import time
from sea import CoinPart, Coin
class Player(Entity):
    def __init__(self, position, network, coins):

        super().__init__(
            model='cube',
            collider = 'box',
            texture=os.path.join("Ships", "ship_4.png"),
            position=position,
            score = 0,
            rotation_z = 0,
            z=0,
            scale_x=1,
            scale_y=2,
            # text = Text(text="Score: " + str(score), color=color.rgb(0,0,0), scale = 2.5, position=(-0.8,0.5,0)),
        )
        self.speed = 0.15
        self.reload = time.time()
        self.level = 1
        self.network = network
        self.coins = coins
        self.healthbar_pos = Vec2(0, -0.1)
        self.healthbar_size = Vec2(0.2, 0.02)
        self.healthbar_bg = Entity(
            parent=camera.ui,
            model="quad",
            color= color.rgb(255, 0, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )
        self.healthbar = Entity(
            parent=camera.ui,
            model="quad",
            color=color.rgb(0, 255, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )
        
        self.health = 20
        self.game_ended = False
        text = Text(text="Score: " +str(self.score), color=color.rgb(0,0,0), scale = 2.5, position=(-0.8,0.5,0))
        
    def update(self):
        self.healthbar.scale_x = self.healthbar_size[0]*self.health/20
        if self.health > 0:
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
            if held_keys['left arrow'] or held_keys['a'] :
                decreaseX = self.speed
                angle = 90
                if held_keys['up arrow'] or held_keys['w']:
                    angle = 135
                    decreaseX = self.speed /1.414
                    increaseY = self.speed /1.414
                elif held_keys['down arrow'] or held_keys['s']:
                    angle = 45
                    decreaseX = self.speed /1.414
                    decreaseY = self.speed /1.414

            if held_keys['right arrow'] or held_keys['d'] :
                increaseX = self.speed
                angle = -90
                if held_keys['up arrow'] or held_keys['w']:
                    angle = -135
                    increaseX = self.speed /1.414
                    increaseY = self.speed /1.414

                elif held_keys['down arrow'] or held_keys['s']:
                    angle = -45
                    increaseX = self.speed /1.414
                    decreaseY = self.speed /1.414
            if held_keys['g']:
                camera.x = self.x
                camera.y = self.y
                camera.z = -50
            self.rotation_z = angle
            
            camera.x = self.x
            camera.y = self.y
            camera.z = -30


            hitinfo = self.intersects()
            if hitinfo.hit:
                if isinstance(hitinfo.entity, CoinPart):
                    if not self.game_ended:
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
            
