from pydantic import BaseModel

class SchemaProduto(BaseModel):
    id: int
    nome: str