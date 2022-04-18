from randomGenerator.numberGenerator import numberGenerator
from randomGenerator.currencyGenerator import currencyGenerator
from randomGenerator.measurementGenerator import measurementGenerator
from randomGenerator.timeGenerator import timeGenerator
from randomGenerator.phoneGenerator import phoneGenerator
from randomGenerator.dateGenerator import dateGenerator


def _file_writer(filename, result):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(result)


def generate(**kwargs):
    for key in kwargs:
        lines = []
        if key == 'number':
            lines = numberGenerator.generate(1000)
        elif key == 'currency':
            lines = currencyGenerator.generate(1000)
        elif key == 'measurement':
            lines = measurementGenerator.generate(1000)
        elif key == 'time':
            lines = timeGenerator.generate(1000)
        elif key == 'phone':
            lines = phoneGenerator.generate(1000)
        elif key == 'date':
            lines = dateGenerator.generate(1000)
        else:
            return
        _file_writer(kwargs[key], lines)


if __name__ == '__main__':
    generate(number='data/numbers.txt', currency='data/currency.txt',
             measurement='data/measurement.txt', time='data/time.txt',
             phone='data/phone.txt', date='data/date.txt')
