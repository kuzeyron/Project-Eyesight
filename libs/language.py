import gettext
from importlib import import_module
from os.path import join

from kivy.lang import Observable
from kivy.utils import platform

__all__ = ['locales', 'Lang']
available = {'da', 'de', 'en', 'es', 'et', 'fi',
             'fr', 'is', 'it', 'lt', 'nl', 'no',
             'pt', 'sv'}


def locales():
    if platform == 'android':
        jnius = import_module('jnius')
        autoclass = jnius.autoclass
        locale = autoclass('java.util.Locale')
        locale = str(locale.getDefault().getLanguage())

    elif platform == 'linux':
        locale = import_module('locale')
        locale = str(locale.getdefaultlocale()[0].split("_", -1)[0])

    if locale in available:
        return locale

    return 'en'


class Lang(Observable):
    observers: list = []
    lang = None

    def __init__(self, defaultlang='en'):
        super().__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super().fbind(name, func, *args, **kwargs)

        return False

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super().funbind(name, func, *args, **kwargs)

        return False

    def switch_lang(self, lang):
        if lang in available | {'auto'}:
            lang = locales() if lang == 'auto' else lang
            locale_dir = join('language', 'data', 'locales')
            locales_ = gettext.translation('langapp',
                                           locale_dir,
                                           languages=[lang])
            self.ugettext = locales_.gettext
            self.lang = lang

            for func, largs, _ in self.observers:
                func(largs, None, None)
