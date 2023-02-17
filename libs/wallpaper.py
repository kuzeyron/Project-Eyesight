from os import makedirs, stat
from os.path import basename, isfile, join

from kivy.app import App
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)

__all__ = ('Wallpaper', )


class Wallpaper(EventDispatcher):
    __events__ = ('on_execute', 'on_textures', 'on_texture_crop')
    crop = ListProperty(None, allownone=True)
    filename = StringProperty()
    mipmap = BooleanProperty(True)
    size = ListProperty((100, 100))
    source = StringProperty()
    store_name = NumericProperty()
    texture = ObjectProperty(None, allownone=True)

    def __init__(self, source=None, crop=None, texture=None, **kwargs):
        super().__init__(**kwargs)
        self.crop = crop
        self.source = source
        self.texture = texture
        self.dispatch('on_execute')

    def on_execute(self, *largs):
        filesize = stat(self.source).st_size
        self.filename = f"{filesize};{basename(self.source)}"
        self._cache_folder = join('.cache', 'wallpapers')
        makedirs(self._cache_folder, exist_ok=True)
        self.path = join(self._cache_folder, self.filename)

        if self.texture:
            self.dispatch('on_textures')
        elif self.crop is None:
            self.texture = Image(self.source).texture
            self.dispatch('on_textures')
        elif isfile(self.path):
            self.texture = Image(self.path).texture
            self.size = self.texture.size
        else:
            self.bind(source=self.on_texture_crop,
                      crop=self.on_texture_crop)
            self.dispatch('on_texture_crop')


    def _crop(self, texture):
        """ Cropping mechanism thanks to Cheaterman """
        crop = self.crop or Window.size

        Logger.debug('Wallpaper: Cropping {texture.size=%s} to {crop=%s}', texture.size, crop)

        target_ratio = crop[0] / crop[1]
        target_width = target_ratio * texture.height

        if texture.width < target_width:
            return texture

        target_x = (texture.width - target_width) / 2

        return texture.get_region(x=target_x,
                                  y=0,
                                  width=target_width,
                                  height=texture.height)

    def on_texture_crop(self, *largs):
        self.texture = self._crop(Image(self.source).texture)
        self.save()

    def on_textures(self, *largs):
        self.texture = self._crop(self.texture)
        self.save()

    def save(self, *largs):
        self.texture.save(self.path, flipped=False)


if __name__ == '__main__':
    from os import listdir
    from textwrap import dedent

    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.image import Image as ImageWidget

    Builder.load_string(dedent('''
    <RV>:
        viewclass: 'Box'
        do_scroll_x: False
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint: None, None
            height: self.minimum_height
            orientation: 'vertical'

    <Box>:
        pos_hint: {'center_x': .5}
        size_hint: None, None
        height: self.minimum_height
        spacing: 10
        Image
            source: root.source
            size_hint: None, None
            size: 300, 300

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                Color:
                    rgba: 1, 0, 0, 1
                Line:
                    rectangle: self.pos + self.size

        MyWid:
            source: root.source
            allow_stretch: True
            size_hint: None, None
            size: 150, 300

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                Color:
                    rgba: 0, 1, 0, 1
                Line:
                    rectangle: self.pos + self.size
    '''))

    class RV(RecycleView):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            path = '/home/kuzeyron/Pictures/Wallpapers'
            self.data = [
                {'source': f"{path}/{x}"}
                for i, x in enumerate(listdir(path))
                if i % 5 == 0
            ]

    class Box(BoxLayout):
        source = StringProperty()

    class MyWid(ImageWidget):
        def set_texture_from_resource(self, resource):
            if not resource:
                self._clear_core_image()
                return

            wp = Wallpaper(
                texture=None,
                source=self.source,
                crop=self.size
            )
            self.bind(size=wp.setter('crop'))
            self.texture = wp.texture
            wp.bind(texture=self.setter('texture'))

    class VisionGalleria(App):
        def build(self):
            return RV()

    VisionGalleria().run()

