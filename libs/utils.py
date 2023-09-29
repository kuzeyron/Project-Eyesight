from importlib import import_module
from os.path import join
from pathlib import Path

__all__ = ('split_nrs', 'importer', 'path_getter')


def split_nrs(nr=None, padding=None):
    """ Insert padding for numbers """
    nr = nr or ''
    padding = padding or ''
    temp = list(nr)

    if all([' ' not in nr, '-' not in nr]):
        if '+' in temp:
            temp.insert(4, padding)
            temp.insert(7, padding)
        else:
            temp.insert(3, padding)

        temp.insert(-4, padding)
        nr = ''.join(temp)

    return nr


def importer(mod=None, cls=None):
    module = import_module(mod)

    if not cls:
        return module

    return getattr(module, cls)


def path_getter(instance=None, file=None):
    return join(Path(instance).parent, file)
