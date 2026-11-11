from dotenv import load_dotenv
import copy
import os
import re

import yaml
from frictionless import describe

load_dotenv()

DATASET_DIR = 'dataset'
YAML_PATH = f'{DATASET_DIR}/datapackage.yaml'
PLACEHOLDER_TITLE = 'Insira um título humanamente legível para este recurso.'
PLACEHOLDER_DESCRIPTION = 'Insira a descrição/explicação detalhada deste recurso.'
CHAVES_VOLATEIS = ('hash', 'bytes', 'stats')


class IndentDumper(yaml.SafeDumper):
    # Mantém listas indentadas como o frictionless grava, para o diff ficar limpo
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def create_datapackage_yaml():
    dataset_files = os.listdir(DATASET_DIR)
    if 'datapackage.yaml' not in dataset_files:
        package = describe('./data', type='package', basepath=f'./{DATASET_DIR}')
        package['name'] = os.getenv("DATASET_NAME")
        package['title'] = ' '.join(os.getenv("DATASET_NAME").split('-')).capitalize()
        package['owner_org'] = os.getenv("OWNER_ORG")
        for resource in package.resources:
            resource['description'] = PLACEHOLDER_DESCRIPTION
            resource['title'] = PLACEHOLDER_TITLE
        package.to_yaml(YAML_PATH)
    else:
        sincronizar_recursos()


# ---------------------------------------------------------------- utilitários

def normalizar_path(path):
    path = (path or '').replace('\\', '/')
    while path.startswith('./'):
        path = path[2:]
    return path


def nomes_campos(schema):
    if not isinstance(schema, dict):
        return []
    return [f.get('name') for f in schema.get('fields', [])]


def esqueleto(nome):
    """'estagiarios_2026_01' -> 'estagiarios_#_#'. Nomes com o mesmo esqueleto
    pertencem à mesma série (ano, mês, versão, número de aba...)."""
    return re.sub(r'\d+', '#', nome or '')


def trocas_numericas(nome_antigo, nome_novo):
    """Pares (antigo, novo) dos números que mudaram entre dois nomes da mesma série."""
    antigos = re.findall(r'\d+', nome_antigo)
    novos = re.findall(r'\d+', nome_novo)
    return [(a, n) for a, n in zip(antigos, novos) if a != n]


def aplicar_trocas(texto, trocas):
    if not isinstance(texto, str):
        return texto
    for antigo, novo in trocas:
        texto = re.sub(rf'(?<!\d){re.escape(antigo)}(?!\d)', novo, texto)
    return texto


