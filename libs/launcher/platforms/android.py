import time
from functools import partial
from io import BytesIO
from os import makedirs
from os.path import getmtime, isfile, join
from shutil import rmtree
from threading import Thread

from android.storage import app_storage_path
from jnius import autoclass, cast
from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.logger import Logger

from ..appicons import AppIcon

__all__ = ('GetPackages', )


class GetPackages:
    __events__ = ('on_draw_content', )

    def on_kv_post(self, *largs):
        Thread(target=self.ready, daemon=True).start()

    def ready(self):
        Intent = autoclass('android.content.Intent')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        intent = Intent()
        intent.setAction(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_LAUNCHER)
        context = cast('android.content.Context',
                       PythonActivity.mActivity)

        pm = context.getPackageManager()
        packages = pm.queryIntentActivities(intent, 0).toArray()

        self.dispatch('on_draw_content', pm, packages)

    def on_draw_content(self, pm, domains):
        """ Code by AnshDadwal """
        OutputStream = autoclass('java.io.ByteArrayOutputStream')
        Bitmap = autoclass("android.graphics.Bitmap")
        Canvas = autoclass("android.graphics.Canvas")
        BitmapConfig = autoclass("android.graphics.Bitmap$Config")
        CompressFormat = autoclass("android.graphics.Bitmap$CompressFormat")
        cache_folder = join(app_storage_path(), '.cache', 'icons')
        makedirs(cache_folder, exist_ok=True)

        if time.time() - getmtime(cache_folder) >= 259200:
            rmtree(cache_folder)
            Logger.debug('Deleted cached icons')
            makedirs(cache_folder, exist_ok=True)

        for domain in domains:
            package = domain.activityInfo.packageName
            info = pm.getApplicationInfo(package, pm.GET_META_DATA)
            name = pm.getApplicationLabel(info)
            filename = join(cache_folder, f'{package}.png')
            image = None

            if not (old := isfile(filename)):
                Logger.debug('Rendering icon: %s', filename)
                drawable = domain.activityInfo.loadIcon(pm)
                bitmap = Bitmap.createBitmap(100, 100, BitmapConfig.ARGB_8888)
                stream, canvas = OutputStream(), Canvas(bitmap)
                drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight())
                drawable.draw(canvas)
                bitmap.compress(CompressFormat.PNG, 100, stream)
                image = Image(BytesIO(bytes(stream.toByteArray())), ext='png')
            else:
                Logger.debug('Loading icon: %s', filename)
                image = Image(filename)

            Clock.schedule_once(partial(self.add_one, name=name,
                                        package=package, texture=image,
                                        old=old, path=filename), 0)

    def add_one(self, *largs, **kwargs):
        texture = kwargs['texture']

        if not kwargs['old']:
            texture.save(kwargs['path'], flipped=False)

        kwargs['arguments'] = kwargs
        kwargs['texture'] = texture.texture
        self.add_widget(AppIcon(**kwargs))
