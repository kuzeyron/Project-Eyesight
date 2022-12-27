from os.path import join

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, DictProperty,
                             ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex, platform

from libs.android_hide_system_bars import HideBars
from libs.configuration import get_language, get_value
from libs.language import Lang
from libs.wallpaper import Wallpaper

if platform not in {'android', 'ios'}:
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))

language = get_language()
tr = Lang(language[0])

Builder.load_string('''
#:import TimeData libs.timedata.TimeData
#:import Contacts libs.contacts.Contacts
#:import AppLauncher libs.applauncher.AppLauncher
#:import app_run libs.android_applaunch.os_return_value_of_subject
#:import tr __main__.tr
#:import DeviceSettings libs.settings.DeviceSettings

<Basement>:
    # on_kv_post: self.current = 'settings'
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
            padding: sp(5), sp(5)
            spacing: sp(5)
            orientation: 'vertical'

            TimeData:
                short_press_time: 8 
                long_press_time: 8
                override: True
                on_long_press:
                    root.current = 'settings'
                    root.transition.direction = 'up'

            Contacts:
                starred: app.starred

            AppLauncher:
                package: app_run('contacts')
                size_hint_y: .5
                text: tr._('Phonebook')

            AppLauncher:
                package: app_run('messaging')
                size_hint_y: .4
                text: tr._('SMS')

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
    color = ColorProperty((1, 1, 1, 1))
    coloro = ColorProperty((1, 1, 1, 1))
    border_radius = ListProperty([10, ])
    icon = StringProperty(join('assets', 'images', 'icon.png'))
    press_delay = NumericProperty(1.5)
    starred = BooleanProperty(True)
    title = StringProperty('ProjectEyesight')
    current_selection = DictProperty({language[1]: [language[0]]})

    def build(self):
        config = {**get_value('settings'), **get_value('format')}
        self.background = Wallpaper(source=config['wallpaper'],
                                    crop=None).texture
        color = get_color_from_hex(config['bg_color'])
        opacity = config['color_opacity']
        self.color = color[:3] + [opacity]
        self.coloro = color[:3] + [max(opacity - .2, 0)]
        self.press_delay = config['press_delay']
        self.current_selection.update({
            'settings.starred_contacts': [config['starred_contacts']],
            'format.time': [config['time']],
            'format.date': [config['date']]
        })
        self.border_radius = [config['border_radius']]

        return Basement()


if __name__ == '__main__':
    ProjectSimplifier().run()
