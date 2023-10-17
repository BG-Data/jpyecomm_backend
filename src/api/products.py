from app.products import ProdutoService
from structure.connectors import Session, get_db
from fastapi import APIRouter, HTTPException, status, Depends


class ProdutoApi():
    def __init__(self) -> None:
        self.produto_service = ProdutoService()
        self.router = APIRouter()
        self.router.add_api_route('/',
                                  self.ler,
                                  methods=['GET'])
    
    def ler(self, nome: str, limit: int = None, 
            session: Session = Depends(get_db)):
        # Leitura
        lista_produtos = self.produto_service.ler_produto(session=session,
                                                          nome=nome,
                                                          limit=limit)
        if lista_produtos is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail='Não tenho um produto parecido com esse nome')
        return lista_produtos

    def inserir(self):
        pass

    def atualizar(self):
        pass

    def deletar(self):
        pass



