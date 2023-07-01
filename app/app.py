from comandos import Opcao, Usuario, Consulta
from db.connection import Connection

from colorama import Fore
import time


def main():
    try:
        conn = Connection()
        while True:
            Opcao.mostrar_todas()
            opcao = Opcao.ler()
            match opcao:
                case Opcao.SAIR:
                    print('Finalizando o programa...')
                    break
                case Opcao.BUSCAR_USUARIO:
                    cpf = input("Informe um cpf para ser buscado: ").strip()
                    usuario = Usuario.buscar(cpf, conn)
                    if usuario:
                        print(f"{usuario!r}")
                    else:
                        print(f"nenhum usário com cpf {Fore.MAGENTA}{cpf!r}{Fore.RESET} encontrado!")
                case Opcao.CADASTRAR_USUARIO:
                    usuario = Usuario.ler()
                    usuario.criar(conn, commit=True)
                case Opcao.AUTORIZAR_PESQUISA:
                    consulta = Consulta.ler()
                    consulta.criar(conn, commit=True)
            time.sleep(0.5)

    finally:
        conn.close()
    print("Programa finalizado com sucesso")

if __name__ == '__main__':
    main()
