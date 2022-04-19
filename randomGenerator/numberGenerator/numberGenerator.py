from transformer.num2words import num2words
from random import randint, random, choices


def generate(n_sample=1):
    data = []
    for i in range(n_sample):
        if choices(['float', 'int'], k=1, weights=(0.4, 0.6))[0] == 'float':
            i = (randint(-10, 10) + random()) * \
                choices([1, 10, 100, 1000, 10000], k=1, weights=(0.5, 0.2, 0.1, 0.1, 0.1))[0]
            data.append(num2words.words(str(i)[:str(i).index('.') + randint(1, 3) + 1], random_result=True).strip() + '\n')

        else:
            if random() >= 0.8:
                i = int((randint(-10, 10) * random()) * \
                    choices([1, 10, 100, 1000, 10000], k=1, weights=(0.4, 0.3, 0.2, 0.08, 0.02))[0])
                data.append(num2words.words(str(i), random_result=True).strip() + '\n')
            else:
                i = int((randint(-10, 10) * random()) * \
                    choices([1, 10, 100, 1000, 10000], k=1, weights=(0.5, 0.3, 0.1, 0.08, 0.02))[0])
                power = (randint(-10, 10)) * \
                    choices([1, 10, 100, 1000, 10000], k=1, weights=(0.5, 0.3, 0.1, 0.08, 0.02))[0]
                data.append(num2words.words(str(i) + 'e' + str(power), random_result=True).strip() + '\n')

    return data



# if __name__ == '__main__':
#     print(generate(1000))
