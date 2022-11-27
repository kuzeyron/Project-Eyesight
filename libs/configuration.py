import sqlite3
import sys
from importlib import import_module
from os.path import dirname, exists, join

from kivy.utils import platform

__all__ = [
    'locales',
]


def locales():
    available = {'sv', 'en', 'fi'}

    if platform == 'android':
        jnius = import_module('jnius')
        locale = jnius.autoclass('java.util.Locale')
        locale = str(locale.getDefault().getLanguage())
    elif platform == 'linux':
        locale = import_module('locale')
        locale = locale.getdefaultlocale()[0]
        locale = str(locale.split("_", -1)[0])

    return locale if locale in available else 'en'


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


def reset_db():
    file = join(dirname(sys.argv[0]),
                'assets',
                'data',
                'default.dbk')

    if exists(file):
        backup = sqlite3.connect(file)
        new = sqlite3.connect('config.db')
        query = "".join(line for line in backup.iterdump())
        new.executescript(query)

        return new

    return False


def db_exist(file=None):
    file = file or 'config.db'

    if isinstance(file, str) and exists(file):
        return sqlite3.connect(file)

    return reset_db()


def get_value(table=None) -> dict:
    database = db_exist()
    database.row_factory = dict_factory
    cur = database.cursor()
    res = cur.execute(f"SELECT * FROM {table}")
    result = res.fetchone()
    res.close()

    return result


def set_value(table=None, target=None, content=None):
    database = db_exist()
    cur = database.cursor()
    res = cur.execute(f"UPDATE {table} SET {target}='{content}'")
    database.commit()
    res.close()


def get_language() -> tuple:
    config = get_value('language')
    language = config['language']
    auto = bool(config['auto'])
    lang = locales() if auto else language

    return (auto, lang)
