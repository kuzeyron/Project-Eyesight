from functools import partial
from os import listdir
from os.path import basename, join
from shutil import move
from threading import Thread
from time import sleep

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform

from .configuration import set_value
from .wallpaper import wallpaper

if platform == 'android':
    from android.permissions import Permission, request_permissions
    from androidstorage4kivy import Chooser, SharedStorage
    from android import api_version

    def can_copy_images(permissions, status):
        perm = {p.split('.')[-1]: status[xy]
                for xy, p in enumerate(permissions)}

        if perm.get('READ_EXTERNAL_STORAGE', False):
            isset = True

            if api_version > 29:
                isset = perm.get('READ_MEDIA_IMAGES', False)

            if isset:
                _app = App.get_running_app()
                _call = _app.root.get_screen('wallpapers').children[0]
                _child = _call.children[0].children[0].children[0]
                _child.chooser.choose_content("image/*")


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


class AddWallpapers(ButtonBehavior, BoxLayout):
    __events__ = ('on_update', )
    chooser = ObjectProperty(None, allownone=True)
    text = StringProperty()

    def on_kv_post(self, *largs):
        self._app = App.get_running_app()
        self._app.bind(language_language=self.on_update)
        self.dispatch('on_update')

        if platform == 'android':
            self.chooser = Chooser(self.chooser_callback)

    @mainthread
    def chooser_callback(self, uri_list):
        try:
            ss = SharedStorage()
            for uri in uri_list:
                if path := ss.copy_from_shared(uri):
                    newname = join('assets', 'wallpapers', basename(path))
                    move(path, newname)
                    Logger.debug('Successfully copied %s to %s',
                                 basename(path), newname)
                    p = self.parent.children[-1].children[0]
                    p.add_widget(Wallpaper(filename=newname, active=True))
        except Exception as e:
            Logger.warning('SharedStorageExample.chooser_callback(): %s', e)

    def on_release(self, *largs):
        if self.chooser is not None:
            request_permissions([Permission.READ_EXTERNAL_STORAGE,
                                 Permission.READ_MEDIA_IMAGES],
                                can_copy_images)

    def on_update(self, *largs):
        if self._app.tr is not None:
            self.text = self._app.tr._('Add more')


class Gallery(BoxLayout):
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
