from importlib import import_module

from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy.utils import platform

__all__ = ['CallService', ]

class CallService(EventDispatcher):
    caller = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        caller = kwargs.get('caller')

        if platform in {'android'}:
            jnius = import_module('jnius')
            permissions = import_module('android.permissions')
            Permission = permissions.Permission
            request_permissions = permissions.request_permissions
            autoclass = jnius.autoclass
            permissions = [Permission.CALL_PHONE]
            request_permissions(permissions, self.dial)
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            uri = autoclass('android.net.Uri')
            self.activity = PythonActivity.mActivity

            self.intent = Intent(Intent.ACTION_CALL)
            self.intent.setData(uri.parse(f"tel:{caller}"))
        else:
            Logger.debug("Calls are only supported on Android devices.")

    def dial(self, *largs):
        self.activity.startActivity(self.intent)
