from typing import Union
from functools import singledispatch
from transformer.num2words import num2words
import re
import random

MEASUREMENTS = {
    'g': 'گرم',
    'G': 'گرم',
    'گرم': 'گرم',
    'A': 'آمپر',
    'آمپر': 'آمپر',
    'N': 'نیوتن',
    'نیوتن': 'نیوتن',
    'Hz': 'هرتز',
    'hz': 'هرتز',
    'هرتز': 'هرتز',
    'H': 'هانری',
    'h': 'هانری',
    'هانری': 'هانری',
    'Ω': 'اهم',
    'اهم': 'اهم',
    '°F': 'درجه فارنهایت',
    '°f': 'درجه فارنهایت',
    'درجه فارنهایت': 'درجه فارنهایت',
    'F': 'فاراد',
    'f': 'فاراد',
    'فاراد': 'فاراد',
    '°C': 'درجه سانتی گراد',
    '°c': 'درجه سانتی گراد',
    'درجه سانتی گراد': 'درجه سانتی گراد',
    'W': 'وات',
    'w': 'وات',
    'وات': 'وات',
    'J': 'ژول',
    'j': 'ژول',
    'ژول': 'ژول',
    'Pa': 'پاسکال',
    'pa': 'پاسکال',
    'پاسکال': 'پاسکال',
    'C': 'کلمب',
    'c': 'کلمب',
    'کلمب': 'کلمب',
    'T': 'تسلا',
    't': 'تسلا',
    'تسلا': 'تسلا',
    's': 'ثانیه',
    'S': 'ثانیه',
    'ثانیه': 'ثانیه',
    'mol': 'مول',
    'Mol': 'مول',
    'mOl': 'مول',
    'moL': 'مول',
    'MOl': 'مول',
    'MoL': 'مول',
    'mOL': 'مول',
    'MOL': 'مول',
    'مول': 'مول',
    'm': 'متر',
    'M': 'متر',
    'متر': 'متر',
    'K': 'کلوین',
    'k': 'کلوین',
    'کلوین': 'کلوین'
}
PREFIX = {
    'T': 'ترا',
    'ترا': 'ترا',
    'G': 'گیگا',
    'گیگا': 'گیگا',
    'M': 'مگا',
    'مگا': 'مگا',
    'k': 'کیلو',
    'K': 'کیلو',
    'کیلو': 'کیلو',
    'Y': 'یوتا',
    'یوتا': 'یوتا',
    'Z': 'زتا',
    'زتا': 'زتا',
    'E': 'اگزا',
    'اگزا': 'اگزا',
    'P': 'پتا',
    'پتا': 'پتا',
    'h': 'هکتو',
    'هکتو': 'هکتو',
    'da': 'دکا',
    'دکا': 'دکا',
    'y': 'یوکتو',
    'یوکتو': 'یوکتو',
    'z': 'زپتو',
    'زپتو': 'زپتو',
    'a': 'اتو',
    'اتو': 'اتو',
    'f': 'فمتو',
    'فمتو': 'فمتو',
    'p': 'پیکو',
    'پیکو': 'پیکو',
    'n': 'نانو',
    'نانو': 'نانو',
    'μ': 'میکرو',
    'میکرو': 'میکرو',
    'm': 'میلی',
    'میلی': 'میلی',
    'c': 'سانتی',
    'سانتی': 'سانتی',
    'd': 'دسی',
    'دسی': 'دسی'
}


# +12 kg
# -3.5 MG
# 280.1Kg
# -18 kg
# -12 daHz

@singledispatch
def words(
        measure: Union[str, list],
        random_result: bool = False
) -> str:
    raise TypeError('invalid input type for words function', measure)


def find_measurement(
        measure: str,
        random_result: bool = False
) -> str:
    match = re.search(r'[-+]?\d+e[-+]?\d*\.\d+|[-+]?\d+e[-+]?\d+|[-+]?\d+/[-+]?\d+|\d*\.\d+-|'
                      r'[-+]?\d*\.\d+|\d+-|[-+]?\d+', measure)
    if match is not None:
        number = match.group()
        while match is not None:
            measure = re.sub(number, '', measure)
            match = re.search(r'[-+]?\d+e[-+]?\d*\.\d+|[-+]?\d+e[-+]?\d+|[-+]?\d+/[-+]?\d+|[-+]?\d*\.\d+|[-+]?\d+',
                              measure)

        for meas in MEASUREMENTS:
            match = re.search(meas, measure)
            if match is None:
                continue

            measurement = match.group()
            measure = measure[:match.start()] + measure[match.end():]
            for pre in PREFIX:
                match = re.search(pre, measure)
                if match is None:
                    continue
                prefix = match.group()
                if not random_result:
                    return num2words.words(number) + \
                           ' ' + PREFIX[prefix] + ' ' + MEASUREMENTS[measurement]
                else:
                    return random_v(number, measurement, prefix)

            if not random_result:
                return num2words.words(number) + ' ' + MEASUREMENTS[measurement]
            else:
                return random_v(number, measurement)
    raise TypeError('invalid input type for words function', measure)


def random_v(number, measurement, prefix=None):
    positive = ''
    negative = random.choice(['منفی ', 'منهای '])
    decimal = random.choice([(1, ' و '), (0, ' ممیز '), (1, ' ممیز ')])
    decimal_separator = decimal[1]
    mode = decimal[0]
    fraction = random.choice([(True, ' '), (False, ' تقسیم بر ')])
    scientific_separator = random.choice([' در ده به توان ', ' ضربدر ده به قوهٔ ', ' ضربدر ده به توان ',
                                          ' در ده به نمای '])
    if prefix is None:
        return num2words.words(number, positive=positive, negative=negative, mode=mode,
                               decimal_separator=decimal_separator, scientific_separator=scientific_separator,
                               fraction_separator=fraction[1], ordinal_denominator=fraction[0]) + \
               ' ' + MEASUREMENTS[measurement]
    else:
        return num2words.words(number, positive=positive, negative=negative, mode=mode,
                               decimal_separator=decimal_separator, scientific_separator=scientific_separator,
                               fraction_separator=fraction[1], ordinal_denominator=fraction[0]) + \
               ' ' + PREFIX[prefix] + ' ' + MEASUREMENTS[measurement]


@words.register(str)
def _(
        measure: str,
        random_result: bool = False
) -> str:
    return find_measurement(measure, random_result=random_result)


@words.register(list)
def _(
        measure: list,
        random_result: bool = False
) -> str:
    if 1 <= len(measure) <= 3:
        return find_measurement(''.join(measure), random_result=random_result)
    raise TypeError('invalid input type for words function', measure)
