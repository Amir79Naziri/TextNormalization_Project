from transformer import currency2words
from transformer import date2words
from transformer import measurement2words
from transformer import num2words
from transformer import phone2words
from transformer import time2words
from transformer.phone2words import KEYWORDS
from transformer.punctuation2words import punctuation2words
import re


def part_normalizer(
        tokenized_text: list,
        max_seq: int,
        normalizer_module,
        reverse: bool = False,
        classifier=None,
        random_result: bool = False
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
                        result = normalizer_module.words([tokenized_text[i:i + counter][0][1:-1]],
                                                         random_result=random_result)
                        result = frame[0] + result + frame[1]
                    else:
                        result = normalizer_module.words(tokenized_text[i:i + counter],
                                                         random_result=random_result)
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
        tokenized_text: list,
        mode: str
) -> str:
    if mode == 'TTSv1' or 'TTSv2':
        random_result = False
    elif mode == 'STT':
        random_result = True
    else:
        raise TypeError('TTS or STT does not declared', mode)
    res = part_normalizer(tokenized_text, max_seq=5, normalizer_module=date2words, random_result=random_result)
    res = part_normalizer(res, max_seq=4, normalizer_module=time2words, reverse=True, random_result=random_result)
    res = part_normalizer(res, max_seq=1, normalizer_module=phone2words,
                          classifier=phone_classifier, random_result=random_result)
    res = part_normalizer(res, max_seq=2, normalizer_module=currency2words, random_result=random_result)
    res = part_normalizer(res, max_seq=3, normalizer_module=measurement2words, random_result=random_result)
    res = part_normalizer(res, max_seq=1, normalizer_module=num2words, random_result=random_result)
    res = re.sub(r'\s+', ' ', ' '.join(res)).strip()

    normalized = ''

    for c in res:
        normalized += punctuation2words.words(c, mode)

    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


if __name__ == '__main__':
    txt = input().split()
    print(normalize(txt, 'TTSv2'))
