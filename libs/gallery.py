from os import listdir
from os.path import join

from kivy.app import App
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.checkbox import CheckBox
from kivy.uix.recycleview import RecycleView

from libs.configuration import set_value
from libs.wallpaper import Wallpaper

__all__ = ['PhotoGallery', 'Picture', ]

Builder.load_string('''
<Picture>:
    size_hint: None, None
    group: None if self.multiselection else True
    canvas:
        Color:
            rgb: 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            radius: (self.corner_radius, )
            size: self.size
        StencilPush
        RoundedRectangle:
            pos: self.pos[0] + dp(5), self.pos[1] + root.bwidth / 2
            radius: [self.corner_radius, ]
            size: self.size[0] - dp(10), self.size[1] - root.bwidth
        StencilUse
        Rectangle:
            pos: self.pos[0], self.pos[1] - (self.height / 3)
            size: self.width, self.height / root.image_ratio
            texture: self.preview_texture if self.preview_texture else None
        StencilUnUse
        RoundedRectangle:
            pos: self.pos[0] + dp(5), self.pos[1] + root.bwidth / 2
            radius: (self.corner_radius, )
            size: self.size[0] - dp(10), self.size[1] - root.bwidth
        StencilPop
        Color:
            rgba: (.25, .15, .25, .7) if self.active else (1, 1, 1, 0)
        RoundedRectangle:
            pos: self.pos[0] + dp(5), self.pos[1] + root.bwidth / 2
            radius: (dp(5), )
            size: self.size[0] - dp(10), self.size[1] - root.bwidth
        Color:
            rgba: 1, 1, 1, int(self.active)
        Line:
            cap: 'square'
            joint: 'miter'
            points: [ \
                (self.center_x - dp(15), self.center_y - dp(12) + root.bwidth), \
                (self.center_x, self.center_y-dp(25) + root.bwidth), \
                (self.center_x + dp(30), self.center_y + dp(5) + root.bwidth) \
            ]
            width: dp(5)
    
<PhotoGallery>:
    viewclass: 'Picture'

    RecycleGridLayout:
        height: self.minimum_height
        default_size: None, dp(120)
        default_size_hint: 1, None
        size_hint_y: None
        cols: 3 
        spacing: dp(5)
        padding: dp(5), dp(5)
''')


class Picture(CheckBox):
    allow_no_selection = BooleanProperty(False)
    bwidth = NumericProperty('10dp')
    corner_radius = NumericProperty('5dp')
    filename = StringProperty()
    image_ratio = NumericProperty(1.)
    keep_ratio = BooleanProperty(True)
    multiselection = BooleanProperty(False)
    preview_texture = ObjectProperty(None)
    image_height = NumericProperty()

    def on_filename(self, *largs):
        self._app = App.get_running_app()
        self.active = self.filename == self._app.wallpaper
        self.preview_texture = Wallpaper(self.filename, mipmap=True).texture
        pt = self.preview_texture
        self.image_ratio = pt.size[0] / float(pt.size[1])
        self.image_height = self.width / self.image_ratio

    def on_active(self, *largs):
        if self.active and self.image_height:
            self._app.background = self.preview_texture
            set_value('settings', 'wallpaper', self.filename)


class PhotoGallery(RecycleView):
    folder = StringProperty('assets/wallpapers')
    
    def on_kv_post(self, *largs):
        self.data = [dict(filename=join(self.folder, source))
                      for source in listdir(self.folder)]
    
    def on_disabled(self, *largs):
        if self.disabled:
            self.data.clear()
        else:
            self.dispatch('on_kv_post')
