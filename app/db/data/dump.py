from typing import Iterable

from db.connection import Connection

def dump_table(table_name: str, conn: Connection) -> Iterable[str]:
    with conn.cursor() as cursor:
        cursor.execute(f'select * from {table_name}')
        columns = ', '.join(col.name for col in cursor.description)
        mask = ', '.join('%s' for _ in cursor.description)
        for row in cursor.fetchall():
            values = cursor.mogrify(mask, row).decode('utf-8')
            yield f"insert into {table_name}({columns}) values ({values});\n"

def dump_many_to_file(tables: list[str], file_name: str, conn: Connection):
    with open(file_name, 'w') as fp:
        for table in tables:
            fp.write(f'-- Inserções na tabela "{table}"\n')
            for row in dump_table(table, conn):
                fp.write(row)
            fp.write('\n\n')
