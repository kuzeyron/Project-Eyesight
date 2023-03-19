from importlib import import_module

from kivy.core.window import Window
from kivy.logger import Logger
from kivy.utils import platform

__all__ = ('HideBars', )
CUTOUT_HEIGHT = 0.

if platform == 'android':
    ui_thread = import_module('android.runnable').run_on_ui_thread
    jnius = import_module('jnius')
    autoclass = jnius.autoclass

    ANDROID_VERSION_CODES = autoclass('android.os.Build$VERSION_CODES')
    ANDROID_VERSION = autoclass('android.os.Build$VERSION')
    AndroidView = autoclass('android.view.View')
    mActivity = import_module('android').mActivity

    if ANDROID_VERSION.SDK_INT >= ANDROID_VERSION_CODES.P:
        decorview = mActivity.getWindow().getDecorView()
        cutout = decorview.rootWindowInsets.displayCutout
        rect = cutout.boundingRects.get(0)
        CUTOUT_HEIGHT = float(rect.height())

    @ui_thread
    def android_hide_system_bars():
        decorview.setSystemUiVisibility(
            AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
            AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
            AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        )
else:
    def android_hide_system_bars():
        Logger.debug("Hiding bars is only supported on Android devices.")


class HideBars:
    cutout_height = CUTOUT_HEIGHT

    def __init__(self, **kwargs):
        Window.bind(on_keyboard=self.key_press)

    def on_start(self):
        android_hide_system_bars()

    def key_press(self, w, k, *lr):
        if there := k in {27} and platform in {'android'}:
            manager = self.root.ids.manager
            manager.current = 'home'
            manager.transition.direction = 'up'

        return there
