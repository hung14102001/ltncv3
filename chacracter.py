from ursina import *

class Chacracter(Button):
    def __init__(self,char_txt,parent,x,y,icon,submit):
        super().__init__(
            parent=parent,
            text=char_txt,
            text_color=color.black,
            position=(x,y,1), 
            scale=0.15, 
            text_origin=(0.4,-1),
            icon=icon,
            color=rgb(255,255,255,0), 
            on_click=submit
        )
        Entity(parent=self,model='quad',texture='next_btn.png',position=(0,-0.9),scale=(2.3,2))
        Button(parent=self,position=(0,-0.84),color=rgb(255,255,255,0),scale=(1.8,0.4),on_click=submit)
                
