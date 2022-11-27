from os import makedirs, stat
from os.path import basename, isfile, join

from kivy.app import App
from kivy.core.image import Image
from kivy.event import EventDispatcher
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)

__all__ = ['Wallpaper', ]


class Wallpaper(EventDispatcher):
    crop = ListProperty((50, 50), allownone=True)
    filename = StringProperty()
    mipmap = BooleanProperty(True)
    size = ListProperty((100, 100))
    source = StringProperty()
    store_name = NumericProperty()
    texture = ObjectProperty(None, allownone=True)

    def __init__(self, source=None, crop=None, texture=None):
        self.filesize = stat(source).st_size
        self.filename = f"{self.filesize};{basename(source)}"
        self._cache_folder = join('.cache', 'wallpapers')
        makedirs(self._cache_folder, exist_ok=True)
        self.crop = crop

        if texture:
            self.bind(texture=self.texture_update)
            self.texture = texture
        elif isfile(self.filename):
            _texture = Image(self.filename)
            self.size = _texture.size
            self.texture = _texture.texture
        elif not crop:
            self.texture = Image(source).texture
            self.save()
        else:
            self.bind(source=self.texture_crop,
                      crop=self.texture_crop)

        self.source = source

    def _crop(self, textr):
        body = (textr.width - self.crop[0]) / 2
        x = (textr.width - body) / 2

        try:
            if all([textr.height >= 200,
                    textr.width >= 200,
                    body >= 200]):
                texture = textr.get_region(height=textr.height,
                                           width=body, x=x, y=0)
            else:
                texture = textr

        except Exception:
            # We failed to crop the image
            texture = textr

        self.texture = texture
        self.size = texture.size

    def texture_crop(self, *largs):
        self._crop(Image(self.source).texture)
        self.save()

    def texture_update(self, *largs):
        self._crop(self.texture)
        self.save()

    def save(self, *largs):
        cache_folder = join(self._cache_folder, self.filename)
        self.texture.save(cache_folder, flipped=False)


if __name__ == '__main__':
    from os import listdir
    from textwrap import dedent

    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.widget import Widget

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
        Widget:
            size_hint: None, None
            size: 300, 300
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    source: root.source
                    size: self.size
                    pos: self.pos
        MyWid:
            size_hint: None, None
            size: 150, 300
            source: root.source
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    texture: self.preview_texture
                    size: self.size
                    pos: self.pos
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

    class MyWid(Widget):
        preview_texture = ObjectProperty()
        source = StringProperty()
        image_ratio = NumericProperty(1.)
        source = StringProperty()
        texture_size = ListProperty((0, 0))

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.bind(source=self.load_texture)

        def load_texture(self, *largs):
            wp = Wallpaper(
                texture=None,
                source=self.source,
                crop=self.size
            )
            self.preview_texture = wp.texture
            self.texture_size = wp.size
            self.image_ratio = wp.size[0] / float(wp.size[1])

    class VisionGalleria(App):
        def build(self):
            return RV()

    VisionGalleria().run()
