from ursina import *

class AudioSwitch(Entity):
    def __init__(self, parent, sound):
        super().__init__(parent=parent)
        self.a = sound
        self.sound_text = Text(
            'SOUND', parent=parent, position=(-0.25, 0, 0), scale=2, color=color.black)
        self.sound_switch = ButtonGroup(('on', 'off'), parent=parent, min_selection=1, position=(
            0.1, 0, 0), default='on', selected_color=color.azure)

        def sound_on_value_changed():
            if self.sound_switch.value == 'on':
                self.a.volume = 1
            else:
                self.a.volume = 0

        self.sound_switch.on_value_changed = sound_on_value_changed
