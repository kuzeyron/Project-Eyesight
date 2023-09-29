from os import listdir
from os.path import join

# from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, DictProperty, StringProperty
from kivy.uix.scrollview import ScrollView

from .checkboxitem import SettingsCrawler

__all__ = ('FontBahn', 'Fonts')

Builder.load_string('''
#:import BorderWidth libs.settingswidgets.BorderWidth

<FontBahn>:
    bar_width: dp(5)
    do_scroll_x: False
    effect_cls: 'ScrollEffect'

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(15)

        Fonts:
            cols: 2
            settings: ('settings', 'font')

        BoxLayout:
            padding: dp(15), dp(15)
            size_hint_y: .2
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba: 1, 1, 1, .1
                RoundedRectangle:
                    pos: self.pos
                    radius: app.border_radius
                    size: self.size

            Label:
                color: 1, 1, 1, .6
                font_name: app.settings_font
                font_size: dp(26)
                outline_width: app.settings_font_border
                size: self.texture_size
                size_hint: None, .6
                text: app.tr._("Border width for text's")

            BorderWidth
''')


class FontBahn(ScrollView):
    pass


class Fonts(SettingsCrawler):
    path = StringProperty('./assets/fonts')
    labels = DictProperty()
    set_font = BooleanProperty(True)

    def on_kv_post(self, *largs):
        self.labels = {join(self.path, source, 'font.ttf'): source
                       for source in listdir(self.path)}
