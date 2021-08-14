from typing import Union
from functools import singledispatch

MISCELLANEOUS_MAP = {
    'م.': 'میلادی',
    'ًَه.ش': 'هجری شمسی',
    'ه.ق': 'هجری قمری',
    'ا.': 'اسم',
    'ص': 'صلی اللّه علیه و آله',
    '(ص)': 'صلی اللّه علیه و آله',
    'س': 'سلام اللّه علیه',
    '(س)': 'سلام اللّه علیه',
    'ع': 'علیه السلام',
    '(ع)': 'علیه السلام',
    'ره': 'رحمه اللّه علیه',
    '(ره)': '',
    'خ': 'خیابان',
    'پ': 'پلاک',
    'ک': 'کوچه',
    'ت ت': 'تاریخ تولد',
    'ش ش': 'شماره شناسنامه',
    'ش ح': 'شماره حساب',
    'ک پ': 'کد پستی',
    'ص پ': 'صندوق پستی'
}


@singledispatch
def words(
        mis: Union[str, list],
        random_result: bool = False
) -> str:
    raise TypeError('invalid input type for words function', mis)


@words.register(str)
def _(
        mis: str,
        random_result: bool = False
) -> str:
    try:
        return MISCELLANEOUS_MAP[mis]
    except KeyError:
        pass

    raise TypeError('invalid input type for words function', mis)


@words.register(list)
def _(
        mis: list,
        random_result: bool = False
) -> str:
    if 1 <= len(mis) <= 2:
        mis = ' '.join(mis)
        try:
            return MISCELLANEOUS_MAP[mis]
        except KeyError:
            pass

    raise TypeError('invalid input type for words function', mis)

