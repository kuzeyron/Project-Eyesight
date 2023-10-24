from os.path import join
from random import uniform

from kivy.animation import Animation
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (BooleanProperty, ColorProperty, NumericProperty,
                             StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import get_hex_from_color

from .configuration import set_value
from .dropdown import DropDownConfig
from .long_press import LongPress

__all__ = ('DeviceSettings', )


Builder.load_file('libs/settings.kv')


class ContentBox(DropDownConfig, BoxLayout):
    pass


class DirectionButton(LongPress, GridLayout):
    color = ColorProperty()
    direction = StringProperty()
    flipped = BooleanProperty(False)
    icon = StringProperty('back')
    long_press_time = NumericProperty(.5)
    override = BooleanProperty(True)
    text = StringProperty('Back')
    font_name = StringProperty('Roboto')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app = App.get_running_app()
        self._app.bind(settings_font=self.on_direction,
                       language_language=self.on_direction)

    def on_direction(self, *largs):
        self.text = self._app.tr._(self.direction.title())

        if self.direction in {'home', 'fonts', 'settings'}:
            self.font_name = self._app.settings_font

    def on_flipped(self, *largs):
        a = self.children.pop(0)
        self.children.append(a)

    def on_short_press(self, *largs):
        self._app.root.transition.direction = 'right'
        self._app.root.current = self.direction


class ColorBox(ButtonBehavior, Widget):
    color = ColorProperty((1, 1, 1, 1))
    bwidth = NumericProperty('10dp')

    def on_release(self, *largs):
        app = App.get_running_app()
        opacity = app.color[-1]
        app.color = self.color[:3] + [opacity]
        set_value('settings', 'bg_color', get_hex_from_color(app.color))
        app.coloro = self.color[:3] + [max(opacity - .1, 0)]


class ColorGenerator(RecycleView):
    amount = NumericProperty(100)

    def on_kv_post(self, *largs):
        app = App.get_running_app()
        self.data = [dict(color=[uniform(0.02, 1.0)
                                 for j in range(3)] + [app.color[-1]])
                     for x in range(self.amount)]


class DeviceSettings(BoxLayout):
    orientation = StringProperty('vertical')


class Privacy(Label):
    opacity = NumericProperty()

    def on_kv_post(self, *largs):
        with open(join('assets', 'privacy', 'privacy.ktxt'),
                  encoding='utf-8') as file:
            self.text = file.read().format(int(dp(23)),
                                           int(dp(18)),
                                           int(dp(14)))
        Animation(opacity=1, t='out_quad', d=.1).start(self)


class DirectionScreen(Screen):
    def add_element(self, element):
        self.children[0].children[0].add_widget(element)

    def on_pre_leave(self, *largs):
        child = self.children[0].children[0]
        child._app = None
        child.clear_widgets()
