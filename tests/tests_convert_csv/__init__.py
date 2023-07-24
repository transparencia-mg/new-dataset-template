import os
import requests

files = [
    {
        'org_repo': 'transparencia-mg/crimes-violentos',
        'file_base_path': 'upload/crimes_violentos_2022.xlsx',
        'ref': '3d4df3461994e9762b3e9fd22d1f90fbb899ee8c',
    },
]

def get_excel_files():
    if not os.path.exists('tests/temp'):
       os.mkdir('tests/temp')
    # import ipdb; ipdb.set_trace(context=10)
    for file in files:
        file_name = file["file_base_path"].split('/')[-1]
        file_path = f'https://api.github.com/repos/{file["org_repo"]}/contents/{file["file_base_path"]}?ref={file["ref"]}'
        data = requests.get(file_path, headers={'Accept': 'application/vnd.github.v3.raw'})
        with open(f'tests/temp/{file_name}', 'wb') as f:
            f.write(data.content)

get_excel_files()
