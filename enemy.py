from ursina import Entity, Vec3, Vec2, color, collider, destroy

class Enemy(Entity):
    def __init__(self, info):
        if info['ship'] == 1:
            img_path = './Ships/ship_1.png'
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

        self.healthbar = Entity(
            parent=self,
            model="quad",
            position=Vec3(0, -.3, -1),
            color=color.rgb(0, 255, 0),
            scale=Vec2(1.5,.1)
        )

        self.maxHealth = 100
        self.health = float(info['health'])
        self.id = info['id']

    def update(self):
        try:
            while self.health == None:
                continue
            if self.health <= 0:
                pass
            self.healthbar.scale_x = self.health / self.maxHealth * 1.5
        except AttributeError as e:
            print(e)
