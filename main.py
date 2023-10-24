from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import (BooleanProperty, ColorProperty, DictProperty,
                             ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex, platform

from libs.android_call import CallService
from libs.android_hide_system_bars import HideBars
from libs.configuration import configuration
from libs.language import Lang
from libs.wallpaper import wallpaper

if platform != 'android':
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = dp(400), dp(650)
    Logger.debug("OS is not Android.")

Builder.load_string('''
#:import AppLauncher libs.applauncher.AppLauncher
#:import Contacts libs.contacts.Contacts
#:import DeviceSettings libs.settings.DeviceSettings
#:import DirectionScreen libs.settings.DirectionScreen
#:import FontBahn libs.fonts.FontBahn
#:import Gallery libs.gallery.Gallery
#:import Privacy libs.settings.Privacy
#:import TimeData libs.timedata.TimeData
#:import AppContainer libs.launcher.AppContainer

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

    DirectionScreen:
        name: 'wallpapers'
        on_enter: self.add_element(Gallery())

    DirectionScreen:
        name: 'privacy'
        on_enter: self.add_element(Privacy())

    DirectionScreen:
        name: 'fonts'
        on_enter: self.add_element(FontBahn())

    DirectionScreen:
        name: 'all apps'
        on_enter: self.add_element(AppContainer())
''')


class Basement(ScreenManager):
    pass


class ProjectSimplifier(App, HideBars):
    appconfig = DictProperty()
    background = ObjectProperty(None, allownone=True)
    border_radius = ListProperty()
    color = ColorProperty()
    coloro = ColorProperty()
    contact_caller = ObjectProperty(None, allownone=True)
    current_selection = DictProperty()
    settings_font = StringProperty()
    settings_font_border = NumericProperty()
    format_date = StringProperty()
    format_time = StringProperty()
    icon = 'assets/images/icon.png'
    language_language = StringProperty()
    press_delay = NumericProperty()
    settings_starred_contacts = StringProperty()
    title = StringProperty('Project Eyesight')
    tr = ObjectProperty(None, allownone=True)
    _change_of_events = BooleanProperty(False)

    def build(self):
        self.contact_caller = CallService()
        self.appconfig = conf = configuration(['settings',
                                               'format',
                                               'language'])
        conf['tr'] = Lang(conf['language_language'])
        conf['background'] = wallpaper(source=conf['wallpaper'])
        color = get_color_from_hex(conf['bg_color'])
        opacity = conf['color_opacity']
        conf['border_radius'] = (conf['border_radius'], )
        conf['color'] = color[:3] + [opacity]
        conf['coloro'] = color[:3] + [max(opacity - .1, 0)]

        for key, value in conf.items():
            setattr(self, key, value)

        self.bind(language_language=self.switch_language,
                  settings_starred_contacts=self.trigger_events)

        return Basement()

    def on_resume(self):
        self.trigger_events()
        Logger.debug("Returning to the application.")

        return True

    def switch_language(self, *largs):
        self.tr.switch_lang(self.language_language)

    def trigger_events(self, *largs):
        Logger.debug("Triggers the events to happen.")
        self._change_of_events = not self._change_of_events


if __name__ == '__main__':
    ProjectSimplifier().run()
