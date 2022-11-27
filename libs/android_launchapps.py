from kivy.utils import platform

__all__ = ['launch_app', ]


def launch_app(package):
    if platform == 'android' and package:
        from jnius import autoclass
        from libs.android_applaunch import available_apps

        if package in sum(available_apps().values(), []):
            Intent: type[autoclass] = autoclass('android.content.Intent')
            PythonActivity: type[autoclass] = autoclass(
                'org.kivy.android.PythonActivity'
            )
            activity: type[PythonActivity] = PythonActivity.mActivity

            pm: type[activity] = activity.getPackageManager()
            app_intent: type[pm] = pm.getLaunchIntentForPackage(package)
            app_intent.setAction(Intent.ACTION_VIEW)
            app_intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

            activity.startActivity(app_intent)

    else:
        print("Launching apps is only supported on Android devices.")
