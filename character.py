from ursina import *
import functools


class Character(Button):
    def __init__(self, char_txt, parent, position, icon, submit, param=1):
        super().__init__(
            parent=parent,
            text=char_txt,
            text_color=color.black,
            position=position,
            scale_y=0.15,
            scale_x=.1,
            text_origin=(0.4, -1),
            icon=icon,
            color=rgb(255, 255, 255, 0),
            on_click=submit
        )
        Entity(parent=self, model='quad', texture='next_btn.png',
               position=(0, -0.9), scale=(3.5, 2))
        Button(parent=self, position=(0, -0.84), color=rgb(255, 255, 255, 0),
               scale=(1.8, .4), on_click=functools.partial(submit, param))
