from dataclasses import dataclass, field, fields

from db.connection import Connection
from db.model import DataModel

@dataclass(kw_only=True)
class Consulta(DataModel):
    professor: str
    pesquisa: str

    @classmethod
    def ler(cls):
        mensagem_inicial = f"Informe os dados para autorizar a consulta:"
        return super().ler(mensagem_inicial)

    def criar(self, conn: Connection, commit: bool = True):
        super().criar('consulta', conn=conn, commit=commit)

    @classmethod
    def buscar(cls, professor: str, pesquisa: str, conn: Connection, commit: bool = True):
        q = {
            'pesquisa': pesquisa,
            'professor': professor,
        }
        consulta = super().buscar('consulta', q=q, conn=conn, commit=commit, fetchone=True)
        return consulta
