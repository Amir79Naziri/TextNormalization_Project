from transformer.time2words import time2words
from random import randint, choice, random


def generate(n_sample=1):
    data = []
    for i in range(n_sample):
        type_ = choice(['PM', 'AM'])
        hour = str(randint(0, 12))
        minute = ':' + str(randint(0, 60))
        second = ''
        if random() > 0.5:
            second = ':' + str(randint(0, 60))

        data.append(time2words.words(hour + minute + second + ' ' + type_, random_result=True).strip() + '\n')


    return data



# if __name__ == '__main__':
#     print(generate(100))
