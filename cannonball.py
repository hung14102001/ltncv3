import os, math
from enemy import Enemy
from ursina import Entity, collider, destroy
class CannonBall(Entity):
    def __init__(self, player, position, rediffX, rediffY, damage, network, enemy=None):

        super().__init__(
            model='quad',
            texture=os.path.join("Cannon", "cannonBall.png"),
            position=position,
            z=0,
            scale_x=0.18,
            scale_y=0.18,
            collider = 'sphere'
        )
        self.player = player
        self.enemy = enemy
        self.network = network
        self.damage = damage

        self.speed = 0.3

        self.rediffX = rediffX
        self.rediffY = rediffY
        self.rad = math.atan(rediffY/rediffX)
        destroy(self,delay=10)
        
    def update(self):
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

            destroy(self)