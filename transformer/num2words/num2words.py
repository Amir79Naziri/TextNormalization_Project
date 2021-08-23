from decimal import Decimal
from fractions import Fraction
from functools import singledispatch
from itertools import chain
from typing import Union
import re
import random

ONES = [
    '',
    'یک',
    'دو',
    'سه',
    'چهار',
    'پنج',
    'شش',
    'هفت',
    'هشت',
    'نه',
]

TENS = [
    '',
    '',
    'بیست',
    'سی',
    'چهل',
    'پنجاه',
    'شصت',
    'هفتاد',
    'هشتاد',
    'نود',
]

TEN_TO_TWENTY = [
    'ده',
    'یازده',
    'دوازده',
    'سیزده',
    'چهارده',
    'پانزده',
    'شانزده',
    'هفده',
    'هجده',
    'نوزده',
]

HUNDREDS = [
    '',
    'یکصد',
    'دویست',
    'سیصد',
    'چهارصد',
    'پانصد',
    'ششصد',
    'هفتصد',
    'هشتصد',
    'نهصد',
]

CLASSES = [
    '',
    ' هزار',
    ' میلیون',
    ' میلیارد',
    ' بیلیون',
    ' بیلیارد',
    ' تریلیون',
    ' ترلیارد',
    ' کوآدریلیون',
    ' کادریلیارد',
    ' کوینتیلیون',
    ' کوانتینیارد',
]

DECIMAL_PLACES = ['', ' دهم', ' صدم']
DECIMAL_PLACES.extend(chain.from_iterable(
    (i, ' ده' + i, ' صد' + i)
    for i in (i + 'م' for i in CLASSES[1:])
))

_NORMALIZATION_TABLE = str.maketrans('E٫', 'e.', '_٬,+')


def _three_digit_words(
        number: int
) -> str:
    """Return the word representation of 0 < number < 1000."""
    h, t, o = number // 100, number % 100 // 10, number % 10
    if h == 0 or (t == o == 0):
        w = HUNDREDS[h]
    else:
        w = HUNDREDS[h] + ' و '
    if t == 1:
        return w + TEN_TO_TWENTY[o]
    if o == 0 or t == 0:
        w += TENS[t]
    else:
        w += TENS[t] + ' و '
    return w + ONES[o]


def words(
        number: Union[int, float, str, list, Decimal, Fraction],
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
        mode: int = 1,
        random_result: bool = False
) -> str:
    if isinstance(number, list):
        if len(number) == 1:
            number = ''.join(number)
        else:
            raise TypeError('invalid input type for words function', number)

    if random_result:
        positive = ''
        negative = random.choice(['منفی ', 'منهای '])
        decimal = random.choice([(1, ' و '), (0, ' ممیز '), (1, ' ممیز ')])
        decimal_separator = decimal[1]
        mode = decimal[0]
        fraction = random.choice([(True, ' '), (False, ' تقسیم بر ')])
        fraction_separator = fraction[1]
        ordinal_denominator = fraction[0]
        scientific_separator = random.choice([' در ده به توان ', ' ضربدر ده به قوهٔ ', ' ضربدر ده به توان ',
                                              ' در ده به نمای '])
    if isinstance(number, str):
        number_ = re.findall(r'[-+]?\d+e[-+]?\d+|[-+]?\d+/[-+]?\d+|\d*\.\d+-|[-+]?\d*\.\d+|\d+-|[-+]?\d+', number)

        if len(number_) == 0:
            raise TypeError('invalid input type for words function', number)
        for n in number_:
            index = number.index(n)
            if re.match(r'\d*\.\d+-', n) is not None or re.match(r'\d+-', n) is not None:
                n = '-' + str(n)[:-1]

            res = __words(n, positive=positive, negative=negative, decimal_separator=decimal_separator,
                          fraction_separator=fraction_separator, ordinal_denominator=ordinal_denominator,
                          scientific_separator=scientific_separator, mode=mode)
            number = number[:index] + ' ' + res + ' ' + number[index + len(n):]
        return number
    else:
        return __words(number, positive=positive, negative=negative, decimal_separator=decimal_separator,
                       fraction_separator=fraction_separator, ordinal_denominator=ordinal_denominator,
                       scientific_separator=scientific_separator, mode=mode)


# noinspection PyUnusedLocal
@singledispatch
def __words(
        number: Union[int, float, str, Decimal, Fraction],
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
        mode: int = 1
) -> str:
    """Return the word form of number.

    If input is a string it should be in the form of a valid Python
    representation for one of the other accepted types. The only exceptions are
    that digits can be in Persian, for example words('۴۲') is valid.

    """
    raise TypeError('invalid input type for words function', number)


