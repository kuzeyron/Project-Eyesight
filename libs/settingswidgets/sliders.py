from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ColorProperty, NumericProperty
from kivy.uix.slider import Slider

from ..checkboxitem import BaseLayout
from ..configuration import set_value

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
        text: f"  {app.tr._('Seconds')}: {slider.value}"

    PressDelayItem:
        id: slider

''')


class ItemSlider(Slider):
    max = NumericProperty(3)
    min = NumericProperty(.1)
    opacity = NumericProperty(.8)
    value = NumericProperty(1.5)
    step = NumericProperty(.01)
    value_track = BooleanProperty(True)
    value_track_color = ColorProperty((0, 0, .8, 1))
    default = NumericProperty(2)
    btw_min = NumericProperty(0)
    btw_max = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.time_set)
        self._app = App.get_running_app()
        self.btw_min = max(self.default - .1, self.min)
        self.btw_max = min(self.default + .1, self.max)

    def time_set(self, *largs):
        value = float(format(self.value, ".2f"))
        self.value = value
        _min = self.btw_min
        _max = self.btw_max

        if all([_max > self.value > _min,
                _max > self.default > _min
        ]):
            self.value_track_color = (0, .8, 0)
        else:
            self.value_track_color = (0, 0, .8)


class PressDelayItem(ItemSlider):
    min = NumericProperty(0)
    default = NumericProperty(1)
    step = NumericProperty(.5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = self._app.press_delay

    def time_set(self, *largs):
        super().time_set(*largs)
        self._app.press_delay = self.value

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        set_value('settings', 'press_delay', self.value)


class ColorOpacity(ItemSlider):
    max = NumericProperty(1)
    min = NumericProperty(0)
    default = NumericProperty(.7)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = self._app.color[-1]

    def time_set(self, *largs):
        super().time_set(*largs)
        self._app.color[-1] = self.value
        self._app.coloro[-1] = max(self.value - .2, 0)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        set_value('settings', 'color_opacity', self.value)


class BorderRadius(ItemSlider):
    max = NumericProperty(25)
    min = NumericProperty(2)
    default = NumericProperty(15)
    step = NumericProperty(.1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = self._app.border_radius[0]

    def time_set(self, *largs):
        super().time_set(*largs)
        self._app.border_radius = [dp(self.value)]

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        set_value('settings', 'border_radius', dp(self.value))


class BorderWidth(ItemSlider):
    max = NumericProperty(15)
    min = NumericProperty(0)
    default = NumericProperty(5)
    step = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = self._app.settings_font_border

    def time_set(self, *largs):
        super().time_set(*largs)
        self._app.settings_font_border = self.value

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        set_value('settings', 'settings_font_border', self.value)


class PressDelayCrawler(BaseLayout):
    pass

