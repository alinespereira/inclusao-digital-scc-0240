from dataclasses import asdict, fields
from psycopg2 import DataError, IntegrityError, sql
import sys

from db.connection import Connection

class DataModel:
    @classmethod
    def ler(cls, mensagem_inicial: str):
        print(mensagem_inicial)
        data = {}
        for field in fields(cls):
            raw = input(f'\t{field.name}: ').strip()
            if len(raw) == 0:
                raw = None
            data[field.name] = field.type(raw)

        return cls(**data)

    def criar(self, table_name: str, conn: Connection, commit: bool = True):
        values = list(asdict(self).values())
        query = sql.SQL("insert into {table} ({fields}) values ({placeholders})").format(
            fields=sql.SQL(',').join([
                sql.Identifier(field) for field in asdict(self).keys()
            ]),
            table=sql.Identifier(table_name),
            placeholders=sql.SQL(',').join([
                sql.Placeholder() for _ in values
            ])
        )

        with conn.cursor(commit=commit) as cursor:
            try:
                cursor.execute(query, values)
            except DataError as e:
                print('Os dados fornecidos apresentam erros')
                print(f"{type(e).__name__}: {e}", file=sys.stderr)
            except IntegrityError as e:
                print('As restrições de integridade da base de dados não foram atendidas')
                print(f"{type(e).__name__}: {e}", file=sys.stderr)
            else:
                print(f'Sucesso: {self!r}')

    @classmethod
    def buscar(cls, table_name: str, q: dict, conn: Connection, commit: bool = True, fetchone: bool = True):
        query = sql.SQL('select * from {table} where {filters}').format(
            table=sql.Identifier(table_name),
            filters=sql.SQL(' and ').join([
                sql.SQL(' = ').join([
                    sql.Identifier(column),
                    sql.Literal(value)
                ])
                for column, value in q.items()
            ])
        )

        with conn.cursor(commit=commit) as cursor:
            try:
                cursor.execute(query)
                columns = [col.name for col in cursor.description]
                if fetchone:
                    row = cursor.fetchone()
                    if row:
                        return cls(**dict(zip(columns, row)))
                else:
                    rows = cursor.fetchall()
                    return [
                        cls(**dict(zip(columns, row))) for row in rows
                    ]
            except DataError as e:
                print('Os dados fornecidos para a busca apresentam erros')
                print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return None
