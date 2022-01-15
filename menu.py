import os
from ursina import *
from re import A, escape
from random import randint
from player import Player
from cannonball import CannonBall
from sea import Sea
from minimap import MiniMap
from scene import Scene
from chacracter import Chacracter
from loading import LoadingWheel
from direct.stdpy import thread
from ursina.prefabs.health_bar import HealthBar
from options import AudioSwitch
from ursina import printvar
from endgame import GameOver, Completed
        
class MainMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=camera.ui, 
            ignore_paused=True)

        # Create empty entities that will be parents of our menus content
        #self.title = Entity(parent=self,model='quad',texture='welcome2.jpg',position=(0,0.2),scale=1) 
        self.bg = Sprite('Image/bg2.png')
        self.main_menu = Entity(parent=self, enabled=True)
        self.choose_menu = Entity(parent=self, enabled=False)
        self.options_menu = Entity(parent=self,enabled=False)

        self.player = Player(-15, -15)
        self.background = Sea()
        self.minimap = MiniMap(self.player, self.background)

        self.loading_screen = LoadingWheel(enabled=False)     
        self.a = Audio('start_game',pitch=1,loop=False,autoPlay=True)

        def isSounding(sound):
            if self.a.volume==1:
                self.b=Audio(sound,pitch=1,loop=False,autoplay=True)
            else:
                self.b.pause()

        # [MAIN MENU] WINDOWN START
        def display(item, state):               # Show/hide item on screen
            if state:
                item.enabled = True
            else:
                item.enabled = False

        def show(*argv):
            for arg in argv:
                display(arg, True)

        def hide(*argv):
            for arg in argv:
                display(arg, False)
                
        def choose1():
            hide(self.choose_menu)
            show(self.loading_screen)
            self.player.texture= os.path.join("Ships", list[0])
            isSounding('mouse_click')
            t = time.time()
        
            try:
                thread.start_new_thread(function=loadTextures, args='')
            except Exception as e:
                print('error starting thread', e)

            print('---', time.time()-t)

        def choose2():
            hide(self.choose_menu)
            show(self.loading_screen)
            self.player.texture= os.path.join("Ships", list[1])
            isSounding('mouse_click')
            t = time.time()
            
            try:
                thread.start_new_thread(function=loadTextures, args='')
            except Exception as e:
                print('error starting thread', e)

            print('---', time.time()-t)

        def choose3():
            hide(self.choose_menu)
            show(self.loading_screen)
            self.player.texture= os.path.join("Ships", list[2])
            isSounding('mouse_click')

            t = time.time()
        
            try:
                thread.start_new_thread(function=loadTextures, args='')
            except Exception as e:
                print('error starting thread', e)

            print('---', time.time()-t)

        def choose4():
            hide(self.choose_menu)
            show(self.loading_screen)
            self.player.texture= os.path.join("Ships", list[3])
            isSounding('mouse_click')
            t = time.time()
        
            try:
                thread.start_new_thread(function=loadTextures, args='')
            except Exception as e:
                print('error starting thread', e)

            print('---', time.time()-t)

        def choose5():
            hide(self.choose_menu)
            show(self.loading_screen)
            self.player.texture= os.path.join("Ships", list[4])
            isSounding('mouse_click')
            
            t = time.time()
        
            try:
                thread.start_new_thread(function=loadTextures, args='')
            except Exception as e:
                print('error starting thread', e)

            print('---', time.time()-t)
        list = ["ship_2.png","ship_3.png","ship_4.png","ship_5.png","ship_6.png"]

        self.chac1=Chacracter('Chacracter 1',self.choose_menu,-0.4,0.1,list[0],choose1)
        self.chac2=Chacracter('Chacracter 2',self.choose_menu,0,0.1,list[1],choose2)
        self.chac3=Chacracter('Chacracter 3',self.choose_menu,0.4,0.1,list[2],choose3)
        self.chac4=Chacracter('Chacracter 4',self.choose_menu,-0.2,-0.2,list[3],choose1)
        self.chac5=Chacracter('Chacracter 5',self.choose_menu,0.2,-0.2,list[4],choose1)

        def loadTextures():
            textures_to_load = ['brick', 'shore', 'grass', 'heightmap'] * 25
            bar = HealthBar(max_value=len(textures_to_load), value=0, position=(-.5,-.35,-2), scale_x=1, animation_duration=0, world_parent=self.loading_screen, bar_color='#f5af42')
            for i, t in enumerate(textures_to_load):
                load_texture(t)
                print(i)
                bar.value = i+1

            print('loaded textures')
            hide(self.loading_screen)
            show(self.player,self.background,self.minimap)
            show(self.player.healthbar_bg,self.player.healthbar)
            Scene()
            self.player.text.visible=True

         # Reference of our action function for play button
        def play_btn():
            isSounding('mouse_click')
            hide(self.bg, self.main_menu)
            show(self.choose_menu)

        # Reference of our action function for options button
        def options_menu_btn():
            isSounding('mouse_click')
            hide(self.main_menu)
            show(self.options_menu)
        
        # Reference of our action function for quit button
        def quit_game():
            isSounding('mouse_click')
            application.quit()

        # Button list
        Entity(parent=self.main_menu, model='quad',texture='play_btn.jpg',position=(0,0,0),scale=(0.5,0.1,1))
        Button('Play',parent=self.main_menu,position=(0,0,0),scale=(0.2,0.06,1),color=rgb(255,255,255,0),on_click=play_btn)

        Entity(parent=self.main_menu, model='quad',texture='options_btn.jpg',position=(0,-0.15,0),scale=(0.5,0.1,1))
        Button('Options',parent=self.main_menu,position=(0,-0.15,0),scale=(0.2,0.06,1),color=rgb(255,255,255,0),on_click=options_menu_btn)

        Entity(parent=self.main_menu, model='quad',texture='exit_btn.jpg',position=(0,-0.3,0),scale=(0.5,0.1,1))
        Button('Exit',parent=self.main_menu,position=(0,-0.3,0),scale=(0.2,0.06,1),color=rgb(255,255,255,0),on_click=quit_game)
        # [MAIN MENU] WINDOW END

        # [CHOOSE CHACRACTER] WINDOW START
        Entity(parent=self.choose_menu,model='quad',texture='title.png',position=(0,0.4),scale=(0.9,0.2))
        Text("CHOOSE CHACRACTER",parent=self.choose_menu,position=(-0.2,0.42,0), scale=1.5,color=color.black)

        def play_back_btn_action():
            isSounding('mouse_click')
            hide(self.choose_menu)
            show(self.bg,self.main_menu)

        Entity(parent=self.choose_menu,model='quad',texture='back_btn.jpg',position=(-0.76,0.44),scale=(0.5,0.3))
        Button(parent=self.choose_menu, position=(-0.8,0.4,0),scale=(0.1,0.05,1),color=rgb(255,255,255,0),on_click=play_back_btn_action)
        # [CHOOSE CHOOSE] WINDOW END

        # [OPTIONS MENU] WINDOW START
        # Title of our menu
        Entity(parent=self.options_menu,model='quad',texture='title.png',position=(0,0.4,0),scale=(0.8,0.2,1))
        Entity(parent=self.options_menu,model='quad',texture='title_bg.png',position=(0,0,0),scale=(0.8,0.5,1))
        Text("OPTIONS MENU",parent=self.options_menu,position=(-0.12,0.42,0), scale=1.5,color=color.black)

        AudioSwitch(self.options_menu,self.a)

        # Reference of our action function for back button
        def options_back_btn_action():
            isSounding('mouse_click')
            show(self.main_menu)
            hide(self.options_menu)

        # Button
        Entity(parent=self.options_menu,model='quad',texture='back_btn2.png',position=(-0.03,-0.3,0),scale=(0.5,0.5,1))
        Button('Back',parent=self.options_menu, position=(0,-0.33,0),scale=(0.15,0.05,1),text_color=color.black,color=rgb(255,255,255,0),on_click=options_back_btn_action)
        # [OPTIONS MENU] WINDOW END
        
        # Here we can change attributes of this class when call this class
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def input(self,key):
        # move left if hold arrow left
        if mouse.left:
            if time.time() - self.player.reload > 1:
                self.player.reload = time.time()
                self.canno = CannonBall(self.player, self.player.x, self.player.y, mouse.x, mouse.y)
                if self.player.enabled:
                    self.canno.enabled = True
                else:
                    self.canno.enabled = False