from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
# Usuários


class PydanticModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # created_at: Optional[datetime] = datetime.utcnow()
    # updated_at: Optional[datetime] = datetime.utcnow()


class UserBase(PydanticModel):
    email: str


class UserSchema(UserBase):
    id: int
    nome: str
    senha: str
    dt_nasc: date
    lgpd: bool
    documento: str
    tipo_documento: str
    tipo_usuario: str
    deletado: bool


class UserInsert(UserBase):
    nome: str
    senha: str
    dt_nasc: date
    lgpd: bool
    documento: str
    tipo_documento: str
    tipo_usuario: str
    deletado: bool = False


class UserUpdate(UserInsert):
    velha_senha: str


class ProductBase(PydanticModel):
    nome: str
    tipo_produto: str
    quantidade: int
    valor_unitario: Decimal
    tempo_fabrica: Decimal
    observacao: str


class ProductSchema(ProductBase):
    id: int
    infos: str
    categoria: bool
    detalhes: str
    url_imagens: str
    nome_personalizado: str
    tipo_personalizado: str


class ProductInsert(ProductBase):
    infos: str
    categoria: bool
    detalhes: str
    url_imagens: str
    nome_personalizado: str
    tipo_personalizado: str


class ProductUpdate(ProductInsert):
    pass


# Address


class AddressBase(PydanticModel):
    cep: str
    logradouro: str
    numero: str
    bairro: str
    estado: str
    pais: str


class AddressSchema(AddressBase):
    id: int
    complemento: str
    ponto_ref: str
    tipo_endereco: str
    entrega: bool
    cobranca: bool
    usuario_id: int


class AddressInsert(AddressBase):
    complemento: str
    ponto_ref: str
    tipo_endereco: str
    entrega: bool
    cobranca: bool
    usuario_id: int


class AddressUpdate(AddressInsert):
    pass


#Payments


class PaymentBase(PydanticModel):
    nome: str


class PaymentSchema(PaymentBase):
    id: int
    tipo_pagamento: str
    usuario_id: int


class PaymentInsert(PaymentBase):
    tipo_pagamento: str
    usuario_id: int


class PaymentUpdate(PaymentInsert):
    pass


# Sales


class SaleBase(PydanticModel):
    valor_total: Decimal
    valor_unitario: Decimal
    quantidade: int
    frete: Decimal


class SaleSchema(SaleBase):
    id: int
    tipo_moeda: str
    tempo_envio: int
    tipo_entrega: str
    plataforma_pag: str
    periodo_envio: str  # corrente, util, etc
    estado_pedido: str
    obs_pedido: Optional[str] = None
    motivo_devolucao: Optional[str] = None
    nome_impressao: Optional[str] = None
    msg_presente: Optional[str] = None
    produto_id: int
    metodo_pagamento_id: int
    comprador_id: int
    endereco_entrega_id: int
    endereco_cobranca_id: int


class SaleInsert(SaleBase):
    tipo_moeda: str
    tempo_envio: int
    tipo_entrega: str
    plataforma_pag: str
    periodo_envio: str  # corrente, util, etc
    estado_pedido: str
    obs_pedido: Optional[str] = None
    motivo_devolucao: Optional[str] = None
    nome_impressao: Optional[str] = None
    msg_presente: Optional[str] = None
    produto_id: int
    metodo_pagamento_id: int
    comprador_id: int
    endereco_entrega_id: int
    endereco_cobranca_id: int


class SaleUpdate(SaleInsert):
    pass
