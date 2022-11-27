import gettext
from os.path import join

from kivy.lang import Observable
from kivy.utils import platform

__all__ = ['locales', 'Lang']

def locales():
    available = ('sv', 'en', 'fi')

    if platform == 'android':
        from jnius import autoclass

        locale = autoclass('java.util.Locale')
        locale = str(
            locale.getDefault().getLanguage()
        )

    elif platform == 'linux':
        import locale

        locale = str(
            locale.getdefaultlocale()[0].split("_", -1)[0]
        )

    if locale in available:
        return locale

    return 'en'


class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join('language', 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)
