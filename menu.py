import random
from ursina import *
from character import Character
from options import AudioSwitch
from ursina import printvar
from game import Game


class MainMenu(Entity):
    import json
    from web3 import Web3

    __instance = None
    w3 = Web3(Web3.WebsocketProvider(
        'wss://ropsten.infura.io/ws/v3/6d3df8badba94fd78e849a7d703fb914'))

    with open("./BattleShipNFT.json") as f:
        info_json = json.load(f)
    abi = info_json["abi"]

    myContract = w3.eth.contract(
        address='0x17b3bc609d87faD52Ae31D782df67ffD421Fe672', abi=abi)

    @staticmethod
    def getInstance():
        """ Static access method. """
        return MainMenu.__instance

    def __init__(self, **kwargs):

        super().__init__(
            parent=camera.ui,
            ignore_paused=True
        )
        if MainMenu.__instance == None:
            MainMenu.__instance = self

        # Create empty entities that will be parents of our menus content
        #self.title = Entity(parent=self,model='quad',texture='welcome2.jpg',position=(0,0.2),scale=1)
        self.user_address = '0'
        self.input_field = InputField(paren=self, y=.1)
        self.bg = Entity(parent=self, model='quad',
                         texture='./Assets/Image/bg2.png.jpg', position=(0, 0), scale=(2, 1))
        self.main_menu = Entity(parent=self, enabled=True)
        self.choose_menu = Entity(parent=self, enabled=False)
        self.options_menu = Entity(parent=self, enabled=False)

        # self.loading_screen = LoadingWheel(enabled=False)
        self.a = Audio('start_game', pitch=1, loop=False, autoPlay=True)

        self.ships = []

        def isSounding(sound):
            if self.a.volume == 1:
                self.b = Audio(sound, pitch=1, loop=False, autoplay=True)
            else:
                self.b.pause()

        # [MAIN MENU] WINDOWN START

        def chooseChar(offset):

            Game(self.ships[offset])

            self.hide(self.choose_menu)
            isSounding('mouse_click')

        lst = ['ship_1.png', "ship_2_1.png", "ship_3_1.png",
               "ship_4_1.png", "ship_5_1.png", "ship_6_1.png"]

        # Reference of our action function for play button

        def play_btn():
            isSounding('mouse_click')
            if self.input_field.text != self.user_address:
                if self.fetchOwnerShips():
                    if len(self.ships) > 0:
                        for i in range(len(self.ships)):
                            x = (-.6 + .4*i) if i < 3 else (-.8 + .4*(i-2))
                            y = .1 if i < 3 else -.2
                            position = Vec3(x, y, 1)
                            id = self.ships[i]['id']
                            type = self.ships[i]['type']

                            Character(
                                f'ID {id}',
                                self.choose_menu,
                                position,
                                lst[type],
                                chooseChar,
                                param=i
                            )

            self.hide(self.input_field)
            self.hide(self.bg, self.main_menu)
            self.show(self.choose_menu)

        # Reference of our action function for options button
        def options_menu_btn():
            isSounding('mouse_click')
            self.hide(self.main_menu)
            self.show(self.options_menu)

        # Reference of our action function for quit button
        def quit_game():
            isSounding('mouse_click')
            application.quit()

        # Button lst
        Entity(parent=self.main_menu, model='quad',
               texture='play_btn.jpg', position=(0, 0, 0), scale=(0.5, 0.1, 1))
        Button('Play', parent=self.main_menu, position=(0, 0, 0), scale=(
            0.2, 0.06, 1), color=rgb(255, 255, 255, 0), on_click=play_btn)

        Entity(parent=self.main_menu, model='quad', texture='options_btn.jpg',
               position=(0, -0.15, 0), scale=(0.5, 0.1, 1))
        Button('Options', parent=self.main_menu, position=(0, -0.15, 0),
               scale=(0.2, 0.06, 1), color=rgb(255, 255, 255, 0), on_click=options_menu_btn)

        Entity(parent=self.main_menu, model='quad', texture='exit_btn.jpg',
               position=(0, -0.3, 0), scale=(0.5, 0.1, 1))
        Button('Exit', parent=self.main_menu, position=(0, -0.3, 0),
               scale=(0.2, 0.06, 1), color=rgb(255, 255, 255, 0), on_click=quit_game)
        # [MAIN MENU] WINDOW END

        # [CHOOSE CHARACTER] WINDOW START
        Entity(parent=self.choose_menu, model='quad',
               texture='title.png', position=(0, 0.4), scale=(0.9, 0.2))
        Text("CHOOSE CHARACTER", parent=self.choose_menu,
             position=(-0.2, 0.42, 0), scale=1.5, color=color.black)

        def play_back_btn_action():
            isSounding('mouse_click')
            self.hide(self.choose_menu)
            self.show(self.bg, self.main_menu)

        Entity(parent=self.choose_menu, model='quad',
               texture='back_btn.jpg', position=(-0.76, 0.44), scale=(0.5, 0.3))
        Button(parent=self.choose_menu, position=(-0.8, 0.4, 0), scale=(0.1,
               0.05, 1), color=rgb(255, 255, 255, 0), on_click=play_back_btn_action)
        # [CHOOSE CHOOSE] WINDOW END

        # [OPTIONS MENU] WINDOW START
        # Title of our menu
        Entity(parent=self.options_menu, model='quad',
               texture='title.png', position=(0, 0.4, 0), scale=(0.8, 0.2, 1))
        Entity(parent=self.options_menu, model='quad',
               texture='title_bg.png', position=(0, 0, 0), scale=(0.8, 0.5, 1))
        Text("OPTIONS MENU", parent=self.options_menu,
             position=(-0.12, 0.42, 0), scale=1.5, color=color.black)

        AudioSwitch(self.options_menu, self.a)

        # Reference of our action function for back button
        def options_back_btn_action():
            isSounding('mouse_click')
            self.show(self.main_menu)
            self.hide(self.options_menu)

        # Button
        Entity(parent=self.options_menu, model='quad', texture='back_btn2.png',
               position=(-0.03, -0.3, 0), scale=(0.5, 0.5, 1))
        Button('Back', parent=self.options_menu, position=(0, -0.33, 0), scale=(0.15, 0.05, 1),
               text_color=color.black, color=rgb(255, 255, 255, 0), on_click=options_back_btn_action)
        # [OPTIONS MENU] WINDOW END

        # Here we can change attributes of this class when call this class
        for key, value in kwargs.items():
            setattr(self, key, value)

    def display(self, item, state):               # Show/hide item on screen
        if state:
            item.enabled = True
        else:
            item.enabled = False

    def show(self, *items):
        for arg in items:
            self.display(arg, True)

    def hide(self, *items):
        for arg in items:
            self.display(arg, False)

    def fetchOwnerShips(self):
        try:
            shipIds = MainMenu.myContract.caller.getShipsByOwner(
                self.input_field.text
            )
        except:
            return False
        myShips = []
        for i in shipIds:
            ship = MainMenu.myContract.caller.battleShips(i)
            ship = {
                'id': ship[0],
                'type': ship[1],
                'exp': ship[2],
                'level': ship[3],
                'hp': ship[4],
                'dmg': ship[5],
            }
            myShips.append(ship)

        self.ships = myShips
        self.user_address = self.input_field.text
        return True
