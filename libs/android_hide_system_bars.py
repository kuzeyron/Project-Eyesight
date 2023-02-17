from kivy.core.window import Window
from kivy.utils import platform

__all__ = ('HideBars', )

if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    # from android.permissions import Permission, request_permissions
    # request_permissions([Permission.CALL_PHONE])

    AndroidView = autoclass('android.view.View')
    AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')

    @run_on_ui_thread
    def android_hide_system_bars():
        view = AndroidPythonActivity.mActivity.getWindow().getDecorView()
        view.setSystemUiVisibility(
            AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
            AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
            AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        )
else:
    def android_hide_system_bars():
        print("Hiding bars is only supported on Android devices.")


class HideBars:

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
