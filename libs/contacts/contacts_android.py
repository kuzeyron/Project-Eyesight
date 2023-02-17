from functools import wraps

from android.permissions import (Permission, check_permission,
                                 request_permissions)
from android.runnable import run_on_ui_thread
from jnius import autoclass
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
from kivy.uix.recycleview import RecycleView

from libs.utils import path_getter, split_nrs

__all__ = ('Contacts', )

Builder.load_file(path_getter(__file__, 'contacts.kv'))

def bind_permissions(lookup):
    """ Decorator to be used with Kivy.
    `permissions` is a `list`.
    Snippet: ```
        from android.permissions import (Permission, check_permission,
                                         request_permissions)
        from kivy.event import EventDispatcher
        from kivy.properties import ListProperty, StringProperty

        class PermissionEvents(EventDispatcher):
            permissions = ListProperty([Permission. ...])
            example_binding = StringProperty('Not set')

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.bind(example_binding=self.impact)
                request_permissions(self.permissions, self.impact)

            @bind_permissions
            def impact(self, *largs):
                # Decorator lookup the permissions in self.permissions.
                # Decorator continues if all permissions are set
                self.example_binding = 'Is now set!'
                print(self.example_binding)
    ```
    """
    @wraps(lookup)
    def check_permissions(i, p, s):
        if isinstance(s, list):
            lookup(i, p, s)
    return check_permissions


def _cursor_interaction(caller) -> tuple:
    """ Interaction with Android for contact informations """
    try:
        # Since QUERY_ALL_PACKAGES is forbidden to use
         # with the Play Strore, we just have to try
        Contract: str = 'android.provider.ContactsContract'
        Common: str = 'CommonDataKinds'
        Phone = autoclass(f"{Contract}${Common}$Phone")
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        cursor_ = activity.getContentResolver()
        PROJECTION: list = [Phone.CONTACT_ID,
                            Phone.DISPLAY_NAME,
                            Phone.STARRED,
                            Phone.NUMBER]
        cursor = cursor_.query(Phone.CONTENT_URI,
                               PROJECTION,
                               None,
                               None,
                               Phone.DISPLAY_NAME)

        return _cursor_extraction(cursor, Phone, caller)

    except Exception:
        # We cannot access the contacts
        return ()


def _cursor_extraction(cursor, Phone, caller) -> tuple:
    """ Extracts the data from Android """

    nm_index: int = cursor.getColumnIndex(Phone.DISPLAY_NAME)
    nr_index: int = cursor.getColumnIndex(Phone.NUMBER)
    strd_index: int = cursor.getColumnIndex(Phone.STARRED)

    found_nrs: list = []
    # pos = found contacts
    # neg = all contacts or not listed
    pos: list = []
    neg: list = []

    while cursor.moveToNext():
        nm: str = cursor.getString(nm_index)
        nr: str = cursor.getString(nr_index)
        intr: int = int(cursor.getString(strd_index))

        if caller is None:
            intr = 1

        if all([nr not in found_nrs, caller is not False, intr]):
            pos.append({'name': nm, 'number': split_nrs(nr)})
        elif nr not in found_nrs:
            neg.append({'name': nm, 'number': split_nrs(nr)})

        found_nrs.append(nr)

    cursor.close()

    return pos, neg


class Contacts(RecycleView, EventDispatcher):
    __events__ = ('on_accessing_permissions', 'on_permission_validation')
    permissions = ListProperty((Permission.READ_CONTACTS, Permission.CALL_PHONE))
    starred = BooleanProperty(True)
    bar_width = NumericProperty(0)
    opacity = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contact_type = kwargs.get('starred', True)
        _app = App.get_running_app()
        _app.bind(trigger_events=self.on_accessing_permissions)
        self.dispatch('on_accessing_permissions')

    def on_accessing_permissions(self, *largs) -> None:
        request_permissions(self.permissions, self.on_permission_validation)
    
    @bind_permissions
    def on_permission_validation(self, *largs) -> None:
        content = _cursor_interaction(self.starred)
        self.data = content[0] or content[1]
