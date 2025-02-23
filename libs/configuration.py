import sqlite3
from os.path import exists, join

from kivy.utils import platform

from libs.setup import app_storage_path


__all__ = ('locales', 'set_value', 'get_value', 'get_language', )


def locales():
    available = {'da', 'de', 'en', 'es', 'et', 'fi',
                 'fr', 'is', 'it', 'lt', 'nl', 'no',
                 'pt', 'sv'}

    if platform == 'android':
        from jnius import autoclass
        locale = autoclass('java.util.Locale')
        locale = str(locale.getDefault().getLanguage())
    elif platform == 'linux':
        from locale import getdefaultlocale
        locale = getdefaultlocale()[0]
        locale = str(locale.split("_", -1)[0])

    return locale if locale in available else 'en'


def _dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


def _reset_db(default_path=None, filename=None):
    default_path = default_path or join('assets', 'data', 'default.dbk')
    filename = filename or 'config.db'
    backup = sqlite3.connect(default_path)
    new = sqlite3.connect(join(app_storage_path(), filename))
    query = "".join(line for line in backup.iterdump())
    new.executescript(query)

    return new


def _db_exist(file=None):
    file = file or join(app_storage_path(), 'config.db')

    if exists(file):
        return sqlite3.connect(file)

    return _reset_db()


def get_value(table=None) -> dict:
    database = _db_exist()
    database.row_factory = _dict_factory
    cur = database.cursor()
    res = cur.execute(f"SELECT * FROM {table}")
    result = res.fetchone()
    res.close()

    return result


def configuration(table=None) -> dict:
    table = table or []
    database = _db_exist()
    database.row_factory = _dict_factory
    cur = database.cursor()
    res = cur.execute(f"SELECT * FROM {', '.join(table)}")
    result = res.fetchone()
    res.close()

    return result


def set_value(table=None, target=None, content=None):
    database = _db_exist()
    cur = database.cursor()
    res = cur.execute(f"UPDATE {table} SET {target}='{content}'")
    database.commit()
    res.close()


def get_language() -> tuple:
    lang = get_value('language')['language']
    language = locales() if lang == 'auto' else lang

    return language, 'language_language'
