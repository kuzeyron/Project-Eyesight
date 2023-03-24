from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import (BooleanProperty, ColorProperty, DictProperty,
                             ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex, platform

from libs.android_hide_system_bars import HideBars
from libs.configuration import configuration
from libs.language import Lang
from libs.wallpaper import Wallpaper

if platform not in {'android', 'ios'}:
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = dp(400), dp(650)
    Logger.debug("Application is not Android.")

Builder.load_string('''
#:import TimeData libs.timedata.TimeData
#:import Contacts libs.contacts.Contacts
#:import AppLauncher libs.applauncher.AppLauncher
#:import DeviceSettings libs.settings.DeviceSettings
#:import Privacy libs.settings.Privacy

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
            padding: dp(5), app.cutout_height + dp(5), dp(5), dp(5)
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

    Privacy:
        name: 'privacy'
''')


class Basement(ScreenManager):
    pass


class ProjectSimplifier(App, HideBars):
    __events__ = ('on_configuration', )
    background = ObjectProperty(None, allownone=True)
    border_radius = ListProperty()
    appconfig = DictProperty({})
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dispatch('on_configuration')

    def on_configuration(self, *largs):
        self.appconfig = conf = configuration(['settings', 'format', 'language'])
        conf['tr'] = Lang(conf['language'])
        conf['background'] = Wallpaper(source=conf['wallpaper'],
                                       crop=None).texture
        color = get_color_from_hex(conf['bg_color'])
        opacity = conf['color_opacity']
        conf['border_radius'] = [conf['border_radius']]
        conf['color'] = color[:3] + [opacity]
        conf['coloro'] = color[:3] + [max(opacity - .1, 0)]
        conf['format_date'] = conf['date']
        conf['format_time'] = conf['time']
        conf['language_language'] = conf['language']
        conf['press_delay'] = conf['press_delay']
        conf['settings_starred_contacts'] = conf['starred_contacts']
        
        for key, value in conf.items():
            setattr(self, key, value)

    def build(self):
        return Basement()

    def on_resume(self):
        self.trigger_events = not self.trigger_events
        Logger.debug("Returning to the application.")

        return True


if __name__ == '__main__':
    ProjectSimplifier().run()
