from structure.connectors import Base, engine, Session, get_db
from sqlalchemy import String, Sequence, Date, Integer, Column, Boolean
from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI, HTTPException, Response, Depends
from datetime import date
from typing import Optional


class UserModel(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, Sequence('users_id', 1, 1),
                primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    dt_nascimento = Column(Date, nullable=False, index=True)
    termos_lgpd = Column(Boolean, nullable=False)
    documento = Column(String(18), nullable=False, index=True)
    tipo_documento = Column(String(10), nullable=False)
    tipo_usuario = Column(String, nullable=False)  # Comprador ou Vendedor


#Deixar os atributos todos opcionais! -> Tem de ajustar
# class AllOptional(pydantic.main.ModelMetaclass):
#     def __new__(cls, name, bases, namespaces, **kwargs):
#         annotations = namespaces.get('__annotations__', {})
#         for base in bases:
#             annotations.update(base.__annotations__)
#         for field in annotations:
#             if not field.startswith('__'):
#                 annotations[field] = Optional[annotations[field]]
#         namespaces['__annotations__'] = annotations
#         return super().__new__(cls, name, bases, namespaces, **kwargs)

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    senha: str
    email: str
    dt_nascimento: date
    termos_lgpd: bool
    documento: str
    tipo_documento: str
    tipo_usuario: str


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    nome: Optional[str] = None
    senha: Optional[str] = None
    email: Optional[str] = None
    dt_nascimento: Optional[date] = None
    termos_lgpd: Optional[bool] = None
    documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    tipo_usuario: Optional[str] = None


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/usuario/')
def ler_usuario(user_id: int = None, nome: str = None,
                limit: int = 10,
                session: Session = Depends(get_db)):
    try:
        leitura = session.query(UserModel)
        if user_id:
            leitura = leitura.filter(UserModel.id == user_id)
        if nome:
            leitura = leitura.filter(UserModel.nome.like(nome))
        if limit:
            leitura = leitura.limit(limit)
        itens = leitura.all()
        return [UserSchema.model_validate(item) for item in itens]
    except Exception as exp:
        return Response(content=f"Erro na leitura de usuário: {exp}")


@app.post('/usuario/')
def inserir_usuario(dados_para_inserir: UserSchema,
                    session: Session = Depends(get_db)):
    conteudo = dados_para_inserir.model_dump(exclude={'id'})
    try:
        criar_usuario = UserModel(**conteudo)
        session.add(criar_usuario)
        session.commit()
        session.refresh(criar_usuario)
        return UserSchema.model_validate(criar_usuario)
    except Exception as exp:
        session.rollback()
        return Response(content=f'Erro na criação de usuário {exp}')


@app.put('/usuario/')
def atualizar_usuario(dados_para_atualizar: UserUpdateSchema,
                      session: Session = Depends(get_db)):
    usuario = session.query(UserModel).filter(UserModel.id == dados_para_atualizar.id)
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não existe')
    try:
        usuario.update(dados_para_atualizar.model_dump(exclude_unset=True))
        session.commit()
        session.flush()
        return UserUpdateSchema.model_validate(usuario)
    except Exception as exp:
        session.rollback()
        return Response(content=f'Erro na atualização de usuário {exp}')


@app.delete('/usuario/')
def deletar_usuario(user_id: int,
                    session: Session = Depends(get_db)):
    usuario = session.query(UserModel).filter(UserModel.id == user_id)
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não existe')
    try:
        session.delete(usuario.one())
        session.commit()
        return f'usuário deletado: {usuario}'
    except Exception as exp:
        session.rollback()
        return Response(content=f'Erro na atualização de usuário {exp}')

