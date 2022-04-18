from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re
import random
from random import choices

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

EN_NUM2MONTHS = {
    1: 'ژانویه',
    '1': 'ژانویه',
    '01': 'ژانویه',
    '١': 'ژانویه',
    '۰١': 'ژانویه',
    2: 'فوریه',
    '2': 'فوریه',
    '02': 'فوریه',
    '٢': 'فوریه',
    '۰٢': 'فوریه',
    3: 'مارس',
    '3': 'مارس',
    '03': 'مارس',
    '۳': 'مارس',
    '۰۳': 'مارس',
    4: 'آوریل',
    '4': 'آوریل',
    '04': 'آوریل',
    '۴': 'آوریل',
    '۰۴': 'آوریل',
    5: 'مه',
    '5': 'مه',
    '05': 'مه',
    '۵': 'مه',
    '۰۵': 'مه',
    6: 'ژوئن',
    '6': 'ژوئن',
    '06': 'ژوئن',
    '۶': 'ژوئن',
    '۰۶': 'ژوئن',
    7: 'ژوئیه',
    '7': 'ژوئیه',
    '07': 'ژوئیه',
    '۷': 'ژوئیه',
    '۰۷': 'ژوئیه',
    8: 'اوت',
    '8': 'اوت',
    '08': 'اوت',
    '۸': 'اوت',
    '۰۸': 'اوت',
    9: 'سپتامبر',
    '9': 'سپتامبر',
    '09': 'سپتامبر',
    '۹': 'سپتامبر',
    '۰۹': 'سپتامبر',
    10: 'اکتبر',
    '10': 'اکتبر',
    '١۰': 'اکتبر',
    11: 'نوامبر',
    '11': 'نوامبر',
    '١١': 'نوامبر',
    12: 'دسامبر',
    '12': 'دسامبر',
    '١٢': 'دسامبر'
}

EN_MONTHS2NUM = {
    'ژانویه': 1,
    'فوریه': 2,
    'مارس': 3,
    'آوریل': 4,
    'مه': 5,
    'ژوئن': 6,
    'ژوئیه': 7,
    'اوت': 8,
    'سپتامبر': 9,
    'اکتبر': 10,
    'نوامبر': 11,
    'دسامبر': 12
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

EN_MONTHS = [
    'ژانویه',
    'فوریه',
    'مارس',
    'آوریل',
    'مه',
    'ژوئن',
    'ژوئیه',
    'اوت',
    'سپتامبر',
    'اکتبر',
    'نوامبر',
    'دسامبر'
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
        IR: bool = True,
        random_result: bool = False
) -> str:
    raise TypeError('invalid input type for words function', date)


def find_date_std(
        date: str, delimiter: tuple = ('/', '.', '-'),
        IR: bool = True,
        random_result: bool = False
) -> str:
    for de in delimiter:
        sp = date.split(de)
        if len(sp) == 3:
            if delimiter == '-':
                match = re.search(r'\d+', sp[2])
                match2 = re.search(r'\d+', sp[1])
                match3 = re.search(r'\d+', sp[0])
            else:
                match = re.search(r'\d+', sp[0])
                match2 = re.search(r'\d+', sp[1])
                match3 = re.search(r'\d+', sp[2])
            if match is None or match2 is None or match3 is None:
                break
            year = num2words.words(match.group())
            try:
                if IR:
                    month = NUM2MONTHS[match2.group()]
                else:
                    month = EN_NUM2MONTHS[match2.group()]
                number_month = num2words.words(match2.group())
            except KeyError:
                break
            day = num2words.words(match3.group())
            if not random_result:
                return v1(day, month, year, IR)
            else:
                rand = random.randint(1, 4)
                if rand == 1:
                    return v1(day, month, year, IR)
                elif rand == 2:
                    return v2(day, month, year, IR)
                elif rand == 3:
                    return v3(day, number_month, year, IR)
                else:
                    return v4(day, number_month, year, IR)
    raise TypeError('invalid input type for words function', date)


def v1(day, month, year, IR):
    if IR:
        stmt = choices(['شمسی', 'هجری شمسی', ''], k=1, weights=(0.25, 0.25, 0.5))[0]
    else:
        stmt = choices(['میلادی', ''], k=1, weights=(0.35, 0.65))[0]
    return day + ' ' + month + ' ' + 'سال ' + year + ' ' + stmt


def v2(day, month, year, IR):
    if IR:
        stmt = choices(['شمسی', 'هجری شمسی', ''], k=1, weights=(0.25, 0.25, 0.5))[0]
    else:
        stmt = choices(['میلادی', ''], k=1, weights=(0.35, 0.65))[0]
    return day + ' ' + month + ' ' + year + ' ' + stmt


def v3(day, number_month, year, IR):
    if IR:
        stmt = choices(['شمسی', 'هجری شمسی', ''], k=1, weights=(0.25, 0.25, 0.5))[0]
    else:
        stmt = choices(['میلادی', ''], k=1, weights=(0.35, 0.65))[0]
    return day + ' ' + number_month + ' ' + 'سال ' + year + ' ' + stmt


def v4(day, number_month, year, IR):
    if IR:
        stmt = choices(['شمسی', 'هجری شمسی', ''], k=1, weights=(0.25, 0.25, 0.5))[0]
    else:
        stmt = choices(['میلادی', ''], k=1, weights=(0.35, 0.65))[0]
    return day + ' ' + number_month + ' ' + year + ' ' + stmt


@words.register(str)
def _(
        date: str,
        IR: bool = True,
        random_result: bool = False
) -> str:
    return find_date_std(date, IR=IR, random_result=random_result)


@words.register(list)
def _(
        date: list,
        IR: bool = True,
        random_result: bool = False
) -> str:
    length = len(date)
    if length == 1:
        return find_date_std(''.join(date), IR=IR, random_result=random_result)
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
                    if IR:
                        if d in MONTHS:
                            month = d
                            number_month = num2words.words(MONTHS2NUM[month])
                        else:
                            continue
                    else:
                        if d in EN_MONTHS:
                            month = d
                            number_month = num2words.words(EN_MONTHS2NUM[month])
                        else:
                            continue
                else:
                    number = int(match.group())
                    try:
                        if IR:
                            month = NUM2MONTHS[number]
                        else:
                            month = EN_NUM2MONTHS[number]
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
                    return v1(day, month, year, IR)
                else:
                    rand = random.randint(1, 4)
                    if rand == 1:
                        return v1(day, month, year, IR)
                    elif rand == 2:
                        return v2(day, month, year, IR)
                    elif rand == 3:
                        return v3(day, number_month, year, IR)
                    else:
                        return v4(day, number_month, year, IR)

    raise TypeError('invalid input type for words function', date)
