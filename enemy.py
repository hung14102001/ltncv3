from ursina import Entity, Vec3, Vec2, color, collider, destroy

class Enemy(Entity):
    def __init__(self, info):
        self.ship = info['ship']
        img_path = f'./Ships/ship_{self.ship}_1.png'
        super().__init__(
            position=Vec2(*info['position']),
            model="quad",
            collider="box",
            texture=img_path,
            scale=Vec3(1, 2, 0)
        )

        self.name_tag = Entity(
            parent=self,
            text=info['username'],
            position=Vec3(0, 1.3, -1),
            scale=Vec2(5, 3),
            billboard=True,
            origin=Vec2(0, 0)
        )

        self.maxHealth = 100
        self.health = float(info['health'])
        self.id = info['id']

    def update(self):
        if not hasattr(self, 'health'): return
        try:
            if self.health <= 0:
                self.texture = f'./Ships/ship_{self.ship}_4.png'
            elif self.health <= 30:
                self.texture = f'./Ships/ship_{self.ship}_3.png'
            elif self.health <= 70:
                self.texture = f'./Ships/ship_{self.ship}_2.png'
            
        except AttributeError as e:
            print(e)
