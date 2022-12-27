from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ColorProperty, NumericProperty
from kivy.uix.slider import Slider

from libs.checkboxitem import BaseLayout
from libs.configuration import set_value

__all__ = ('ItemSlider', 'PressDelayItem', 'ColorOpacity', 'BorderRadius', 'PressDelayCrawler')

Builder.load_string('''
#:import CheckBoxLabel libs.checkboxitem.CheckBoxLabel

<PressDelayCrawler>:
    padding: dp(5), dp(5)
    rows: 2
    canvas.before:
        Color:
            rgba: app.color
        RoundedRectangle:
            pos: self.pos
            radius: app.border_radius
            size: self.size

    CheckBoxLabel:
        text: f"  {tr._('Seconds')}: {slider.value}"

    PressDelayItem:
        id: slider

''')


class ItemSlider(Slider):
    max = NumericProperty(3)
    min = NumericProperty(.1)
    opacity = NumericProperty(.8)
    step = NumericProperty(.1)
    value = NumericProperty(1.5)
    value_track = BooleanProperty(True)
    value_track_color = ColorProperty((0, 0, .8, 1))


class PressDelayItem(ItemSlider):
    min = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.time_set)

    def on_kv_post(self, *largs):
        instance = App.get_running_app()
        self.value = instance.press_delay

    def time_set(self, *largs):
        instance = App.get_running_app()
        value = float(format(self.value, ".2f"))
        set_value('settings', 'press_delay', value)
        self.value = value
        instance.press_delay = value
        self.value_track_color = (0, .8, 0) if value == 1.5 else (0, 0, .8)


class ColorOpacity(ItemSlider):
    max = NumericProperty(1)
    min = NumericProperty(0)
    step = NumericProperty(.01)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.time_set)

    def on_kv_post(self, *largs):
        instance = App.get_running_app()
        self.value = instance.color[-1]

    def time_set(self, *largs):
        instance = App.get_running_app()
        self.value_track_color = (0, .8, 0) if .8 > self.value > .6 else (0, 0, .8)
        instance.color[-1] = self.value
        instance.coloro[-1] = max(self.value - .2, 0)
    
    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        set_value('settings', 'color_opacity', self.value)


class BorderRadius(ItemSlider):
    max = NumericProperty(25)
    min = NumericProperty(5)
    step = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.time_set)

    def on_kv_post(self, *largs):
        instance = App.get_running_app()
        self.value = instance.border_radius[0]

    def time_set(self, *largs):
        instance = App.get_running_app()
        instance.border_radius = [dp(self.value)]
    
    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        set_value('settings', 'border_radius', dp(self.value))


class PressDelayCrawler(BaseLayout):
    pass

