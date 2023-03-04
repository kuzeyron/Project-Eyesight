from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, DictProperty,
                             ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex, platform

from libs.configuration import configuration
from libs.android_hide_system_bars import HideBars
from libs.language import Lang
from libs.wallpaper import Wallpaper

if platform not in {'android', 'ios'}:
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))

Builder.load_string('''
#:import TimeData libs.timedata.TimeData
#:import Contacts libs.contacts.Contacts
#:import AppLauncher libs.applauncher.AppLauncher
#:import DeviceSettings libs.settings.DeviceSettings

<Basement>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            texture: app.background
            size: self.size
            pos: self.pos
        Color:
            rgba: 0, 0, 0, .4
        Rectangle:
            size: self.size
            pos: self.pos

    Screen:
        name: 'home'
        BoxLayout:
            padding: dp(5), dp(5)
            spacing: dp(5)
            orientation: 'vertical'

            TimeData:
                short_press_time: 4 
                long_press_time: 4
                override: True
                on_long_press:
                    root.current = 'settings'
                    root.transition.direction = 'up'

            Contacts:
                id: contacts

            AppLauncher:
                package: 'contacts'
                size_hint_y: .5
                text: app.tr._('Phonebook')

            AppLauncher:
                package: 'messaging'
                size_hint_y: .4
                text: app.tr._('SMS')

            Widget:
                size_hint_y: .4

    Screen:
        name: 'settings'
        on_kv_post: self.add_widget(DeviceSettings())
''')


class Basement(ScreenManager):
    pass


class ProjectSimplifier(App, HideBars):
    background = ObjectProperty(None, allownone=True)
    border_radius = ListProperty([10, ])
    color = ColorProperty()
    coloro = ColorProperty()
    current_selection = DictProperty()
    format_date = StringProperty()
    format_time = StringProperty()
    icon = 'assets/images/icon.png'
    language_language = StringProperty()
    press_delay = NumericProperty(1.5)
    settings_starred_contacts = StringProperty()
    title = StringProperty('Project Eyesight')
    trigger_events = BooleanProperty(False)
    tr = ObjectProperty(None, allownone=True)

    def build(self):
        self.config = config = configuration(['settings', 'format', 'language'])
        self.tr = Lang(config['language'])
        self.background = Wallpaper(source=config['wallpaper'],
                                    crop=None).texture
        color = get_color_from_hex(config['bg_color'])
        opacity = config['color_opacity']
        self.border_radius = [config['border_radius']]
        self.color = color[:3] + [opacity]
        self.coloro = color[:3] + [max(opacity - .1, 0)]
        self.format_date = config['date']
        self.format_time = config['time']
        self.language_language = config['language']
        self.press_delay = config['press_delay']
        self.settings_starred_contacts = config['starred_contacts']

        return Basement()

    def on_resume(self):
        self.trigger_events = not self.trigger_events

        return True


if __name__ == '__main__':
    ProjectSimplifier().run()
