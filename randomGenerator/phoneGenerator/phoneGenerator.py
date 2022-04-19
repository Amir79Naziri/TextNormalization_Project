from transformer.phone2words import phone2words
from random import randint, random


def generate(n_sample=1):
    data = []
    for i in range(n_sample):

        if random() > 0.5:

            if random() > 0.7:
                phone = '09' + ''.join([str(randint(0, 9)) for _ in range(9)])
            else:
                phone = '0' + ''.join([str(randint(0, 9)) for _ in range(10)])
        else:
            phone = str(randint(1, 9)) + ''.join([str(randint(0, 9)) for _ in range(7)])

        data.append(phone2words.words(phone, random_result=True).strip() + '\n')

    return data

# if __name__ == '__main__':
#     print(generate(100))
