from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re

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
) -> str:
    raise TypeError('invalid input type for words function', date)


def find_date_std(
        date: str, delimiter: tuple = ('/', '.', '-')
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
            except KeyError:
                break
            day = num2words.words(match3.group())
            return day + ' ' + month + ' ' + 'سال ' + year
    raise TypeError('invalid input type for words function', date)


@words.register(str)
def _(
        date: str,
) -> str:
    return find_date_std(date)


@words.register(list)
def _(
        date: list,
) -> str:
    length = len(date)
    if length == 1:
        return find_date_std(''.join(date))
    if 5 >= length >= 2:
        counter = 0
        output = ''

        for d in date:

            if counter == 0:
                match = re.search(r'\d+', d)
                if match is None:
                    continue
                number = int(match.group())
                output += num2words.words(number) + ' '
                counter += 1

            elif counter == 1:
                match = re.search(r'\d+', d)
                if match is None:
                    if d in MONTHS:
                        output += d + ' '
                    else:
                        continue
                else:
                    number = int(match.group())
                    try:
                        output += NUM2MONTHS[number] + ' '
                    except KeyError:
                        break
                counter += 1

            else:
                match = re.search(r'\d+', d)
                if match is None:
                    continue
                number = int(match.group())
                output += 'سال ' + num2words.words(number)
                return output

    raise TypeError('invalid input type for words function', date)
