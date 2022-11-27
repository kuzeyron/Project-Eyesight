from kivy.utils import platform

__all__ = [
    'available_contact_apps',
    'available_sms_apps',
    'available_browser_apps',
    'available_apps',
    'return_value_of_subjects',
    'os_return_value_of_subject',
]


def _find_packages(intent) -> list:
    from jnius import autoclass, cast

    PythonActivity: type[autoclass] = autoclass(
        'org.kivy.android.PythonActivity'
    )
    context: type[cast] = cast(
        'android.content.Context',
        PythonActivity.mActivity
    )

    pm = context.getPackageManager()
    packages = pm.queryIntentActivities(intent, 0).toArray()
    apps = {package.activityInfo.packageName for package in packages}

    return list(apps)


def _intent() -> tuple:
    from jnius import autoclass

    Intent: type[autoclass] = autoclass('android.content.Intent')
    intent = Intent()

    return Intent, intent


def available_contact_apps() -> list:
    Intent, intent = _intent()
    intent.setAction(Intent.ACTION_MAIN)
    intent.addCategory(Intent.CATEGORY_APP_CONTACTS)

    return _find_packages(intent)


def available_sms_apps() -> list:
    Intent, intent = _intent()
    intent.setAction(Intent.ACTION_MAIN)
    intent.addCategory(Intent.CATEGORY_APP_MESSAGING)

    return _find_packages(intent)


def available_browser_apps() -> list:
    Intent, intent = _intent()
    intent.setAction(Intent.ACTION_MAIN)
    intent.addCategory(Intent.CATEGORY_APP_BROWSER)

    return _find_packages(intent)


def available_apps() -> dict:
    return {
        'contacts': available_contact_apps(),
        'messaging': available_sms_apps(),
        'browsers': available_browser_apps()
    }


def return_value_of_subjects(subject) -> list:
    content: dict = available_apps()
    data: list = content.get(subject, [])

    if data:
        return data[0]

    return data


def os_return_value_of_subject(subject):
    return return_value_of_subjects(subject) if platform == 'android' else ''
