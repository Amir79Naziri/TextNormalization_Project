from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re
import random

NUM2MONTHS = {
    1: 'فروردین',
    '1': 'فروردین',
    '01': 'فروردین',
    '١': 'فروردین',
    '۰١': 'فروردین',
    2: 'اردیبهشت',
    '2': 'اردیبهشت',
    '02': 'اردیبهشت',
    '٢': 'اردیبهشت',
    '۰٢': 'اردیبهشت',
    3: 'خرداد',
    '3': 'خرداد',
    '03': 'خرداد',
    '۳': 'خرداد',
    '۰۳': 'خرداد',
    4: 'تیر',
    '4': 'تیر',
    '04': 'تیر',
    '۴': 'تیر',
    '۰۴': 'تیر',
    5: 'مرداد',
    '5': 'مرداد',
    '05': 'مرداد',
    '۵': 'مرداد',
    '۰۵': 'مرداد',
    6: 'شهریور',
    '6': 'شهریور',
    '06': 'شهریور',
    '۶': 'شهریور',
    '۰۶': 'شهریور',
    7: 'مهر',
    '7': 'مهر',
    '07': 'مهر',
    '۷': 'مهر',
    '۰۷': 'مهر',
    8: 'آبان',
    '8': 'آبان',
    '08': 'آبان',
    '۸': 'آبان',
    '۰۸': 'آبان',
    9: 'آذر',
    '9': 'آذر',
    '09': 'آذر',
    '۹': 'آذر',
    '۰۹': 'آذر',
    10: 'دی',
    '10': 'دی',
    '١۰': 'دی',
    11: 'بهمن',
    '11': 'بهمن',
    '١١': 'بهمن',
    12: 'اسفند',
    '12': 'اسفند',
    '١٢': 'اسفند'
}

MONTHS2NUM = {
    'فروردین': 1,
    'اردیبهشت': 2,
    'خرداد': 3,
    'تیر': 4,
    'مرداد': 5,
    'شهریور': 6,
    'مهر': 7,
    'آبان': 8,
    'آذر': 9,
    'دی': 10,
    'بهمن': 11,
    'اسفند': 12
}

MONTHS = [
    'فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
    'دی',
    'بهمن',
    'اسفند'
]


# 2014-03-01
# 2014/03/01
# 2014.03.1
# ١٢ اردیبهشت ١٢١٢
# 29ام اردیبهشت 1412
# 29 اردیبهشت سال 1412
# 29ام اردیبهشت سال 1412

@singledispatch
def words(
        date: Union[str, list],
        random_result: bool = False
) -> str:
    raise TypeError('invalid input type for words function', date)


def find_date_std(
        date: str, delimiter: tuple = ('/', '.', '-'),
        random_result: bool = False
) -> str:
    for de in delimiter:
        sp = date.split(de)
        if len(sp) == 3:
            match = re.search(r'\d+', sp[2])
            match2 = re.search(r'\d+', sp[1])
            match3 = re.search(r'\d+', sp[0])
            if match is None or match2 is None or match3 is None:
                break
            year = num2words.words(match.group())
            try:
                month = NUM2MONTHS[match2.group()]
                number_month = num2words.words(match2.group())
            except KeyError:
                break
            day = num2words.words(match3.group())
            if not random_result:
                return v1(day, month, year)
            else:
                rand = random.randint(1, 4)
                if rand == 1:
                    return v1(day, month, year)
                elif rand == 2:
                    return v2(day, month, year)
                elif rand == 3:
                    return v3(day, number_month, year)
                else:
                    return v4(day, number_month, year)
    raise TypeError('invalid input type for words function', date)


def v1(day, month, year):
    return day + ' ' + month + ' ' + 'سال ' + year


def v2(day, month, year):
    return day + ' ' + month + ' ' + year


def v3(day, number_month, year):
    return day + ' ' + number_month + ' ' + 'سال ' + year


def v4(day, number_month, year):
    return day + ' ' + number_month + ' ' + year


@words.register(str)
def _(
        date: str,
        random_result: bool = False
) -> str:
    return find_date_std(date, random_result=random_result)


@words.register(list)
def _(
        date: list,
        random_result: bool = False
) -> str:
    length = len(date)
    if length == 1:
        return find_date_std(''.join(date), random_result=random_result)
    if 5 >= length >= 2:
        counter = 0
        day, month, number_month = None, None, None

        for d in date:

            if counter == 0:
                match = re.search(r'\d+', d)
                if match is None:
                    continue
                number = int(match.group())
                day = num2words.words(number)
                counter += 1

            elif counter == 1:
                match = re.search(r'\d+', d)
                if match is None:
                    if d in MONTHS:
                        month = d
                        number_month = num2words.words(MONTHS2NUM[month])
                    else:
                        continue
                else:
                    number = int(match.group())
                    try:
                        month = NUM2MONTHS[number]
                        number_month = num2words.words(number)
                    except KeyError:
                        break
                counter += 1

            else:
                match = re.search(r'\d+', d)
                if match is None:
                    continue
                number = int(match.group())
                year = num2words.words(number)

                if not random_result:
                    return v1(day, month, year)
                else:
                    rand = random.randint(1, 4)
                    if rand == 1:
                        return v1(day, month, year)
                    elif rand == 2:
                        return v2(day, month, year)
                    elif rand == 3:
                        return v3(day, number_month, year)
                    else:
                        return v4(day, number_month, year)

    raise TypeError('invalid input type for words function', date)
