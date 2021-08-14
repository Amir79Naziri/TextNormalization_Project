from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re
import random

KEYWORDS = [
    'تماس',
    'پیام',
    'ارسال',
    'شماره',
    'زنگ',
    'پیامک',
    'sms',
    'کال',
    'مسیج',
    'تلفن',
    'موبایل',
    'فکس',
    'سریال'
]


@singledispatch
def words(
        time: Union[str, list],
        random_result: bool = False
) -> str:
    raise TypeError('invalid input type for words function', time)


def find_phone(
        phone: str,
        random_result: bool = False
) -> str:
    if len(re.findall(r'-', phone)) > 1:
        parts = phone.split('-')
        if not random_result:
            return 'خط تیره'.join([v1(i) for i in parts])
        else:
            output = list()
            for i in parts:
                rand = random.randint(1, 2)
                if rand == 1:
                    output.append(v1(i))
                else:
                    output.append(v2(i))
            return 'خط تیره'.join(output)

    else:
        match = re.search(r'[+]', phone)
        if match is not None and match.start() == 0:
            phone = phone[1:]
        elif match is not None and match.end() == len(phone):
            phone = phone[:-1]

        if not random_result:
            return v1(phone)
        else:
            rand = random.randint(1, 3)
            if rand == 1 or rand == 2:
                return v1(phone)
            else:
                return v2(phone)


def v2(phone):
    index = 0
    output = ''
    while index < len(phone):
        if phone[index] == '0':
            output += ' صفر'
            index += 1
        else:
            if index + 3 <= len(phone) and phone[index:index + 3].isdigit():
                output += ' ' + num2words.words(phone[index:index + 3])
                index += 3
            elif index + 2 <= len(phone) and phone[index:index + 2].isdigit():
                output += ' ' + num2words.words(phone[index:index + 2])
                index += 2
            elif index + 1 <= len(phone) and phone[index:index + 1].isdigit():
                output += ' ' + num2words.words(phone[index:index + 1])
                index += 1
            else:
                raise TypeError('invalid input type for words function', phone)

    return output


def v1(phone):
    index = 0
    mod = 2
    output = ''
    while index < len(phone):
        if len(phone) - index == 3:
            mod = 3
        elif len(phone) - index == 2:
            mod = 2

        if phone[index] == '0':
            output += ' صفر'
            index += 1
            mod = 3

        else:
            if mod == 2 and index + 2 <= len(phone) and phone[index:index + 2].isdigit():
                output += ' ' + num2words.words(phone[index:index + 2])
                index += 2
            elif mod == 3 and index + 3 <= len(phone) and phone[index:index + 3].isdigit():
                output += ' ' + num2words.words(phone[index:index + 3])
                index += 3
                mod = 2
            elif index + 1 <= len(phone) and phone[index:index + 1].isdigit():
                output += ' ' + num2words.words(phone[index:index + 1])
                index += 1
            else:
                raise TypeError('invalid input type for words function', phone)

    return output


@words.register(str)
def _(
        phone: str,
        random_result: bool = False
) -> str:
    return find_phone(phone, random_result)


@words.register(list)
def _(
        phone: list,
        random_result: bool = False
) -> str:
    if len(phone) == 1:
        return find_phone(''.join(phone), random_result)
    else:
        raise TypeError('invalid input type for words function', phone)
