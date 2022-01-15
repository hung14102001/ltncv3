from ursina import *
from scene import  Scene

class GameOver(Entity):
    def __init__(self,sound):
        super().__init__(parent=camera.ui)
        self.bg = Entity(parent=self,model='quad',texture='game_over_bg.jpg',position=(0,0.02,0),scale=(1,0.6,0))
        self.mess = Entity(parent=self,model='quad',texture='game_over.png',position=(0,0,0),scale=1)

        if sound.volume==1:
            self.a=Audio('game_over',loop=False,autoPlay=True)
        else:
            self.a.pause()
            
        def play_again_btn_action():
            self.a.stop()
            self.disable()

        def home_back_action():
            pass

        Entity(parent=self,model='quad',texture='play_btn.jpg',position=(0.2,-0.3),scale=(0.5,0.1))
        Button("Play again", parent=self,position=(0.2,-0.3), scale=(0.24, 0.06), color=rgb(255,255,255,0),
                text_color=color.black,on_click=play_again_btn_action)
        
        Entity(parent=self,model='quad',texture='options_btn.jpg',position=(-0.2,-0.3),scale=(0.5,0.1))
        Button("Home", parent=self,position=(-0.2,-0.3), scale=(0.24, 0.06), color=rgb(255,255,255,0),
                text_color=color.black,on_click=play_again_btn_action)

class Completed(Entity):
    def __init__(self,sound):
        super().__init__(
            parent=camera.ui,
            enabled=True
        )
        self.bg2 = Entity(parent=self,model='cube',texture='win_game_bg2.jpg',position=(-0.01,0.15,0),scale=1)
        self.bg = Entity(parent=self,model='cube',texture='win_game_bg.jpg',position=(0,-0.1,0),scale=0.7)
        self.mess = Entity(parent=self,model='quad',texture='win_game_text.png',position=(0.01,0.1,0),scale=0.5)

        if sound.volume==1:
            self.a=Audio('level_completed',loop=False,autoPlay=True)
        else:
            self.a.pause()
            
        def play_again_btn_action():
            self.a.stop()
            self.disable()
            #Scene()

        Entity(parent=self,model='quad',texture='play_btn.jpg',position=(0.2,-0.3),scale=(0.5,0.1))
        Button("Countine", parent=self,position=(0.2,-0.3), scale=(0.24, 0.06), color=rgb(255,255,255,0),
                text_color=color.black,on_click=play_again_btn_action)
        
        Entity(parent=self,model='quad',texture='options_btn.jpg',position=(-0.2,-0.3),scale=(0.5,0.1))
        Button("Home", parent=self,position=(-0.2,-0.3), scale=(0.24, 0.06), color=rgb(255,255,255,0),
                text_color=color.black,on_click=play_again_btn_action)
