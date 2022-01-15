from ursina import Entity, Vec3, Vec2, color, collider, destroy

class Enemy(Entity):
    def __init__(self, position: Vec2, identifier: str, username: str, img_path: str):
        super().__init__(
            position=position,
            model="cube",
            collider="box",
            texture=img_path,
            scale=Vec3(1, 2, 0)
        )

        self.name_tag = Entity(
            parent=self,
            text=username,
            position=Vec3(0, 1.3, 0),
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
        self.health = 100
        self.id = identifier
        self.username = username
    def update(self):
        self.healthbar.scale_x = self.health / self.maxHealth * 1.5
        if self.health <= 0:
            destroy(self)
