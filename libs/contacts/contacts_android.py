from android.permissions import Permission, request_permissions
from jnius import autoclass
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
from kivy.uix.recycleview import RecycleView
from ..utils import path_getter, split_nrs

__all__ = ('Contacts', )

Builder.load_file(path_getter(__file__, 'contacts.kv'))


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
    """ Extracts the data from Android. Part code from pydroid. """

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


def add_contacts(permissions, status):
    perm = {p.split('.')[-1]: status[xy] for xy, p in enumerate(permissions)}
    _app = App.get_running_app()

    if perm.get('READ_CONTACTS', False):
        content = _cursor_interaction(bool(int(
            _app.settings_starred_contacts)))
        _app.root.ids.contacts.data = content[0] or content[1]

    _app.can_use_call = perm.get('CALL_PHONE', False)


class Contacts(RecycleView):
    __events__ = ('on_accessing_permissions', )
    permissions = ListProperty((Permission.READ_CONTACTS,
                                Permission.CALL_PHONE))
    starred = BooleanProperty(True)
    bar_width = NumericProperty(0)
    opacity = NumericProperty(0)

    def on_kv_post(self, *largs):
        _app = App.get_running_app()
        _app.bind(_change_of_events=self.on_accessing_permissions)
        self.dispatch('on_accessing_permissions')

    def on_accessing_permissions(self, *largs):
        request_permissions(self.permissions, add_contacts)
