import sys
from normalizer import normalizer


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


def text_normalizer(input_filename, output_filename, *args):
    lines = _file_reader(input_filename)
    result = list()
    for line in lines:
        normalized = normalizer.normalize(line, args)
        if sum(normalized[1].values()) != 0:
            result.append(normalized[0] + '\n')
    _file_writer(output_filename, result)


if __name__ == '__main__':
    text_normalizer(sys.argv[1], sys.argv[2], sys.argv[3:])
