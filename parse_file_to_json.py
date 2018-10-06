import sys
import pandas as pd


def parse_banamex(file_name):
    # destination_name = file_name.replace('.txt', '.json')
    print(pd.read_csv(file_name).to_json(orient='records'))


def parse_farmacias_ahorro(file_name):
    destination_name = file_name.replace('.csv', '.json')
    pd.read_csv(file_name, encoding="latin1").to_json(destination_name, orient='records')


def get_parser(file_source):
    if file_source == 'banamex':
        return parse_banamex
    if file_source == 'farmaciasAhorro':
        return parse_farmacias_ahorro()


def get_file_source(file_name):
    if 'Banamex' in file_name:
        return 'banamex'
    if 'FAhorro' in file_name:
        return 'farmaciasAhorro'


def main(file_name):
    file_source = get_file_source(file_name)
    parser = get_parser(file_source)

    parser(file_name)


if __name__ == '__main__':
    file_name = sys.argv[1]
    main(file_name)
