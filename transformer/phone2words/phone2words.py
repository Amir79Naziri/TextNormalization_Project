from transformer.num2words import num2words
from typing import Union
from functools import singledispatch
import re

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
) -> str:
    raise TypeError('invalid input type for words function', time)


def find_phone(
        phone: str
) -> str:
    match = re.search(r'[+]', phone)
    if match is not None and match.start() == 0:
        phone = phone[1:]
    elif match is not None and match.end() == len(phone):
        phone = phone[:-1]

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


@words.register(str)
def _(
        phone: str,
) -> str:
    return find_phone(phone)


@words.register(list)
def _(
        phone: list,
) -> str:
    if len(phone) == 1:
        return find_phone(''.join(phone))
    else:
        raise TypeError('invalid input type for words function', phone)
