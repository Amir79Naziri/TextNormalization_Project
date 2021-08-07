from typing import Union
from functools import singledispatch
from transformer.num2words import num2words
import re
import random


# 12:12:12
# 12:12:12 AM
# 12:12:12 PM
# 12:13
# 12:13 AM
# 12:13 PM

@singledispatch
def words(
        time: Union[str, list],
        random_result=False
) -> str:
    raise TypeError('invalid input type for words function', time)


def find_time(
        time: str,
        random_result=False
) -> str:
    times = time.split(':')
    counter = 0
    if 2 <= len(times) <= 3:
        hours, minutes, seconds = None, None, None
        for t in times:
            if counter == 0:
                match = re.search(r'\d+', t)
                if match is None:
                    continue
                hours = int(match.group())
                counter += 1
            elif counter == 1:
                match = re.search(r'\d+', t)
                if match is None:
                    continue
                minutes = int(match.group())
                counter += 1
            else:
                match = re.search(r'\d+', t)
                if match is None:
                    continue
                seconds = int(match.group())
                break
        if minutes is None or hours is None:
            raise TypeError('invalid input type for words function', time)

        mode = 'AM'
        if hours <= 12 and (re.search(r'PM|pm|Pm|pM', time) is not None or
                            re.search('بعد ازظهر|بعداز ظهر|بعد از ظهر|بعدازظهر', time) is not None):
            mode = 'PM'

        if hours > 24 or minutes > 60 or (seconds is not None and seconds > 60) or (mode == 'PM' and hours + 12 > 24):
            raise TypeError('invalid input type for words function', time)

        if not random_result:
            return v1(hours, minutes, seconds, mode)
        else:
            rand = random.randint(1, 4)
            if rand == 1:
                return v1(hours, minutes, seconds, mode)
            elif rand == 2:
                return v2(hours, minutes, seconds, mode)
            elif rand == 3:
                return v3(hours, minutes, seconds, mode)
            else:
                return v4(hours, minutes, seconds, mode)

    raise TypeError('invalid input type for words function', time)


def v1(hours, minutes, seconds, mode):
    if mode == 'PM':
        hours += 12
    if hours == 24:
        hours = 0

    if hours != 0:
        return num2words.words(hours) + ' و ' + num2words.words(minutes) + ' دقیقه' + \
               (' و ' + num2words.words(seconds) + ' ثانیه' if seconds is not None else '')
    else:
        return num2words.words(minutes) + ' دقیقه' + \
               (' و ' + num2words.words(seconds) + ' ثانیه' if seconds is not None else '') + ' بامداد'


def v2(hours, minutes, seconds, mode):
    if mode == 'PM':
        hours += 12

    return num2words.words(hours) + ' و ' + num2words.words(minutes) + ' دقیقه' + \
        (' و ' + num2words.words(seconds) + ' ثانیه' if seconds is not None else '')


def v3(hours, minutes, seconds, mode):
    if mode == 'PM':
        hours += 12
    if hours == 24:
        hours = 0

    if hours != 0:
        return num2words.words(hours) + ' و ' + num2words.words(minutes) + ' دقیقه' + \
               (' و ' + num2words.words(seconds) + ' ثانیه' if seconds is not None else '')
    else:
        return num2words.words(minutes) + ' دقیقه' + \
               (' و ' + num2words.words(seconds) + ' ثانیه' if seconds is not None else '') + ' نیمه شب'


def v4(hours, minutes, seconds, mode):
    if mode == 'AM' and hours > 12:
        hours -= 12

    return num2words.words(hours) + ' و ' + num2words.words(minutes) + ' دقیقه' + \
        (' و ' + num2words.words(seconds) + ' ثانیه' if seconds is not None else '') + \
        (' ' + 'بعد از ظهر' if mode == 'PM' else 'قبل از ظهر')


@words.register(str)
def _(
        time: str,
        random_result=False
) -> str:
    return find_time(time, random_result)


@words.register(list)
def _(
        time: list,
        random_result=False
) -> str:
    if len(time) == 1:
        return find_time(''.join(time), random_result)
    elif len(time) == 2 and \
            (re.search('AM|am|Am|aM', time[0]) is not None) or \
            (re.search('AM|am|Am|aM', time[1]) is not None) or \
            (re.search('PM|pm|Pm|pM', time[0]) is not None) or \
            (re.search('PM|pm|Pm|pM', time[1]) is not None) or \
            (re.search('بعد ازظهر|بعداز ظهر|بعد از ظهر|بعدازظهر', time[0]) is not None) or \
            (re.search('بعد ازظهر|بعداز ظهر|بعد از ظهر|بعدازظهر', time[1]) is not None) or \
            (re.search('قبل از ظهر|قبل ازظهر', time[0]) is not None) or \
            (re.search('قبل از ظهر|قبل ازظهر', time[1]) is not None) or \
            (re.search('دقیقه', time[0]) is not None) or \
            (re.search('دقیقه', time[1]) is not None):
        return find_time(''.join(time), random_result)
    raise TypeError('invalid input type for words function', time)