@__words.register(str)
@__words.register(Decimal)
def _(
        number: str,
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
        mode: int = 1
) -> str:
    # Normalize the str
    number = str(number).strip().translate(_NORMALIZATION_TABLE)

    # sign
    c0 = number[0]
    if c0 == '-':
        sign = negative
        number = number[1:]
    elif c0 == '0':
        sign = ''
    else:
        sign = positive

    numerator, e, denominator = number.partition('/')

    if denominator:
        if ordinal_denominator:
            return (
                    sign
                    + _natural_words(numerator)
                    + fraction_separator
                    + ordinal_words(denominator)
            )
        return (
                sign
                + _natural_words(numerator)
                + fraction_separator
                + _natural_words(denominator)
        )
    return sign + _exp_words(
        numerator, positive, negative, decimal_separator, scientific_separator, mode=mode
    )


# noinspection PyUnusedLocal
@__words.register(Fraction)
def _(
        number: Fraction,
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
        mode: int = 1
) -> str:
    numerator = number.numerator
    if numerator < 0:
        sign = negative
        numerator = str(numerator)[1:]
    else:
        sign = positive
        numerator = str(numerator)
    if ordinal_denominator:
        return (
                sign
                + _natural_words(numerator)
                + fraction_separator
                + ordinal_words(number.denominator)  # denominator has no sign
        )
    return (
            sign
            + _natural_words(numerator)
            + fraction_separator
            + _natural_words(str(number.denominator))  # denominator has no sign
    )


# noinspection PyUnusedLocal
@__words.register(int)
def _(
        number: int,
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
        mode: int = 1
) -> str:
    """Return the fa-word form for the given int."""
    if number == 0:
        return 'صفر'
    if number < 0:
        return negative + _natural_words(str(number)[1:])
    return positive + _natural_words(str(number))


# noinspection PyUnusedLocal
@__words.register(float)
def _(
        number: float,
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
        mode: int = 1
) -> str:
    """Return the fa-word form for the given float."""
    if number == 0:
        return 'صفر'
    str_num = str(number)
    if number < 0:
        return negative + _exp_words(
            str_num[1:],
            positive,
            negative,
            decimal_separator,
            scientific_separator,
            mode=mode
        )
    return positive + _exp_words(
        str_num, positive, negative, decimal_separator, scientific_separator, mode=mode
    )


def _exp_words(
        number: str,
        positive: str,
        negative: str,
        decimal_separator: str,
        scientific_separator: str,
        mode: int = 1
) -> str:
    # exponent
    base, e, exponent = number.partition('e')
    if exponent:
        return (
                _point_words(base, decimal_separator=decimal_separator, mode=mode)
                + scientific_separator
                + __words(int(exponent), positive, negative)
        )
    return _point_words(base, decimal_separator=decimal_separator, mode=mode)


def _point_words(
        number: str,
        decimal_separator: str,
        mode: int = 1
) -> str:
    before_p, p, after_p = number.partition('.')
    if after_p:
        if before_p == '0':
            if after_p == '0':
                return 'صفر'
            if mode == 0:
                return _natural_words(after_p)
            else:
                return _natural_words(after_p) + DECIMAL_PLACES[len(after_p)]
        if after_p != '0':
            if mode == 0:
                return (
                        _natural_words(before_p)
                        + decimal_separator
                        + _natural_words(after_p)
                )
            else:
                return (
                        _natural_words(before_p)
                        + decimal_separator
                        + _natural_words(after_p)
                        + DECIMAL_PLACES[len(after_p)]
                )
        return _natural_words(before_p)
    return _natural_words(before_p)


def _natural_words(
        str_num: str
) -> str:
    if str_num == '0':
        return 'صفر'
    length = len(str_num)
    if length > len(CLASSES) * 3:
        raise ValueError('out of range')

    modulo_3 = length % 3
    if modulo_3:
        str_num = '0' * (3 - modulo_3) + str_num
        length += 3 - modulo_3

    groups = length // 3
    group = groups
    natural_words = ''
    while group > 0:
        three_digit = str_num[group * 3 - 3:group * 3]
        word3 = _three_digit_words(int(three_digit))
        if word3 and group != groups:
            if natural_words:
                natural_words = word3 + CLASSES[groups - group] + \
                                ' و ' + natural_words
            else:
                natural_words = word3 + CLASSES[groups - group]
        else:
            natural_words = word3 + natural_words
        group -= 1

    return natural_words


def ordinal_words(
        number: Union[int, str],
        positive: str = '',
        negative: str = 'منفی ',
) -> str:
    """Return the number converted to ordinal words form."""
    w = __words(int(number), positive, negative)
    if w[-2:] == 'سه':
        return w[:-2] + 'سوم'
    return w + 'م'


def change_defaults(
        positive: str = '',
        negative: str = 'منفی ',
        decimal_separator: str = ' و ',
        fraction_separator: str = ' ',
        ordinal_denominator: bool = True,
        scientific_separator: str = ' در ده به توان ',
):
    """The the default values for words and ordinal_words functions."""
    defaults = (
        positive, negative, decimal_separator, fraction_separator,
        ordinal_denominator, scientific_separator,
    )
    change_defaults.__defaults__ = defaults
    for func in __words.registry.values():
        func.__defaults__ = defaults
    ordinal_words.__defaults__ = (positive, negative)
