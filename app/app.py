from db.connection import Connection
from db.data.generator import generate_comments, generate_users, insert_users, update_user_types
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
        # 'avaliacao_disciplina',
        # 'avaliacao_curso',
        # 'membro_turma',
        # 'horario_turma',
        # 'teste',
        # 'realiza_teste',
        'avaliacao_professor',
        'avaliacao_monitor',
        # 'pesquisa_ibge'
        # 'consulta'
        # 'agregado_ibge'
        # 'variavel_ibge'
        # 'mapa_ibge'
        # 'resultado_ibge'
        # 'nivel_ibge'
        # 'localidade_ibge'
        # 'serie_ibge'
    ]
    file_name = 'db/sql/dump.sql'
    try:
        # users = generate_users(200)
        # insert_users(users, conn, commit=True)
        # update_user_types(conn, commit=True)
        # generate_comments(25, conn, commit=True)
        dump_many_to_file(tables, file_name, conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