def prefixo_comum(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


# ------------------------------------------------------------- recurso novo

def escolher_modelo(resources, nome, campos):
    """Procura um recurso existente para servir de base ao novo:
    1º) mesma série no nome (só números diferentes) e mesmas colunas;
    2º) mesmas colunas, qualquer nome (o mais parecido no nome);
    3º) mesma série no nome, colunas diferentes.
    Retorna (modelo, mesma_serie, mesmas_colunas)."""
    candidatos = []
    for r in resources:
        mesma_serie = esqueleto(r.get('name')) == esqueleto(nome)
        mesmas_colunas = bool(campos) and nomes_campos(r.get('schema')) == campos
        if not (mesma_serie or mesmas_colunas):
            continue
        prioridade = 3 if (mesma_serie and mesmas_colunas) else 2 if mesmas_colunas else 1
        candidatos.append((prioridade, prefixo_comum(r.get('name', ''), nome), r.get('name', ''), r))
    if not candidatos:
        return None, False, False
    _, _, _, modelo = max(candidatos, key=lambda c: c[:3])
    return (modelo,
            esqueleto(modelo.get('name')) == esqueleto(nome),
            nomes_campos(modelo.get('schema')) == campos)


def novo_recurso(path, nome, resources):
    descrito = describe(path, basepath=f'./{DATASET_DIR}').to_dict()
    for chave in CHAVES_VOLATEIS:
        descrito.pop(chave, None)
    campos = nomes_campos(descrito.get('schema'))

    modelo, mesma_serie, mesmas_colunas = escolher_modelo(resources, nome, campos)
    if modelo is None:
        descrito['title'] = PLACEHOLDER_TITLE
        descrito['description'] = PLACEHOLDER_DESCRIPTION
        return descrito, 'novo: preencher título e descrição'

    novo = copy.deepcopy(modelo)
    for chave in CHAVES_VOLATEIS:
        novo.pop(chave, None)
    novo['name'] = nome
    novo['path'] = path

    if mesma_serie:
        trocas = trocas_numericas(modelo['name'], nome)
        novo['title'] = aplicar_trocas(novo.get('title', nome), trocas)
        novo['description'] = aplicar_trocas(novo.get('description', ''), trocas)
    else:
        novo['title'] = PLACEHOLDER_TITLE
        novo['description'] = PLACEHOLDER_DESCRIPTION

    if mesmas_colunas:
        situacao = f'schema copiado de {modelo["name"]}'
    else:
        # Colunas mudaram: schema inferido do CSV novo, herdando a documentação
        # e o tipo das colunas que continuam existindo.
        doc = {f.get('name'): f for f in (modelo.get('schema') or {}).get('fields', [])}
        for campo in descrito.get('schema', {}).get('fields', []):
            antigo = doc.get(campo.get('name'))
            if antigo:
                for chave in ('title', 'description', 'type', 'format'):
                    if chave in antigo:
                        campo[chave] = antigo[chave]
        novo['schema'] = descrito.get('schema')
        if 'dialect' in descrito:
            novo['dialect'] = descrito['dialect']
        situacao = f'colunas diferentes de {modelo["name"]}, schema inferido: REVISAR'

    if not mesma_serie:
        situacao += '; preencher título e descrição'
    return novo, situacao


# ------------------------------------------------------- sincronização geral

def sincronizar_recursos():
    """Deixa o datapackage.yaml igual ao conteúdo de dataset/data:
    inclui CSVs novos e retira recursos cujo arquivo local foi excluído."""
    with open(YAML_PATH, encoding='utf-8') as f:
        package = yaml.safe_load(f) or {}

    resources = package.get('resources') or []
    csvs = sorted(f for f in os.listdir(f'{DATASET_DIR}/data') if f.lower().endswith('.csv'))

    # --- exclusões
    removidos = []
    if csvs:
        mantidos = []
        for r in resources:
            path = normalizar_path(r.get('path'))
            local = path and not path.startswith('http')
            if local and not os.path.exists(os.path.join(DATASET_DIR, path)):
                removidos.append(r.get('name', path))
            else:
                mantidos.append(r)
        resources = mantidos
    elif resources:
        print('ATENÇÃO: nenhum CSV em dataset/data. Por segurança, nenhum recurso foi '
              'retirado do datapackage.yaml.')

    # --- inclusões
    paths = {normalizar_path(r.get('path')) for r in resources}
    names = {r.get('name') for r in resources}
    incluidos = []
    for csv in csvs:
        path = f'data/{csv}'
        nome = csv[:-4]
        if path in paths or nome in names:
            continue
        recurso, situacao = novo_recurso(path, nome, resources)
        resources.append(recurso)
        incluidos.append(f'{nome} ({situacao})')

    if not (removidos or incluidos):
        print('datapackage.yaml já está igual a dataset/data.')
        return

    package['resources'] = resources
    with open(YAML_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(package, f, Dumper=IndentDumper, allow_unicode=True, sort_keys=False)
    for nome in removidos:
        print(f'Recurso retirado do datapackage.yaml (arquivo excluído): {nome}')
    for item in incluidos:
        print(f'Recurso incluído no datapackage.yaml: {item}')


if __name__ == '__main__':
    create_datapackage_yaml()
