from importlib import import_module

from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy.utils import platform


class CallService(EventDispatcher):
    __events__ = ('on_android', 'on_linux')
    caller = StringProperty()

    def call(self, caller):
        self.caller = caller
        self.dispatch(f'on_{platform}')

    def on_android(self):
        self.mActivity = import_module('android').mActivity
        permissions = import_module('android.permissions')
        request_permissions = permissions.request_permissions
        Permission = permissions.Permission
        autoclass = import_module('jnius').autoclass
            
        Intent = autoclass('android.content.Intent')
        uri = autoclass('android.net.Uri')

        self.intent = Intent(Intent.ACTION_CALL)
        self.intent.setData(uri.parse(f"tel:{self.caller}"))
        
        request_permissions([Permission.CALL_PHONE], self.dial)
        
    def on_linux(self):
        Logger.debug("Calls are only supported on Android devices.")

    def dial(self, *largs):
        self.mActivity.startActivity(self.intent)

