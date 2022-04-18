from transformer.date2words import date2words
from random import randint, choice, random


def generate(n_sample=1):
    data = []
    for i in range(n_sample):
        type_ = choice([True, False])
        if type_:
            year = str(randint(1000, 1499))
        else:
            year = str(randint(1500, 2099))

        month = str(randint(1, 12))
        day = str(randint(1, 31))

        data.append(date2words.words(year + '.' + month + '.' + day, IR=type_, random_result=True).strip() + '\n')


    return data



if __name__ == '__main__':
    print(generate(100))
    # print(date2words.words('2020.11.02', IR=True, random_result=True))