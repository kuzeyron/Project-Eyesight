from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, NumericProperty,
                             StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from .battery import battery
from .long_press import LongPress

__all__ = ('TimeData', )

Builder.load_string('''
<TimeLabel>:
    font_name: app.settings_font

<TimeData>:
    padding: dp(10), dp(10)
    canvas.before:
        Color:
            rgba: app.color
        RoundedRectangle:
            pos: self.pos
            radius: app.border_radius
            size: self.size
        Color:
            rgba: 1, 1, 1, .1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, app.border_radius[0]

    TimeLabel:
        size_hint_y: 1.2
        font_size: self.height if len(self.text) < 6 else self.height / 1.6
        outline_width: app.settings_font_border
        text: root.time
        markup: True

    TimeLabel:
        font_size: self.height // 4
        outline_width: app.settings_font_border
        text: root.info

''')


class TimeLabel(Label):
    pass


class Time(BoxLayout):
    pass


def is24(time, fm, fmt):
    if all([fm not in {'auto', 'h24'},
            time[:2].isdigit(),
            fmt == 'time']):
        return time[int(int(time[:2]) < 10):]
    return time


def timeformat(time, timed, fmt):
    fm = getattr(App.get_running_app(), f"format_{fmt}")
    return is24(time.strftime(timed[fm]), fm, fmt)


class TimeData(LongPress, BoxLayout):
    _date = StringProperty('auto')
    _time = StringProperty('auto')
    background_color = ColorProperty((0, 0, 0, 0))
    battery_charging = BooleanProperty(False)
    battery_percent = NumericProperty(0)
    info = StringProperty()
    orientation = StringProperty('vertical')
    rows = NumericProperty(3)
    show_traces = BooleanProperty(False)
    time = StringProperty('00:00')

    def on_kv_post(self, *largs):
        self.date_format = dict(obliquestroke='%m/%d/%Y',
                                auto='%d.%m.%Y',
                                hyphen='%d-%m-%Y')
        self.time_format = dict(auto='%H:%M',
                                h24='%H.%M',
                                h12='%I.%M',
                                am12='%I:%M[color=#ddffe7]%p[/color]')
        Clock.schedule_interval(self.on_activity, 10)
        self.dispatch('on_activity')

    def on_activity(self, *largs):
        battery_percent, battery_charging = battery()
        now = datetime.now()
        week_name = self._app.tr._(now.strftime("%A").title())
        date = timeformat(now, self.date_format, 'date')
        self.time = timeformat(now, self.time_format, 'time')
        charge_status = self._app.tr._('Charging'
                                       if battery_charging
                                       else 'Battery')

        self.info = (f"{date} - {week_name}\n{charge_status}:"
                     f" {battery_percent}%")
