from typing import Final


def constant(func):
    def func_set(self, value):
        raise TypeError

    def func_get(self):
        return func()

    return property(func_get, func_set)


class _Const(object):
    @constant
    def api_path() -> str:
        return '/tmp/doubleapi'

    @constant
    def utf8() -> str:
        return 'utf-8'


CONST: Final = _Const()
