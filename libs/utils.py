from importlib import import_module
from os.path import join
from pathlib import Path

__all__ = ('split_nrs', 'importer', 'path_getter')

def split_nrs(nr: str = '', padding: str = ' ') -> str:
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


def importer(mod: str, cls: str = ''):
    module = import_module(mod)

    if not cls:
        return module

    return getattr(module, cls)


def path_getter(instance: str, file: str = '') -> str:
    return join(Path(instance).parent, file)
