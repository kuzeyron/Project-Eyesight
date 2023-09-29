from os import listdir
from os.path import join
from threading import Thread

from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.checkbox import CheckBox
from kivy.uix.recycleview import RecycleView

from .configuration import set_value
from .wallpaper import wallpaper

__all__ = ('Gallery', 'Wallpaper')

Builder.load_string('''
<Wallpaper>:
    size_hint: None, None
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
    viewclass: 'Wallpaper'

    RecycleGridLayout:
        cols: 3
        default_size: None, dp(140)
        default_size_hint: 1, None
        height: self.minimum_height
        padding: dp(5), dp(5)
        size_hint_y: None
        spacing: dp(5)

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
        Thread(target=self.load_image).start()

    @mainthread
    def load_image(self):
        self.texture = wallpaper(self.filename)
        w, h = self.texture.size
        self.image_ratio = w / float(h)
        self.active = (self.filename == self._app.wallpaper) or None

    def on_active(self, *largs):
        if self.active:
            self._app.background = self.texture
            set_value('settings', 'wallpaper', self.filename)


class Gallery(RecycleView):
    folder = StringProperty('./assets/wallpapers')
    opacity = NumericProperty(0)

    def on_kv_post(self, *largs):
        Thread(target=self.setup, daemon=True).start()

    @mainthread
    def setup(self, *largs):
        self.data = [{'filename': join(self.folder, source)}
                     for source in listdir(self.folder)]
