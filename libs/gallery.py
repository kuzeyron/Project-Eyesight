from functools import partial
from os import listdir
from os.path import join
from threading import Thread
from time import sleep

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout

from .configuration import set_value
from .wallpaper import wallpaper

__all__ = ('Gallery', 'Wallpaper')

Builder.load_string('''
<Wallpaper>:
    size_hint: None, None
    size: dp(90), dp(130)
    group: True
    canvas:
        Color:
            rgb: 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            radius: (self.corner_radius, )
            size: self.size
        StencilPush
        RoundedRectangle:
            pos: self.pos[0] + dp(2.5), self.pos[1] + root.bwidth / 2
            radius: [self.corner_radius, ]
            size: self.size[0] - dp(5), self.size[1] - root.bwidth
        StencilUse
        Rectangle:
            pos: self.x, self.y - (self.height / 3)
            size: self.width, self.height / self.image_ratio
            texture: self.texture if self.texture else None
        StencilUnUse
        RoundedRectangle:
            pos: self.pos[0] + dp(2.5), self.pos[1] + root.bwidth / 2
            radius: (self.corner_radius, )
            size: self.size[0] - dp(5), self.size[1] - root.bwidth
        StencilPop
        Color:
            rgba: (.25, .15, .25, .7) if self.active else (1, 1, 1, 0)
        RoundedRectangle:
            pos: self.pos[0] + dp(2.5), self.pos[1] + root.bwidth / 2
            radius: (dp(2.5), )
            size: self.size[0] - dp(5), self.size[1] - root.bwidth
        Color:
            rgba: 1, 1, 1, int(self.active)
        SmoothLine:
            cap: 'square'
            joint: 'miter'
            points: [ \
                (self.center_x - dp(15), self.center_y - dp(8) + root.bwidth), \
                (self.center_x, self.center_y-dp(20) + root.bwidth), \
                (self.center_x + dp(20), self.center_y + dp(5) + root.bwidth) \
            ]
            width: dp(5)

<Gallery>:
    GalleryPlatform:
        padding: dp(5), dp(5)
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(5)
        folder: root.folder

''')


class Wallpaper(CheckBox):
    allow_no_selection = BooleanProperty(False)
    bwidth = NumericProperty('5dp')
    corner_radius = NumericProperty('5dp')
    filename = StringProperty()
    image_ratio = NumericProperty(1.)
    texture = ObjectProperty(None, allownone=True)
    image_height = NumericProperty()

    def on_filename(self, *largs):
        self._app = App.get_running_app()
        self.texture = wallpaper(self.filename)
        w, h = self.texture.size
        self.image_ratio = w / float(h)
        self.active = (self.filename == self._app.wallpaper) or None

    def on_active(self, *largs):
        if self.active:
            self._app.background = self.texture
            self._app.wallpaper = self.filename
            set_value('settings', 'wallpaper', self.filename)


class Gallery(ScrollView):
    folder = StringProperty('assets/wallpapers')


class GalleryPlatform(StackLayout):
    folder = StringProperty()

    def on_kv_post(self, *largs):
        Thread(target=self.scan, daemon=True).start()

    def scan(self, *largs):
        for source in listdir(self.folder):
            Clock.schedule_once(partial(self.on_source, source), 0)
            sleep(.05)

    def on_source(self, source, dt):
        self.add_widget(Wallpaper(filename=join(self.folder, source)))
