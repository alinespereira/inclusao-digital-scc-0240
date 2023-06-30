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
