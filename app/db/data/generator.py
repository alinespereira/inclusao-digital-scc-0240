import random
import requests

from db.connection import Connection

def generate_users(size: int = 2) -> list[dict]:
    response = requests.get(f'https://randomuser.me/api/?results={size}&nat=BR')
    response.raise_for_status()
    generated_users = response.json()
    users = [
        {
            'cpf': ''.join(str(random.choice(range(10))) for _ in range(11)),
            'nome': user['name']['first'],
            'sobrenome': user['name']['last'],
            'email': user['email'],
            'cod_pais': '+55',
            'ddd': random.choice(range(10, 100)),
            'numero': random.choice(range(1000_0000, 9_9999_9999)),
            'senha': user['login']['password'],
            'endereco': (
                f"{user['location']['street']['name']}, {user['location']['street']['number']}, "
                f"{user['location']['city']}, {user['location']['state']}, {user['location']['country']}"
            ),
            'tipo': random.choice(['moderador', 'professor', 'monitor', 'aluno']),
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
