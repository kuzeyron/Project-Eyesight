from os.path import join

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, DictProperty,
                             NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex, platform

from libs.android_hide_system_bars import HideBars
from libs.configuration import get_language, get_value, set_value
from libs.language import Lang
from libs.wallpaper import Wallpaper

if platform not in {'android', 'ios'}:
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))

globlang = get_language()
tr = Lang(globlang[1])

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
                short_press_time: app.press_delay * 5
                long_press_time: app.press_delay * 10
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
    color = ColorProperty()
    icon = StringProperty(join('assets', 'images', 'icon.png'))
    lang_changes = DictProperty({'0': globlang,
                                 '1': globlang,
                                 'changed': False})
    press_delay = NumericProperty(1.5)
    starred = BooleanProperty(True)
    title = StringProperty('ProjectEyesight')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = get_value('settings')
        self.background = Wallpaper(source=config['wallpaper'],
                                    crop=None).texture
        self.color = get_color_from_hex(config['bg_color'])
        self.press_delay = config['press_delay']
        self.starred = config['starred_contacts']

    def build(self):
        return Basement()

    def set_language(self, lang=None, auto=None):
        if all([
            isinstance(lang, str),
            isinstance(auto, bool)
        ]):
            auto = int(auto)
            lang = lang or 'en'
            tr.switch_lang(lang)

            set_value('language', "language", tr.lang)
            set_value('language','auto', auto)


if __name__ == '__main__':
    ProjectSimplifier().run()
