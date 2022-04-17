from randomGenerator.numberGenerator import numberGenerator


def _file_writer(filename, result):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(result)


def generate(filenames):
    for filename in filenames:
        lines = numberGenerator.generate(1000)
        _file_writer(filename, lines)


if __name__ == '__main__':
    generate(['data.txt'])
