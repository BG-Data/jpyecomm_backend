from sqlalchemy.orm import Session
from structure.models import ModelProduto
from structure.connectors import get_db, SessionLocal
from fastapi import Depends
from structure.schemas import SchemaProduto


class ProdutoService:
    'Criar o serviço de produto da aplicação'

    def ler_produto(self,
                    nome: str,
                    session: Session = SessionLocal(),
                    limit: int = 10):
        query = session.query(ModelProduto)\
                .filter(ModelProduto.nome.like(nome))\
                .limit(limit=limit).all()
        return [SchemaProduto.model_validate(queries) for queries in query]

    def inserir_produto(self):
        pass

    def atualizar_produto(self):
        pass

    def deletar_produto(self):
        pass
