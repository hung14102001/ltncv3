from ursina import *

class AudioSwitch(Entity):
    def __init__(self,parent,sound):
        super().__init__(parent=parent)
        self.a=sound
        self.switch_text=Text('SOUND',parent=parent,position=(-0.25,0.1,0),scale=2,color=color.black)
        self.on_off_switch = ButtonGroup(('on', 'off'), parent=parent, min_selection=1,position=(0.1,0.1,0), default='on', selected_color=color.azure)

        self.switch_text2=Text('MUSIC',parent=parent,position=(-0.25,-0.05,0),scale=2,color=color.black)
        self.on_off_switch2 = ButtonGroup(('on', 'off'), parent=parent, min_selection=1,position=(0.1,-0.05,0), default='on', selected_color=color.azure)

        def on_value_changed():
            if self.on_off_switch.value == 'on':
                self.a.volume=1
            else :
                self.a.volume=0

        self.on_off_switch.on_value_changed = on_value_changed
