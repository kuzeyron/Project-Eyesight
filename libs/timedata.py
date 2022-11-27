from datetime import datetime
from threading import Thread
from time import sleep

from __main__ import tr
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, NumericProperty,
                             StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from libs.android_battery import battery
from libs.long_press import LongPress

Builder.load_string('''
<TimeData>:
    padding: dp(10), dp(10)
    canvas.before:
        Color:
            rgba: app.color[:3] + [.45]
        RoundedRectangle:
            pos: self.pos
            radius: [dp(15), ]
            size: self.size
        Color:
            rgba: 1,1,1,.1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, dp(15)

    TimeLabel:
        size_hint_y: 1.2
        font_size: self.height
        outline_width: dp(5)
        text: root.time

    TimeLabel:
        font_size: self.height // 4
        outline_width: dp(3)
        text: root.info

''')


class TimeLabel(Label):
    font_name = StringProperty('assets/fonts/font.ttf')


class Time(BoxLayout):
    pass


class TimeData(LongPress, BoxLayout):
    background_color = ColorProperty((0, 0, 0, 0))
    battery_charging = BooleanProperty(False)
    battery_percent = NumericProperty(0)
    info = StringProperty()
    orientation = StringProperty('vertical')
    rows = NumericProperty(3)
    show_traces = BooleanProperty(False)
    time = StringProperty('00:00')

    def on_kv_post(self, *largs):
        Clock.schedule_once(self.status, 0)
        Clock.schedule_interval(self.status, 1)
        Thread(target=self.refresh_data, daemon=True).start()

    def refresh_data(self):
        while True:
            self.battery_percent, self.battery_charging = battery()
            sleep(10)

    def status(self, *largs):
        now = datetime.now()
        week_name = tr._(now.strftime("%A").title())
        date = now.strftime("%d.%m.%Y")
        self.time = now.strftime("%H:%M")
        charge_status = tr._('Charging'
                             if self.battery_charging
                             else 'Battery')

        self.info = (f"{date} - {week_name}\n{charge_status}:"
                     f" {self.battery_percent}%")
