from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.label import Label

from .launchapps import launch_app
from .long_press import LongPress

__all__ = ('AppLauncher', )

Builder.load_string('''
<AppLauncher>:
    font_size: self.height // 3
    outline_width: app.settings_font_border
    font_name: app.settings_font
    canvas.before:
        Color:
            rgba: root.background_color[:3] + [.05]
        RoundedRectangle:
            pos: self.pos
            radius: app.border_radius
            size: self.size
        Color:
            rgba: 1, 1, 1, .1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, app.border_radius[0]
''')


class AppLauncher(LongPress, Label):
    long_press_time = NumericProperty(1.5)
    package = StringProperty('org.test')

    def on_long_press(self, *largs):
        launch_app(self.package)
