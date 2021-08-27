import sys
from normalizer import normalizer
from tqdm import tqdm
from tabulate import tabulate


def _file_reader(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
        lines = list()

        for i in range(len(raw_lines)):
            if i == len(raw_lines) - 1 and raw_lines[i][:-1] != '\n':
                lines.append(raw_lines[i].strip().split())
            else:
                lines.append(raw_lines[i][:-1].strip().split())

        return lines


def _file_writer(filename, result):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(result)


def _update_status_dict(total_status_dict, new_status_dict):
    for key in new_status_dict:
        total_status_dict[key] += new_status_dict[key]



def text_normalizer(input_filename, output_filename, *args):
    lines = _file_reader(input_filename)
    result = list()
    total_status_dict = {'date': 0, 'time': 0, 'phone and ID': 0, 'currency': 0,
                         'measurement': 0, 'number': 0, 'miscellaneous': 0, 'punctuation': 0}
    total_line = len(lines)

    counter = 0
    for line in tqdm(lines, colour='white'):
        normalized = normalizer.normalize(line, args)
        if sum(normalized[1].values()) != 0:
            counter += 1
            result.append(normalized[0] + '\n')
            _update_status_dict(total_status_dict, normalized[1])

    filtered_lines = total_line - counter
    _file_writer(output_filename, result)

    print(tabulate([[total_line, filtered_lines] + list(total_status_dict.values())],
                   headers=['total lines', 'filtered lines'] + list(total_status_dict.keys()), tablefmt="pretty"))


if __name__ == '__main__':
    text_normalizer(sys.argv[1], sys.argv[2], sys.argv[3:])
