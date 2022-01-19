from ursina import Entity, Vec3, Vec2
import os


class Enemy(Entity):
    def __init__(self, info):
        self.ship = info['ship'] + 1
        img_path = os.path.join("Ships", f"ship_{self.ship}_1.png")
        super().__init__(
            position=Vec2(*info['position']),
            model="quad",
            collider="box",
            texture=img_path,
            scale=Vec3(1, 2, 0)
        )

        self.damage = float(info['damage'])
        self.maxHealth = float(info['health'])
        self.health = self.maxHealth
        self.id = info['id']

    def update(self):
        if not hasattr(self, 'health'):
            return
        try:
            if self.health <= 0:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_4.png")
            elif self.health <= self.maxHealth*.3:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_3.png")
            elif self.health <= self.maxHealth*.7:
                self.texture = os.path.join("Ships", f"ship_{self.ship}_2.png")

        except AttributeError as e:
            print(e)
