from ursina import *

class LoadingWheel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.point = Entity(parent=self, 
                            model=Circle(24, mode='point', thickness=.03), 
                            color='#f5af42', 
                            y=.7, 
                            scale=2, 
                            texture='circle')
        self.point2 = Entity(parent=self, 
                             model=Circle(12, mode='point', thickness=.03), 
                             color='#f5af42', 
                             y=.7, 
                             scale=1, 
                             texture='circle')

        self.scale = .025
        self.text_entity = Text(world_parent=self, 
                                text='Loading...', 
                                origin=(0,2), 
                                color=color.light_gray)
        self.y = -.25

        self.bg = Entity(parent=self, 
                         model='quad',
                         scale_x=camera.aspect_ratio, 
                         color=color.black, 
                         z=1)
        self.bg.scale *= 400

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.point.rotation_y += 5
        self.point2.rotation_y += 3