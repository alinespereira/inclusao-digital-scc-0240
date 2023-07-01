from db.connection import Connection
from db.data.generator import (generate_comments,
                               generate_users,
                               insert_users,
                               update_user_types,
                               load_agregados)
from db.data.dump import dump_many_to_file

def main():
    conn = Connection()
    tables = [
        'usuario',
        'moderador',
        'professor',
        'monitor',
        'aluno',
        'bane_usuario',
        'comentario',
        'bane_comentario',
        'curso',
        'disciplina',
        'inscricao',
        'curso_disciplina',
        'requisito',
        'turma',
        'evento',
        'avaliacao_disciplina',
        'avaliacao_curso',
        'membro_turma',
        'horario_turma',
        'teste',
        'realiza_teste',
        'avaliacao_professor',
        'avaliacao_monitor',
        'pesquisa_ibge',
        'consulta',
        'agregado_ibge',
        'variavel_ibge',
        'mapa_ibge',
        'resultado_ibge',
        'nivel_ibge',
        'localidade_ibge',
        'serie_ibge',
    ]
    file_name = 'db/sql/dump.sql'
    agregados = [8418, 1732, 1735, 1734, 1733, 2869, 992, 6449, 2933, 993, 2934,
                 994, 995, 2937, 1685, 3421, 6450, 988, 6703, 2059, 2074, 2061, 2060]
    try:
        # users = generate_users(200)
        # insert_users(users, conn, commit=True)
        # update_user_types(conn, commit=True)
        # generate_comments(25, conn, commit=True)
        # load_agregados(agregados, conn, commit=True)
        dump_many_to_file(tables, file_name, conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
