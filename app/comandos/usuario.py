from dataclasses import dataclass, field, fields

from db.connection import Connection
from db.model import DataModel

@dataclass(kw_only=True)
class Usuario(DataModel):
    cpf: str
    nome: str
    sobrenome: str
    email: str
    cod_pais: str
    ddd: str
    numero: str
    senha: str = field(repr=False)
    endereco: str
    tipo: str

    @classmethod
    def ler(cls):
        mensagem_inicial = f"Informe os dados do usuário a ser criado:"
        return super().ler(mensagem_inicial)

    def criar(self, conn: Connection, commit: bool = True):
        super().criar('usuario', conn=conn, commit=commit)

    @classmethod
    def buscar(cls, cpf: str, conn: Connection, commit: bool = True):
        usuario = super().buscar('usuario', q={'cpf': cpf}, conn=conn, commit=commit, fetchone=True)
        return usuario
