from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform

from ..utils import importer

__all__ = ('Applications', 'AppContainer', 'AppList', )

GetApps = importer(f'libs.launcher.platforms.{platform}', 'GetPackages')
Builder.load_string('''
#:import platform kivy.utils.platform

<AppContainer>:
    padding: 0, dp(5), 0, app.cutout_height or dp(5)
    canvas.before:
        Color:
            rgba: 0, 0, 0, .3
        RoundedRectangle:
            pos: self.pos
            radius: [dp(10), ]
            size: self.size
    ScrollView:
        bar_width: dp(3)
        do_scroll_x: False
        BoxLayout:
            height: self.minimum_height
            padding: [dp(5), ] * 4
            size_hint_y: None
            Applications:
                spacing: dp(40)
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(3 if platform == 'android' else 20), \
                         dp(0 if platform == 'android' else 10)
''')


class Applications(GetApps, StackLayout):  # type: ignore
    padding = ListProperty([dp(10), ] * 4)
    spacing = ListProperty([dp(0), ] * 2)


class AppContainer(BoxLayout):
    pass
