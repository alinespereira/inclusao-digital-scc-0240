from enum import Enum, auto
from colorama import Fore

class Opcao(Enum):
    CADASTRAR_USUARIO = auto()
    BUSCAR_USUARIO = auto()
    AUTORIZAR_PESQUISA = auto()
    SAIR = 9

    @property
    def label(self) -> str:
        match self:
            case Opcao.CADASTRAR_USUARIO:
                return "Cadastrar usuário"
            case Opcao.BUSCAR_USUARIO:
                return "Buscar usuário"
            case Opcao.AUTORIZAR_PESQUISA:
                return "Autorizar consulta a pesquisa para professor"
            case Opcao.SAIR:
                return "Sair"


    @classmethod
    def mostrar_todas(cls):
        print("Opções disponíveis:")
        for opcao in cls:
            print(f"\t({opcao.value}) {Fore.GREEN}{opcao.label}{Fore.RESET}")

    @classmethod
    def ler(cls):
        try:
            id_opcao = input('Digite a opção desejada: ')
            opcao = cls(int(id_opcao))
        except ValueError:
            print(f"Opção inválida: {Fore.MAGENTA}{id_opcao}{Fore.RESET}")
            return cls.ler()
        else:
            return opcao
