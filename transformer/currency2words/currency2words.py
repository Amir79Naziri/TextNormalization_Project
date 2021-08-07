from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re
import random

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
        random_result: bool = False
) -> str:
    raise TypeError('invalid input type for words function', currency)


def find_currency(
        currency: str,
        random_result: bool = False
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
        if not random_result:
            return v1(number, currency_unit)
        else:
            rand = random.randint(1, 3)
            if rand == 1:
                return v1(number, currency_unit)
            elif rand == 2:
                return v2(number, currency_unit)
            else:
                return v3(number, currency_unit)

    raise TypeError('invalid input type for words function', currency)


def v1(number, currency_unit):
    s_number = int(number)
    diff = round(number - s_number, 3)
    diff2 = round((number - s_number) / 0.01, 3)
    if currency_unit[0] == 'ریال' or currency_unit[0] == 'پنی' or \
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


def v2(number, currency_unit):
    s_number = int(number)
    diff = round(number - s_number, 3)
    diff2 = round((number - s_number) / 0.01, 3)
    if currency_unit[0] == 'ریال' or currency_unit[0] == 'پنی' or \
            currency_unit[0] == 'سنت' or currency_unit[0] == 'تومان':
        if diff < 0.01:
            return num2words.words(s_number) + ' ' + currency_unit[0]
        else:
            return num2words.words(number, decimal_separator=' ممیز ', mode=0) + ' ' + currency_unit[0]
    else:
        if diff2 < 0.01:
            return num2words.words(s_number) + ' ' + currency_unit[0]
        else:
            return num2words.words(s_number) + ' ' + currency_unit[0] + ' و ' + \
                   num2words.words(diff2) + ' ' + currency_unit[1]


def v3(number, currency_unit):
    s_number = int(number)
    diff = round(number - s_number, 3)
    diff2 = round((number - s_number) / 0.01, 3)
    if currency_unit[0] == 'ریال' or currency_unit[0] == 'پنی' or \
            currency_unit[0] == 'سنت' or currency_unit[0] == 'تومان':
        if diff < 0.01:
            return num2words.words(s_number) + ' ' + currency_unit[0]
        else:
            return num2words.words(number, decimal_separator=' ممیز ', mode=1) + ' ' + currency_unit[0]
    else:
        if diff2 < 0.01:
            return num2words.words(s_number) + ' ' + currency_unit[0]
        else:
            return num2words.words(s_number) + ' ' + currency_unit[0] + ' و ' + \
                   num2words.words(diff2) + ' ' + currency_unit[1]


@words.register(str)
def _(
        currency: str,
        random_result: bool = False
) -> str:
    return find_currency(currency, random_result=random_result)


@words.register(list)
def _(
        currency: list,
        random_result: bool = False
) -> str:
    if 1 <= len(currency) <= 2:
        return find_currency(''.join(currency), random_result=random_result)
    raise TypeError('invalid input type for words function', currency)
