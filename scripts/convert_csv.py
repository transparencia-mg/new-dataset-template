import json
import os
import pandas as pd
import re
from unidecode import unidecode
import config

# Registro de quais CSVs foram gerados a partir de cada Excel da pasta upload.
# Serve para saber o que apagar quando um Excel (ou uma aba no config.py) sai.
# CSVs colocados direto em dataset/data, sem Excel, nunca são apagados por aqui.
MANIFESTO = 'dataset/.csv_gerados.json'


def find_all_files():
    gerados = {}
    upload_files = os.listdir('upload')
    for file in upload_files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            abas = config.abas.get(file)
            if abas:
                gerados[file] = [convert_csv(file, aba) for aba in abas]
            else:
                gerados[file] = [convert_csv(file)]
    remover_csvs_orfaos(gerados)


def remover_csvs_orfaos(gerados):
    anteriores = {}
    if os.path.exists(MANIFESTO):
        with open(MANIFESTO, encoding='utf-8') as f:
            anteriores = json.load(f)

    atuais = {csv for csvs in gerados.values() for csv in csvs}
    if getattr(config, 'remover_excluidos', True):
        for excel, csvs in anteriores.items():
            for csv in csvs:
                caminho = f'dataset/data/{csv}.csv'
                if csv not in atuais and os.path.exists(caminho):
                    os.remove(caminho)
                    print(f'Removido {caminho} (origem {excel} excluída do upload ou do config.py).')

    with open(MANIFESTO, 'w', encoding='utf-8') as f:
        json.dump(gerados, f, ensure_ascii=False, indent=2, sort_keys=True)


def convert_csv(file, aba=None):
    read_file = pd.read_excel (f'upload/{file}', aba)
    read_file = list(read_file.items())[0][1] if aba == None else read_file
    read_file = read_file \
                .replace('\n', ' ', regex=True) \
                .replace('\r', '', regex=True)
    columns = read_file.columns
    new_columns = []
    for column in columns:
        new_columns.append(snake_small_case(column))
    csv_name = file.split('.xls')[0]
    csv_name = csv_name if aba == None else f'{aba}' # to xlsx and xls
    read_file.columns=new_columns

    read_file.to_csv (f'dataset/data/{csv_name}.csv', \
                    index = None, \
                    header=True, \
                    sep = ';', \
                    decimal = ',', \
                    encoding = 'utf-8-sig', \
                    na_rep = ""\
                    )
    return csv_name

def snake_small_case(column):
  column_lower = column.lower()
  column_unidecode = unidecode(column_lower)
  column_alphanumeric = re.sub('[^A-Za-z0-9]+', ' ', column_unidecode)
  column_split = column_alphanumeric.split(' ')
  column_empty = [x for x in column_split if x != '']
  column = '_'.join(column_empty)
  return column

if __name__ == '__main__':
    find_all_files()
