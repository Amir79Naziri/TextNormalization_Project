from typing import Union
from functools import singledispatch
from transformer.num2words import num2words
import re

MEASUREMENTS = {
    'g': 'گرم',
    'G': 'گرم',
    'A': 'آمپر',
    'N': 'نیوتن',
    'Hz': 'هرتز',
    'hz': 'هرتز',
    'H': 'هانری',
    'h': 'هانری',
    'Ω': 'اهم',
    '°F': 'درجه فارنهایت',
    '°f': 'درجه فارنهایت',
    'F': 'فاراد',
    'f': 'فاراد',
    '°C': 'درجه سانتی گراد',
    '°c': 'درجه سانتی گراد',
    'W': 'وات',
    'w': 'وات',
    'J': 'ژول',
    'j': 'ژول',
    'Pa': 'پاسکال',
    'pa': 'پاسکال',
    'C': 'کلمب',
    'c': 'کلمب',
    'T': 'تسلا',
    't': 'تسلا',
    's': 'ثانیه',
    'S': 'ثانیه',
    'mol': 'مول',
    'Mol': 'مول',
    'mOl': 'مول',
    'moL': 'مول',
    'MOl': 'مول',
    'MoL': 'مول',
    'mOL': 'مول',
    'MOL': 'مول',
    'm': 'متر',
    'M': 'متر',
    'K': 'کلوین',
    'k': 'کلوین'
}

PREFIX = {
    'T': 'ترا',
    'G': 'گیگا',
    'M': 'مگا',
    'k': 'کیلو',
    'K': 'کیلو',
    'Y': 'یوتا',
    'Z': 'زتا',
    'E': 'اگزا',
    'P': 'پتا',
    'h': 'هکتو',
    'da': 'دکا',
    'y': 'یوکتو',
    'z': 'زپتو',
    'a': 'اتو',
    'f': 'فمتو',
    'p': 'پیکو',
    'n': 'نانو',
    'μ': 'میکرو',
    'm': 'میلی',
    'c': 'سانتی',
    'd': 'دسی'
}


# +12 kg
# -3.5 MG
# 280.1Kg
# -18 kg
# -12 daHz

@singledispatch
def words(
        measure: Union[str, list],
) -> str:
    raise TypeError('invalid input type for words function', measure)


def find_measurement(
        measure: str
) -> str:
    match = re.search(r'[-+]?\d+e[-+]?\d+|[-+]?\d+/[-+]?\d+|[-+]?\d*\.\d+|[-+]?\d+', measure)
    if match is not None:
        number = match.group()
        while match is not None:
            measure = measure[match.end():]
            match = re.search(r'[-+]?\d+e[-+]?\d+|[-+]?\d+/[-+]?\d+|[-+]?\d*\.\d+|[-+]?\d+', measure)

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

                return num2words.words(number, positive='مثبت ') + \
                    ' ' + PREFIX[prefix] + ' ' + MEASUREMENTS[measurement]

            return num2words.words(number, positive='مثبت ') + ' ' + MEASUREMENTS[measurement]
    raise TypeError('invalid input type for words function', measure)


@words.register(str)
def _(
        measure: str,
) -> str:
    return find_measurement(measure)


@words.register(list)
def _(
        measure: list,
) -> str:
    if 1 <= len(measure) <= 2:
        return find_measurement(''.join(measure))
    raise TypeError('invalid input type for words function', measure)
