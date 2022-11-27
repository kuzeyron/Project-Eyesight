from kivy.utils import platform

__all__ = ['dial_up', ]


def dial_up(caller) -> None:
    if platform == 'android':
        from jnius import autoclass

        PythonActivity: type[autoclass] = autoclass(
            'org.kivy.android.PythonActivity'
        )
        Intent: type[autoclass] = autoclass('android.content.Intent')
        uri: type[autoclass] = autoclass('android.net.Uri')
        activity = PythonActivity.mActivity

        intent = Intent(Intent.ACTION_CALL)
        intent.setData(uri.parse(f"tel:{caller}"))

        activity.startActivity(intent)

    else:
        print("Calls are only supported on Android devices.")
