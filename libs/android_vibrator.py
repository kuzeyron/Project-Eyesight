from kivy.utils import platform

__all__ = ['vibrate', ]


def vibrate(duration):
    if platform in {'android'}:
        from jnius import autoclass

        Context: type[autoclass] = autoclass('android.content.Context')
        PythonActivity: type[autoclass] = autoclass(
            'org.kivy.android.PythonActivity'
        )
        activity = PythonActivity.mActivity
        vibrator = activity.getSystemService(
            Context.VIBRATOR_SERVICE
        )

        vibrator.vibrate(duration * 1000)

        return vibrator

    else:
        print("Vibrator function is only supported on Android devices.")

        class FakeVib:
            def vibrate(self, *largs) -> None:
                pass

            def cancel(self, *largs) -> None:
                pass

        return FakeVib()
