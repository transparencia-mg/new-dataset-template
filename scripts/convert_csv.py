import os
import pandas as pd
import re
from unidecode import unidecode
import config

def find_all_files():
    upload_files = os.listdir('upload')
    for file in upload_files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            abas = config.abas.get(file)
            if abas:
                for aba in abas:
                    convert_csv(file, aba)
            else:
                convert_csv(file)

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
    # import ipdb; ipdb.set_trace(context=10)
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
