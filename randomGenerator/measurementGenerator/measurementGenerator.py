from transformer.measurement2words import measurement2words
from random import randint, random, choices, choice

MEASUREMENTS = [
    'گرم',
    'آمپر',
    'نیوتن',
    'هرتز',
    'هانری',
    'اهم',
    'درجه فارنهایت',
    'فاراد',
    'درجه سانتی گراد',
    'وات',
    'ژول',
    'پاسکال',
    'کلمب',
    'تسلا',
    'ثانیه',
    'مول',
    'متر',
    'کلوین'
]

PREFIX = [
    'ترا',
    'گیگا',
    'مگا',
    'کیلو',
    'یوتا',
    'زتا',
    'اگزا',
    'پتا',
    'هکتو',
    'دکا',
    'یوکتو',
    'زپتو',
    'اتو',
    'فمتو',
    'پیکو',
    'نانو',
    'میکرو',
    'میلی',
    'سانتی',
    'دسی'
]


def generate(n_sample=1):
    data = []
    for i in range(n_sample):

        measurement = choice(MEASUREMENTS)
        prefix = ''
        if random() > 0.7:
            prefix = choice(PREFIX)

        if choices(['float', 'int'], k=1, weights=(0.4, 0.6))[0] == 'float':
            i = (randint(-10, 10) + random()) * \
                choices([1, 10, 100, 1000], k=1, weights=(0.4, 0.3, 0.2, 0.1))[0]
            data.append(
                measurement2words.words(str(i)[:str(i).index('.') + randint(1, 3) + 1] +
                                        prefix + ' ' + measurement, random_result=True).strip() + '\n')

        else:
            if random() >= 0.8:
                i = int((randint(-10, 10) * random()) * \
                    choices([1, 10, 100, 1000, 10000], k=1, weights=(0.4, 0.4, 0.1, 0.08, 0.02))[0])
                data.append(measurement2words.words(str(i) +
                                                    prefix + ' ' + measurement, random_result=True).strip() + '\n')
            else:
                i = int((randint(-10, 10) * random()) * \
                    choices([1, 10, 100, 1000, 10000], k=1, weights=(0.6, 0.3, 0.05, 0.03, 0.02))[0])
                power = (randint(-10, 10)) * \
                    choices([1, 10, 100, 1000, 10000], k=1, weights=(0.5, 0.3, 0.1, 0.08, 0.02))[0]
                data.append(measurement2words.words(str(i) + 'e' + str(power) +
                                                    prefix + ' ' + measurement, random_result=True).strip() + '\n')

    return data

# if __name__ == '__main__':
#     print(generate(100))
