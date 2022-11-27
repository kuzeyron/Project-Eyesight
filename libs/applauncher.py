from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.label import Label

from libs.android_launchapps import launch_app
from libs.long_press import LongPress

__all__ = ['AppLauncher', ]

Builder.load_string('''
<AppLauncher>:
    font_size: self.height // 3
    canvas.before:
        Color:
            rgba: root.background_color if root.state == 'down' else app.color
        RoundedRectangle:
            radius: [dp(15), ]
            pos: self.pos
            size: self.size
        Color:
            rgba: 1,1,1,.1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, dp(15)
''')


class AppLauncher(LongPress, Label):
    font_name = StringProperty('assets/fonts/font.ttf')
    long_press_time = NumericProperty(1.5)
    outline_width = NumericProperty(3)
    package = StringProperty('org.test')

    def on_long_press(self, *largs):
        launch_app(self.package)


if __name__ == '__main__':
    from kivy.app import App

    class AppCaller(App):
        def build(self):
            return AppLauncher()

    AppCaller().run()
