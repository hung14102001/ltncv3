from ursina import camera, Entity, Vec2, color
class MiniMap(Entity):
    def __init__(self, player, sea):
        super().__init__(
            scale=0.28,
            parent=camera.ui,
            model="quad",
            position=Vec2(0.74, 0.35),
            color=color.rgb(161, 234, 255)
        )

        self.player = player
        black = color.rgb(0, 0, 0)
        red = color.rgb(255, 0, 0)
        green = color.rgb(0, 255, 0)
        bistre = color.rgb(205, 133, 63)
        goldenbrown = color.rgb(205, 133, 63)
        self.playerRep = Entity(
            parent=self,
            scale=.05,
            model='circle',
            position=(player.x/40,player.y/40),
            color=red
        )
        self.boRep = Entity(
            parent=self,
            scale=1.2,
            model='quad',
            position=(0.03, 0.07, 0.0001),
            color=goldenbrown
        )
        self.cotRep = Entity(
            parent=self,
            scale=(.05, 0.2),
            model='quad',
            position=(0,-0.38,0),
            color=bistre
        )
        self.cotRep = Entity(
            parent=self,
            scale=(0.2, .05),
            model='quad',
            position=(-0.38,0,0),
            color=bistre
        )
        self.cotRep = Entity(
            parent=self,
            scale=(.05, 0.2),
            model='quad',
            position=(0,0.38,0),
            color=bistre
        )
        self.cotRep = Entity(
            parent=self,
            scale=(0.2, .05),
            model='quad',
            position=(0.38,0,0),
            color=bistre
        )

        self.daoRep = Entity(
            parent=self,
            scale=(.095, .095),
            model='quad',
            position=(0.175,0.175,0),
            color=bistre
        )

        self.daoRep = Entity(
            parent=self,
            scale=(.095, .095),
            model='quad',
            position=(-0.175,0.175,0),
            color=bistre
        )

        self.daoRep = Entity(
            parent=self,
            scale=(.095, .095),
            model='quad',
            position=(0.175,-0.175,0),
            color=bistre
        )

        self.daoRep = Entity(
            parent=self,
            scale=(.095, .095),
            model='quad',
            position=(-0.175,-0.175,0),
            color=bistre
        )

        self.daotoRep = Entity(
            parent=self,
            scale=(.14, .14),
            model='quad',
            position=(0,0,0),
            color=bistre
        )
        self.daotoRep = Entity(
            parent=self,
            scale=(.1, .1),
            model='quad',
            position=(0,0,-0.1),
            color=green
        )
    def update(self):
        self.playerRep.x = self.player.x/40
        self.playerRep.y = self.player.y/40