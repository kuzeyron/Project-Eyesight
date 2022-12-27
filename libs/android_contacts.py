from kivy.utils import platform

__all__ = [
    'get_kind_of_contacts',
]


def _split_nrs(nr: str = '', padding: str = ' ') -> str:
    """ Insert padding for numbers """

    temp: list = list(nr)

    if all([' ' not in nr, '-' not in nr]):
        if '+' in temp:
            temp.insert(4, padding)
            temp.insert(7, padding)
        else:
            temp.insert(3, padding)

        temp.insert(-4, padding)
        nr = ''.join(temp)

    return nr


def _cursor_interaction(caller) -> tuple:
    """ Interaction with Android for contact informations """

    from android.permissions import Permission, request_permissions
    from jnius import autoclass
    from libs.android_applaunch import available_contact_apps

    request_permissions([Permission.READ_CONTACTS])

    if any(available_contact_apps()):
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

    return ()


def _cursor_extraction(cursor, Phone, caller) -> tuple:
    """ Extracts the data from Android """

    nm_index: int = cursor.getColumnIndex(Phone.DISPLAY_NAME)
    nr_index: int = cursor.getColumnIndex(Phone.NUMBER)
    strd_index: int = cursor.getColumnIndex(Phone.STARRED)

    found_nrs: list = []
    pos: list = []
    neg: list = []

    while cursor.moveToNext():
        nm: str = cursor.getString(nm_index)
        nr: str = cursor.getString(nr_index)
        intr: int = int(cursor.getString(strd_index))

        if caller is None:
            intr = 1

        if all([nr not in found_nrs, caller is not False, intr]):
            pos.append({'name': nm, 'number': _split_nrs(nr)})
        elif nr not in found_nrs:
            neg.append({'name': nm, 'number': _split_nrs(nr)})

        found_nrs.append(nr)

    cursor.close()

    return pos, neg


def get_kind_of_contacts(contact_type: bool = True) -> list:
    """ Partly dummy function to support all platforms and Android """

    if platform == 'android':
        content: tuple = _cursor_interaction(contact_type)

        # Return negative list if positive list is empty
        return content[0] or content[1]

    print('Getting contacts is only available on Android devices')
    return [
        {'name': 'John Smith', 'number':  _split_nrs('+3580000000')},
        {'name': 'Sally Sweet', 'number':  _split_nrs('+3581111111')},
        {'name': 'John Doe', 'number':  _split_nrs('+3582222222')}
    ]
