from functools import partial
from os import listdir, makedirs, stat
from os.path import basename, isdir, isfile, join
from threading import Thread
from time import sleep

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.stacklayout import StackLayout

from .configuration import set_value
from .setup import WALLPAPER_CACHE, WALLPAPER_STORAGE, SystemFileChooser

__all__ = ('cut_region', 'wallpaper', 'Gallery', 'Wallpaper')

makedirs(WALLPAPER_STORAGE, exist_ok=True)
makedirs(WALLPAPER_CACHE, exist_ok=True)

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
            pos: self.pos
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
    orientation: 'vertical'
    spacing: dp(15)

    ScrollView:
        GalleryPlatform:
            padding: dp(5), dp(5)
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(5)
            folder: root.folder

    AddWallpapers:
        size_hint: None, None
        size: dp(160), dp(70)
        spacing: dp(5)
        pos_hint: {'center_x': .5}
        Image:
            source: 'assets/images/add.png'
        Label:
            size_hint_x: None
            text: self.parent.text

''')


def cut_region(texture=None, crop=None):
    crop = crop or Window.size
    target_ratio = crop[0] / crop[1]
    target_width = target_ratio * texture.height

    if texture.width < target_width:
        return texture

    target_x = (texture.width - target_width) / 2

    return texture.get_region(x=target_x,
                              y=0,
                              width=target_width,
                              height=texture.height)


def wallpaper(source=None, crop=None, mipmap=None):
    filesize = stat(source).st_size
    filename = f"{filesize};{basename(source)}"
    path = join(WALLPAPER_CACHE, filename)
    mipmap = mipmap or False

    if isfile(path):
        texture = Image(path, mipmap=mipmap).texture
    else:
        texture = cut_region(Image(source, mipmap=mipmap).texture)
        texture.save(path, flipped=False)

    return texture


class Wallpaper(CheckBox):
    allow_no_selection = BooleanProperty(False)
    bwidth = NumericProperty('5dp')
    corner_radius = NumericProperty('5dp')
    filename = StringProperty()
    image_ratio = NumericProperty(1.)
    texture = ObjectProperty(None, allownone=True)
    image_height = NumericProperty()

    def on_filename(self, _, filename):
        self._app = App.get_running_app()
        self.texture = Image(filename).texture
        w, h = self.texture.size
        self.image_ratio = w / float(h)
        self.active = (filename == self._app.wallpaper) or None

    def on_active(self, _, active):
        if active:
            _app = App.get_running_app()
            _app.background = wallpaper(self.filename)
            _app.wallpaper = self.filename
            set_value('settings', 'wallpaper', self.filename)


class AddWallpapers(SystemFileChooser, ButtonBehavior, BoxLayout):
    __events__ = ('on_update', )
    mime_type = StringProperty('image/*')
    multiple = BooleanProperty(True)
    text = StringProperty()

    def on_kv_post(self, _):
        self._app = App.get_running_app()
        self._app.bind(language_language=self.on_update)
        self.dispatch('on_update')

    def on_release(self):
        self.trigger()

    @mainthread
    def on_uris(self, _, uris):
        from androidssystemfilechooser import (uri_image_to_texture,
                                               uri_to_filename)
        p = self.parent.children[-1].children[0]

        for uri in uris:
            path = join(WALLPAPER_STORAGE, f"{uri_to_filename(uri)}.png")

            if not isfile(path):
                texture = uri_image_to_texture(uri)
                texture.save(path, flipped=False)
                p.add_widget(Wallpaper(filename=path))

        self.uris = []

    def on_update(self):
        if self._app.tr is not None:
            self.text = self._app.tr._('Add more')


class Gallery(BoxLayout):
    folder = StringProperty('assets/wallpapers')


class GalleryPlatform(StackLayout):
    folder = StringProperty()

    def on_kv_post(self, _):
        Thread(target=self.scan, daemon=True).start()

    def scan(self):
        included_wallpapers = []
        uploaded_wallpapers = []

        if isdir(self.folder):
            included_wallpapers = [join(self.folder, file)
                                   for file in listdir(self.folder)]

        if isdir(WALLPAPER_STORAGE):
            uploaded_wallpapers = [join(WALLPAPER_STORAGE, file)
                                   for file in listdir(WALLPAPER_STORAGE)]

        for source in included_wallpapers + uploaded_wallpapers:
            Clock.schedule_once(partial(self.on_source, source), 0)
            sleep(.05)

    def on_source(self, source, dt):
        self.add_widget(Wallpaper(filename=source))
