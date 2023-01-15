from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (AliasProperty, BooleanProperty, ColorProperty,
                             DictProperty, ListProperty, NumericProperty,
                             StringProperty, ObjectProperty)
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import ButtonBehavior
from libs.configuration import get_value, set_value

__all__ = ('SettingsCrawler', 'LabeledCheckBox')

Builder.load_string('''
<LabeledCheckBox>:
    active: self.rv_key == getattr(app, self.dict_name, False)
    on_active: self.select_row(self.active)
    font_size: self.button_size
    text: app.tr._(self.cached_text)
    _checkbox_state_image:
        self.background_checkbox_down \
        if self.active else self.background_checkbox_normal
    _checkbox_disabled_image:
        self.background_checkbox_disabled_down \
        if self.active else self.background_checkbox_disabled_normal
    _radio_state_image:
        self.background_radio_down \
        if self.active else self.background_radio_normal
    _radio_disabled_image:
        self.background_radio_disabled_down \
        if self.active else self.background_radio_disabled_normal
    _checkbox_image:
        self._checkbox_disabled_image \
        if self.disabled else self._checkbox_state_image
    _radio_image:
        self._radio_disabled_image \
        if self.disabled else self._radio_state_image
    canvas:
        Clear:  # Clearing out label-canvas
        Color:
            rgba: 0, 0, 0, app.color[-1]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10), ]
        Color:
            rgba: self.color[:3] + [1]
        Rectangle:
            pos: int(self.x + self.button_size / 2), self.center_y - self.button_size
            size: self.button_size * 2, self.button_size * 2
            source: self._radio_image if self.group else self._checkbox_image
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos:
                int(self.x + (self.button_size * 2.5)), \
                int(self.center_y - self.texture_size[1] / 2.)

<SettingsCrawler>:
    viewclass: 'LabeledCheckBox'
    effect_cls: 'ScrollEffect'
    
    RecycleGridLayout:
        default_size: 100, dp(80)
        default_size_hint: 1, None 
        size_hint_y: None
        height: self.minimum_height
        cols: root.cols
        rows: root.rows
        spacing: dp(5)

''')


class CheckBoxLabel(ButtonBehavior, Label):
    font_size = NumericProperty("22dp")


class LabeledCheckBox(ToggleButtonBehavior, Label):
    allow_no_selection = BooleanProperty(False)
    button_size = NumericProperty("20dp")
    rv_key = ObjectProperty()
    text = StringProperty()

    def _get_active(self):
        return self.state == 'down'

    def _set_active(self, value):
        self.state = 'down' if value else 'normal'

    active = AliasProperty(
        _get_active, _set_active, bind=('state', ), cache=True)
    background_checkbox_normal = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_off')
    background_checkbox_down = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_on')
    background_checkbox_disabled_normal = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_disabled_off')
    background_checkbox_disabled_down = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_disabled_on')
    background_radio_normal = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_radio_off')
    background_radio_down = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_radio_on')
    background_radio_disabled_normal = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_radio_disabled_off')
    background_radio_disabled_down = StringProperty(
        'atlas://data/images/defaulttheme/checkbox_radio_disabled_on')
    color = ColorProperty([1, 1, 1, 1])
    dict_name = StringProperty()
    settings = ListProperty()
    cached_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fbind('state', self._on_state)
        self._app = App.get_running_app()

    def _on_state(self, instance, value):
        if self.group and self.state == 'down':
            self._release_group(self)

    def on_group(self, *largs):
        super().on_group(*largs)
        if self.active:
            self._release_group(self)

    def on_settings(self, *largs):
        self.group = self.settings[1]
        self.dict_name = name = '_'.join(self.settings)
        data = get_value(self.settings[0])
        setattr(self._app, name, data[self.settings[1]])
    
    def select_row(self, active):
        if active and self.rv_key is not getattr(self._app, self.dict_name):
            setattr(self._app, self.dict_name, self.rv_key)
            if self.rv_key is getattr(self._app, self.dict_name):
                set_value(*self.settings, self.rv_key)
                self._app.tr.switch_lang(self.rv_key)

class SettingsCrawler(TouchRippleBehavior, RecycleView):
    ripple_scale = NumericProperty(.25)
    show_traces = BooleanProperty(True)
    settings = ListProperty()
    labels = DictProperty()
    cols = NumericProperty(None, allownone=True)
    rows = NumericProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(labels=self.setup)

    def setup(self, *largs):
        self.data = [dict(rv_key=k, cached_text=v, settings=self.settings)
                     for k, v in self.labels.items()]


class BaseLayout(TouchRippleBehavior, GridLayout):
    ripple_scale = NumericProperty(.25)
    show_traces = BooleanProperty(True)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point and self.show_traces:
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False


if __name__ == '__main__':
    from kivy.base import runTouchApp
    x = SettingsCrawler()
    x.current_selection = []
    x.settings = ('language', 'language')
    x.labels = dict(sv='Svenska', en='English', fi='Suomi', auto='Auto')
    runTouchApp(x)
