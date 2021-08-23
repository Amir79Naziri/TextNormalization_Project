from transformer import currency2words
from transformer import date2words
from transformer import measurement2words
from transformer import num2words
from transformer import phone2words
from transformer import time2words
from transformer import punctuation2words
from transformer import miscellaneous2words
from transformer.punctuation2words import NEW_LINES
from transformer.phone2words import KEYWORDS
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
        *args,
        **kwargs,
) -> str:

    try:
        mode = kwargs['mode']
    except KeyError:
        mode = 'TTSv1'
    if mode == 'TTSv1' or 'TTSv2':
        random_result = False
    elif mode == 'STT':
        random_result = True
    else:
        raise TypeError('TTS or STT does not declared', mode)

    try:
        res = args[0]
        if not isinstance(res, list):
            raise Exception('tokenized text is not defined')
    except IndexError:
        raise Exception('tokenized text is not defined')


    date = time = phone = currency = measurement = number = miscellaneous = punctuation = False
    for i in range(1, len(args)):
        if isinstance(args[i], str):
            if 'date' in args[i] or '-d' in args[i]:
                date = True
            elif 'time' in args[i] or '-t' in args[i]:
                time = True
            elif 'phone' in args[i] or '-p' in args[i]:
                phone = True
            elif 'currency' in args[i] or '-c' in args[i]:
                currency = True
            elif 'measure' in args[i] or '-m' in args[i]:
                measurement = True
            elif 'number' in args[i] or '-n' in args[i]:
                number = True
            elif 'miscellaneous' in args[i] or '-mi' in args[i]:
                miscellaneous = True
            elif 'punctuation' in args[i] or '-pu' in args[i]:
                punctuation = True

    total = not(date or time or phone or currency or measurement or number or miscellaneous or punctuation)


    if total:
        date = time = phone = currency = measurement = number = miscellaneous = punctuation = True
    if date:
        res = part_normalizer(res, max_seq=5, normalizer_module=date2words,
                              random_result=random_result)
    if time:
        res = part_normalizer(res, max_seq=4, normalizer_module=time2words, reverse=True,
                              random_result=random_result)
    if phone:
        res = part_normalizer(res, max_seq=1, normalizer_module=phone2words,
                              classifier=phone_classifier, random_result=random_result)
    if currency:
        res = part_normalizer(res, max_seq=2, normalizer_module=currency2words,
                              random_result=random_result)
    if measurement:
        res = part_normalizer(res, max_seq=3, normalizer_module=measurement2words,
                              random_result=random_result)
    if number:
        res = part_normalizer(res, max_seq=1, normalizer_module=num2words,
                              random_result=random_result)
    if miscellaneous:
        res = part_normalizer(res, max_seq=2, normalizer_module=miscellaneous2words,
                              random_result=random_result)

    res = re.sub(r'\s+', ' ', ' '.join(res)).strip()

    if punctuation:
        normalized = ''
        for c in res:
            normalized += punctuation2words.words(c, mode)

        normalized = re.sub(r'\s+', ' ', normalized).strip()
        res = normalized

    return res


if __name__ == '__main__':
    txt = input().split()
    print(normalize(txt, 'date', mode='TTSv2'))
