from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.utils import platform

__all__ = ['dial_up', 'CallService', ]

class CallService(EventDispatcher):
    caller = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        caller = kwargs.get('caller')

        if platform in {'android'}:
            from android.permissions import Permission, request_permissions
            from jnius import autoclass
            permissions = [Permission.CALL_PHONE]
            request_permissions(permissions, self.dial)
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            uri = autoclass('android.net.Uri')
            self.activity = PythonActivity.mActivity

            self.intent = Intent(Intent.ACTION_CALL)
            self.intent.setData(uri.parse(f"tel:{caller}"))
        else:
            print("Calls are only supported on Android devices.")

    def dial(self, *largs):
        self.activity.startActivity(self.intent)
