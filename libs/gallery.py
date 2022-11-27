from os import listdir
from os.path import isfile, join

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.checkbox import CheckBox
from kivy.uix.stacklayout import StackLayout

from libs.configuration import get_value, set_value
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
            pos: self.pos
            size: self.size
            texture: self.preview_texture.texture \
                if self.preview_texture else None
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
            rgba: (1, 1, 1, 1 if self.active else 0)
        Line:
            cap: 'square'
            joint: 'miter'
            points: [ \
                (self.center_x-dp(15), self.center_y-dp(12)+root.bwidth), \
                (self.center_x, self.center_y-dp(25)+root.bwidth), \
                (self.center_x+dp(30), self.center_y+dp(5)+root.bwidth) \
            ]
            width: dp(5)
''')


class Picture(CheckBox):
    allow_no_selection = BooleanProperty(False)
    bwidth = NumericProperty('10dp')
    corner_radius = NumericProperty()
    filename = StringProperty()
    hover = BooleanProperty(True)
    image_ratio = NumericProperty(1.)
    keep_ratio = BooleanProperty(True)
    multiselection = BooleanProperty(None)
    preview_texture = ObjectProperty(None)

    def on_kv_post(self, *largs):
        config = get_value('settings')
        self.preview_texture = Image(self.filename,
                                     mipmap=True)
        if config['wallpaper'] == self.filename:
            self.active = True
        self.bind(active=self.toggle_click,
                  size=self.layout_changes)
        Clock.schedule_once(self.layout_changes, 0)

    def layout_changes(self, *largs):
        pt = self.preview_texture
        self.image_ratio = pt.width / float(pt.height)
        self.height = self.width / self.image_ratio

    def toggle_click(self, *largs):
        app = App.get_running_app()
        self.preview_texture = Wallpaper(source=self.filename,
                                         crop=app.root.size)
        pt = self.preview_texture.texture
        app.background = pt
        set_value('settings', 'wallpaper', self.filename)


class PhotoGallery(StackLayout):
    allowed_exts = ListProperty(['.png', '.jpg', '.jpeg', '.webp'])
    border_width = NumericProperty('10sp')
    collection = ListProperty()
    corner_radius = NumericProperty()
    folder = StringProperty('assets/wallpapers')
    multiselection = BooleanProperty(None, allownone=True)
    orientation = StringProperty('lr-tb')
    rows = NumericProperty(3)
    is_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(is_open=self.open_status,
                  size=self.recompute_layout)

    def open_status(self, *largs):
        if self.is_open:
            Clock.schedule_once(self._collect, 0)
        else:
            self.collection.clear()
            self.clear_widgets()

    def width_calculation(self):
        """ Sums together the spacing/padding and match
            that with amount of rows """
        sr = sum(self.spacing[::2] + self.padding[::2]) * self.rows
        return (self.width - sr) / self.rows

    def _collect(self, *largs):
        """ Main core """
        width = self.width_calculation()

        for filename in listdir(self.folder):
            path = join(self.folder, filename)

            if isfile(path):
                self.add_widget(Picture(filename=path,
                                        width=width,
                                        corner_radius=self.corner_radius,
                                        bwidth=self.border_width,
                                        multiselection=self.multiselection))

    def recompute_layout(self, *largs):
        """ Giving the width for the children """
        width = self.width_calculation()
        for child in self.children:
            child.width = width
