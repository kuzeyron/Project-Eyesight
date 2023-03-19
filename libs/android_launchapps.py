from importlib import import_module

from kivy.logger import Logger
from kivy.utils import platform

__all__ = ['launch_app', ]

def launch_app(package):
    if platform in {'android'}:
        jnius = import_module('jnius')
        autoclass = jnius.autoclass
        Intent = autoclass('android.content.Intent')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        intent = Intent()
        intent.setAction("android.intent.action.MAIN");
        intent.addCategory("android.intent.category.LAUNCHER");
        intent.addCategory("android.intent.category.DEFAULT");

        if package == 'contacts':
            ComponentName = autoclass('android.content.ComponentName')
            intent.setComponent(ComponentName('com.google.android.dialer',
                                              'com.android.dialer.DialtactsActivity'))
        
        elif package == 'messaging':
            intent.addCategory(Intent.CATEGORY_APP_MESSAGING)

        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        activity.startActivity(intent)

    else:
        Logger.debug("Launching apps is only supported on Android devices.")
