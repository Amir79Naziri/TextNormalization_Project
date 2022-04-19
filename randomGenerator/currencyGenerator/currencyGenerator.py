from transformer.currency2words import currency2words
from random import randint, random, choices

CURRENCIES = [
    '£',
    '€',
    'ریال',
    'تومان',
    '$'
]


def generate(n_sample=1):
    data = []
    for i in range(n_sample):
        currency = choices(CURRENCIES, k=1, weights=(0.2, 0.2, 0.2, 0.2, 0.2))[0]
        if currency == 'تومان' or currency == 'ریال':
            i = int((10 * random()) * \
                choices([1, 10, 100, 1000, 10000, 100000, 1000000,
                         10000000, 100000000, 1000000000, 10000000000, 100000000000,
                         1000000000000], k=1,
                        weights=(0.02, 0.02, 0.05, 0.1, 0.13, 0.1, 0.1, 0.1, 0.1, 0.1, 0.07, 0.07, 0.04))[0])
            data.append(currency2words.words(str(i) + currency, random_result=True).strip() + '\n')

        else:
            i = (randint(1, 10) + random()) * \
                choices([1, 10, 100, 1000, 10000, 100000, 1000000,
                         10000000, 100000000, 1000000000, 10000000000, 100000000000,
                         1000000000000], k=1,
                        weights=(0.02, 0.02, 0.05, 0.1, 0.13, 0.1, 0.1, 0.1, 0.1, 0.1, 0.07, 0.07, 0.04))[0]
            data.append(currency2words.
                        words(str(i)[:str(i).index('.') + randint(1, 2) + 1] + \
                              currency, random_result=True).strip() + '\n')

    return data


# if __name__ == '__main__':
#     print(generate(100))
