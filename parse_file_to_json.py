import sys
import pandas as pd

fields = ['origen', 'donacionUnitaria', 'donacionMultiple', 'fecha', 'donativo', 'estado']


def display_data(string_data):
    print(string_data)


def parse_banamex(file_name):
    file_data = pd.read_csv(file_name)

    parsed_data = pd.DataFrame()

    parsed_data['fecha'] = file_data['Fecha']
    parsed_data['donativo'] = file_data['Monto'].apply(lambda x: x / 100)
    parsed_data['estado'] = file_data['Estado']

    parsed_data['origen'] = 'Banamex'
    parsed_data['donacionUnitaria'] = True
    parsed_data['donacionMultiple'] = None

    return parsed_data[fields].to_json(orient='records')


def parse_farmacias_ahorro(file_name):
    file_data = pd.read_csv(file_name, encoding="latin1")

    parsed_data = pd.DataFrame()

    parsed_data['fecha'] = file_data['Fecha y Hora']
    parsed_data['donativo'] = file_data['total']
    parsed_data['estado'] = file_data['plaza']

    parsed_data['origen'] = 'Farmacias del Ahorro'
    parsed_data['donacionUnitaria'] = False
    parsed_data['donacionMultiple'] = file_data['No. De Movimientos']

    return parsed_data.to_json(orient='records')


def parse_soriana(file_name):
    file_data = pd.read_csv(file_name, delimiter='|', encoding="utf-16le")[1:-1]

    parsed_data = pd.DataFrame()

    parsed_data['donativo'] = file_data['IMPORTE'].apply(pd.to_numeric)
    parsed_data['estado'] = file_data['TIENDA']

    parsed_data['fecha'] = file_data['FECHA'].apply(pd.to_datetime)

    parsed_data['origen'] = 'Soriana'
    parsed_data['donacionUnitaria'] = False
    parsed_data['donacionMultiple'] = file_data['DONADORES'].apply(pd.to_numeric)

    return parsed_data.to_json(orient='records')


def get_parser(file_source):
    if file_source == 'banamex':
        return parse_banamex
    if file_source == 'farmaciasAhorro':
        return parse_farmacias_ahorro
    if file_source == 'soriana':
        return parse_soriana


def get_file_source(file_name):
    if 'Banamex' in file_name:
        return 'banamex'
    if 'FAhorro' in file_name:
        return 'farmaciasAhorro'
    if 'Soriana' in file_name:
        return 'soriana'


def main(file_name):
    file_source = get_file_source(file_name)
    parser = get_parser(file_source)
    json_string_data = parser(file_name)
    display_data(json_string_data)


if __name__ == '__main__':
    file_name = sys.argv[1]
    main(file_name)
