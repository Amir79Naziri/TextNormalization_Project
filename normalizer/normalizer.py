from transformer import currency2words
from transformer import date2words
from transformer import measurement2words
from transformer import num2words
from transformer import phone2words
from transformer import time2words
from transformer.phone2words import KEYWORDS
import re


def part_normalizer(
        tokenized_text: list,
        max_seq: int,
        normalizer_module,
        reverse: bool = False,
        classifier=None
) -> list:
    if reverse:
        counter = max_seq
    else:
        counter = 1

    while (counter <= max_seq and not reverse) or (counter >= 1 and reverse):
        change_list = []
        remove_list = []

        for i in range(len(tokenized_text)):
            try:
                if i + counter <= len(tokenized_text):

                    if classifier is not None and not classifier(i, tokenized_text):
                        raise TypeError('invalid input type for words function', tokenized_text[i:i + counter])
                    frame = None
                    if counter == 1:
                        if tokenized_text[i:i + counter][0][0] == '(' and tokenized_text[i:i + counter][0][-1] == ')':
                            frame = ('(', ')')

                        elif tokenized_text[i:i + counter][0][0] == '[' and tokenized_text[i:i + counter][0][-1] == ']':
                            frame = ('[', ']')

                        elif tokenized_text[i:i + counter][0][0] == '{' and tokenized_text[i:i + counter][0][-1] == '}':
                            frame = ('{', '}')

                    if counter == 1 and frame is not None:
                        result = normalizer_module.words([tokenized_text[i:i + counter][0][1:-1]])
                        result = frame[0] + result + frame[1]
                    else:
                        result = normalizer_module.words(tokenized_text[i:i + counter])
                    change_list.append((i, result))
                    if counter > 1:
                        remove_list.extend(list(range(i + 1, i + counter)))
                    i += (counter - 1)

            except TypeError:
                pass

        for ind, val in change_list:
            tokenized_text[ind] = val

        new_tokenized_text = []
        for i in range(len(tokenized_text)):
            if not (i in remove_list):
                new_tokenized_text.append(tokenized_text[i])
        tokenized_text = new_tokenized_text
        if reverse:
            counter -= 1
        else:
            counter += 1

    return tokenized_text


def phone_classifier(
        index: int,
        tokenized_text: list,
        domain: int = 4
) -> bool:
    if len(tokenized_text[index]) < 8:
        return False
    for i in range(max(0, index - domain), min(index + domain + 1, len(tokenized_text) - 1)):
        if re.search('|'.join(KEYWORDS), tokenized_text[i]) is not None:
            return True
    else:
        return False


def normalize(
        tokenized_text: list
) -> str:
    res = part_normalizer(tokenized_text, max_seq=5, normalizer_module=date2words)
    res = part_normalizer(res, max_seq=2, normalizer_module=time2words, reverse=True)
    res = part_normalizer(res, max_seq=1, normalizer_module=phone2words, reverse=True, classifier=phone_classifier)
    res = part_normalizer(res, max_seq=2, normalizer_module=currency2words)
    res = part_normalizer(res, max_seq=2, normalizer_module=measurement2words)
    res = part_normalizer(res, max_seq=1, normalizer_module=num2words)
    normalized = re.sub(r'\s+', ' ', ' '.join(res)).strip()
    return normalized


if __name__ == '__main__':
    txt = input().split()
    print(normalize(txt))
