from importlib import import_module

from kivy.utils import platform

__all__ = ['battery', ]


def battery():
    if platform == 'android':
        jnius = import_module('jnius')
        autoclass = jnius.autoclass
        cast = jnius.cast

        BatteryManager = autoclass('android.os.BatteryManager')
        Intent = autoclass('android.content.Intent')
        IntentFilter = autoclass('android.content.IntentFilter')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        ifilter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        battery_status = cast('android.content.Intent',
                              activity.registerReceiver(None, ifilter))

        query = battery_status.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        is_charging = query == BatteryManager.BATTERY_STATUS_CHARGING
        is_full = query == BatteryManager.BATTERY_STATUS_FULL

        level = battery_status.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        scale = battery_status.getIntExtra(BatteryManager.EXTRA_SCALE, -1)

        return int((level / max(scale, 1)) * 100), is_charging or is_full

    print("Battery function is only supported on Android devices.")
    return -1, False


if __name__ == '__main__':
    print(battery())
