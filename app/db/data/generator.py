import lorem
from numpy.random import choice as np_choice
from random import choice as py_choice
import requests

from db.connection import Connection
from psycopg2.extensions import quote_ident

def generate_users(size: int = 2) -> list[dict]:
    response = requests.get(f'https://randomuser.me/api/?results={size}&nat=BR')
    response.raise_for_status()
    generated_users = response.json()
    users = [
        {
            'cpf': ''.join(map(str, np_choice(range(10), size=11))),
            'nome': user['name']['first'],
            'sobrenome': user['name']['last'],
            'email': user['email'],
            'cod_pais': '+55',
            'ddd': str(np_choice(range(10, 100))),
            'numero': str(py_choice(range(1000_0000, 9_9999_9999))),
            'senha': user['login']['password'],
            'endereco': (
                f"{user['location']['street']['name']}, {user['location']['street']['number']}, "
                f"{user['location']['city']}, {user['location']['state']}, {user['location']['country']}"
            ),
            'tipo': np_choice(['moderador', 'professor', 'monitor', 'aluno'], p=[0.091, 0.06, 0.219, 0.63]),
        } for user in generated_users['results']
    ]
    return users

def insert_users(users: list[dict], conn: Connection, commit: bool = True):
    columns: list[str] = ['cpf', 'nome', 'sobrenome', 'email', 'cod_pais',
                          'ddd', 'numero', 'senha', 'endereco', 'tipo']
    data = [tuple(user[column] for column in columns) for user in users]
    with conn.cursor(commit=commit) as cursor:
        cursor.executemany(
            f"insert into usuario({', '.join(columns)}) "
            f"values ({', '.join('%s' for _ in columns)})",
            data
        )


def update_user_types(conn: Connection, commit: bool = True):
    types: list[str] = ['moderador', 'professor', 'monitor', 'aluno']
    with conn.cursor(commit=commit) as cursor:
        for type_ in types:
            cursor.execute(
                f"insert into {type_} "
                "select cpf from usuario where tipo = %s;",
                [type_]
            )

def generate_comments(size: int, conn: Connection, commit: bool = True):
    with conn.cursor(commit=commit) as cursor:
        cursor.execute(f'select cpf from usuario u order by random() limit {size}')
        comentarios = [
            (cpf, lorem.paragraph(),)
            for row in cursor.fetchall() for cpf in row
        ]
        cursor.executemany(
            f"insert into comentario (usuario, data_comentario, conteudo) values "
            "(%s, now() + (random() * 20)::int * '1 day'::interval, %s)",
            comentarios
        )

def load_agregados(ids: list[int], conn: Connection, commit: bool = True):
    base_url_metadata = 'https://servicodados.ibge.gov.br/api/v3/agregados/{id}/metadados'
    base_url_periodos = 'https://servicodados.ibge.gov.br/api/v3/agregados/{id}/periodos'
    base_url_resultados = (
        'https://servicodados.ibge.gov.br'
        '/api/v3/agregados/{agregado}'
        '/periodos/{periodo}'
        '/variaveis/{variavel}'
        '?localidades={nivel}[all]'
    )

    for id in ids:
        response = requests.get(base_url_metadata.format(id=id))
        response.raise_for_status()
        metadata = response.json()

        print(metadata['nome'])

        with conn.cursor(commit=commit) as cursor:
            cursor.execute(
                'insert into agregado_ibge(id, pesquisa, nome, assunto) '
                'values (%s, (select id from pesquisa_ibge where nome = %s), %s, %s) '
                'on conflict do nothing;',
                [metadata['id'], metadata['pesquisa'], metadata['nome'], metadata['assunto']]
            )

        with conn.cursor(commit=commit) as cursor:
            cursor.executemany(
                'insert into variavel_ibge(id, nome, agregado, unidade) '
                'values (%s, %s, %s, %s) '
                'on conflict do nothing;',
                [(variavel['id'], variavel['nome'], metadata['id'], variavel['unidade'])
                  for variavel in metadata['variaveis']]
            )

        niveis = list({nivel
                       for values in metadata['nivelTerritorial'].values()
                       for nivel in values})

        response = requests.get(base_url_periodos.format(id=id))
        response.raise_for_status()
        periodos = response.json()

        with conn.cursor(commit=commit) as cursor:
            for nivel in niveis[:1]:
                for variavel in metadata['variaveis'][:1]:
                    response = requests.get(base_url_resultados.format(
                        agregado=metadata['id'],
                        periodo='|'.join(periodo['id'] for periodo in periodos),
                        variavel=variavel['id'],
                        nivel=nivel))
                    response.raise_for_status()
                    resultado, *_ = response.json()

                    print(f"\t{metadata['id'] = }")
                    print(f"\t{variavel['id'] = }")
                    print(f"\t{nivel = }")

                    for res in resultado['resultados']:
                        classificacao = ', '.join(c['id'] for c in res['classificacoes'])
                        cursor.executemany(
                            'insert into mapa_ibge (id, nome) '
                            'values (%s, %s) '
                            'on conflict do nothing;',
                            [(serie['localidade']['id'], serie['localidade']['nome'])
                                for serie in res['series']]
                        )

                        cursor.executemany(
                            'insert into nivel_ibge (id, nome) '
                            'values (%s, %s) '
                            'on conflict do nothing;',
                            [(serie['localidade']['nivel']['id'], serie['localidade']['nivel']['nome'])
                                for serie in res['series']]
                        )

                        cursor.executemany(
                            'insert into localidade_ibge (id, nome, nivel) '
                            'values (%s, %s, %s) '
                            'on conflict do nothing;',
                            [(serie['localidade']['id'], serie['localidade']['nome'], serie['localidade']['nivel']['id'])
                                for serie in res['series']]
                        )

                        cursor.executemany(
                            'insert into resultado_ibge (variavel, classificacao, mapa) '
                            'values (%s, %s, %s) '
                            'on conflict do nothing;',
                            [(variavel['id'], classificacao, serie['localidade']['id'])
                                for serie in res['series']]
                        )

                        cursor.executemany(
                            'insert into serie_ibge (classificacao, periodo, valor, localidade) '
                            'values (%s, %s, %s, %s) '
                            'on conflict do nothing;',
                            [(classificacao, p, v, serie['localidade']['id'])
                                for serie in res['series']
                                for p, v in serie['serie'].items()
                                ]
                        )
