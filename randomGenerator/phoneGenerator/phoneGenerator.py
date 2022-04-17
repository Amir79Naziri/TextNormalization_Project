from transformer.phone2words import phone2words
from random import randint, random


def generate(n_sample=1):
    data = []
    for i in range(n_sample):

        if random() > 0.5:
            phone = '0' + ''.join([str(randint(0, 9)) for _ in range(10)])
        else:
            phone = ''.join([str(randint(0, 9)) for _ in range(8)])

        data.append(phone2words.words(phone, random_result=True).strip() + '\n')

    return data

# if __name__ == '__main__':
#     print(generate(100))
