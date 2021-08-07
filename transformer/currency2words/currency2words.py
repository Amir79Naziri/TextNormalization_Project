from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re

CURRENCY2WORD = {
    '£': ['پوند', 'سنت'],
    '€': ['یورو', 'سنت'],
    'Rials': ['ریال', ],
    'ریال': ['ریال', ],
    'تومان': ['تومان', ],
    '$': ['دلار', 'پنی'],
    'دلار': ['دلار', 'پنی'],
    'پوند': ['پوند', 'سنت'],
    'یورو': ['یورو', 'سنت'],
    'پنی': ['پنی', ],
    'سنت': ['سنت', ]
}


# ٢۰Rials
# 20 £
# 20£
# £20
# £ 20
# ٢۰


@singledispatch
def words(
        currency: Union[str, list],
) -> str:
    raise TypeError('invalid input type for words function', currency)


def find_currency(
        currency: str
) -> str:
    for cur in CURRENCY2WORD:
        if cur == '$':
            cur = '[' + cur + ']'
        match1 = re.search(cur, currency)

        if match1 is None:
            continue
        match2 = re.search(r'\d*\.\d+|\d+', currency)

        if match2 is None:
            break

        currency_unit = CURRENCY2WORD[match1.group()]
        number = round(float(match2.group()), 3)
        s_number = int(number)
        diff = round(number - s_number, 3)
        diff2 = round((number - s_number) / 0.01, 3)
        if currency_unit[0] == 'ریال' or currency_unit[0] == 'پنی' or\
                currency_unit[0] == 'سنت' or currency_unit[0] == 'تومان':
            if diff < 0.01:
                return num2words.words(s_number) + ' ' + currency_unit[0]
            else:
                return num2words.words(number) + ' ' + currency_unit[0]
        else:
            if diff2 < 0.01:
                return num2words.words(s_number) + ' ' + currency_unit[0]
            else:
                return num2words.words(s_number) + ' ' + currency_unit[0] + ' و ' + \
                       num2words.words(diff2) + ' ' + currency_unit[1]

    raise TypeError('invalid input type for words function', currency)


@words.register(str)
def _(
        currency: str,
) -> str:
    return find_currency(currency)


@words.register(list)
def _(
        currency: list,
) -> str:
    if 1 <= len(currency) <= 2:
        return find_currency(''.join(currency))
    raise TypeError('invalid input type for words function', currency)
