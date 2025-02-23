from os.path import join

from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.utils import platform

__all__ = ('Setup', 'SystemFileChooser', 'WALLPAPER_STORAGE', 'WALLPAPER_CACHE')
CUTOUT_HEIGHT = 0.

if platform == 'android':
    from android import mActivity
    from android.runnable import run_on_ui_thread
    from android.storage import app_storage_path
    from androidssystemfilechooser import SystemFileChooser
    from jnius import autoclass

    AndroidView = autoclass('android.view.View')

    try:
        decorview = mActivity.getWindow().getDecorView()
        cutout = decorview.rootWindowInsets.displayCutout
        rect = cutout.boundingRects.get(0)
        CUTOUT_HEIGHT = float(rect.height())
    except Exception:
        pass

    @run_on_ui_thread
    def android_hide_system_bars():
        decorview.setSystemUiVisibility(
            AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
            AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
            AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        )

else:
    def android_hide_system_bars():
        Logger.debug("Hiding bars is only supported on Android devices.")

    def app_storage_path():
        return '.'

    class SystemFileChooser(EventDispatcher):
        def trigger(self):
            pass


WALLPAPER_STORAGE = join(app_storage_path(), '.cache', 'wallpapers')
WALLPAPER_CACHE = join(app_storage_path(), '.cache', '.wallpapers')


class Setup:
    cutout_height = CUTOUT_HEIGHT

    def __init__(self, **kwargs):
        Window.bind(on_keyboard=self.key_press)

    def on_start(self):
        android_hide_system_bars()

    def key_press(self, w, k, *lr):
        if there := k in {27} and platform in {'android'}:
            manager = self.root
            manager.current = 'home'
            manager.transition.direction = 'up'

        return there
