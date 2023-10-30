from structure.connectors import Base
from sqlalchemy import String, Sequence, Date, DateTime, Integer, Numeric, Column, Boolean, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime


class DefaultModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, index=True)

    def formatted_date_created(self):
        return func.to_char(self.created_at, 'YYYY-MM-DD')

    def formatted_datetime_created(self):
        return func.to_char(self.created_at, 'YYYY-MM-DD HH24:MI:SS')

    def formatted_time_created(self):
        return func.to_char(self.created_at, 'HH24:MI:SS')

    def formatted_date_updated(self):
        return func.to_char(self.updated_at, 'YYYY-MM-DD')

    def formatted_datetime_updated(self):
        return func.to_char(self.updated_at, 'YYYY-MM-DD HH24:MI:SS')

    def formatted_time_updated(self):
        return func.to_char(self.updated_at, 'HH24:MI:SS')


class UserModel(DefaultModel):
    __tablename__ = 'usuarios'

    id = Column(Integer,
                primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    dt_nasc = Column(Date, nullable=False, index=True)
    lgpd = Column(Boolean, nullable=False)
    documento = Column(String(18), nullable=False, index=True)
    tipo_doc = Column(String(10), nullable=False)
    tipo_usuario = Column(String, nullable=False, default='comprador')
    deletado = Column(Boolean, nullable=False,
                      default=False)  # Usuário está desativado? (padrão é False) rmeoção lógica e não física

    enderecos = relationship('AddressModel', back_populates='usuario')
    pagamentos = relationship('PaymentMethodModel', back_populates='usuario')
    produtos = relationship('ProductModel', back_populates='usuario')
    vendas = relationship('SaleModel', back_populates='usuario')


class AddressModel(DefaultModel):
    __tablename__ = 'enderecos'
    id = Column(Integer, primary_key=True)
    cep = Column(String(20), nullable=False)
    complemento = Column(String(100))
    logradouro = Column(String(100), nullable=False)
    bairro = Column(String(50), nullable=False)
    numero = Column(String(20), nullable=False)
    estado = Column(String(5), nullable=False)
    pais = Column(String(50), nullable=False)
    ponto_ref = Column(String(250))
    tipo_endereco = Column(String(50), nullable=False)
    entrega = Column(Boolean, nullable=False)
    cobranca = Column(Boolean, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False,
                        onupdate='CASCADE')

    usuario = relationship('UserModel', back_populates='enderecos')


class PaymentMethodModel(DefaultModel):
    __tablename__ = 'tipo_pagamentos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    tipo_pagamento = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship('UserModel', back_populates='pagamentos')


class ProductToSaleModel(DefaultModel):
    __tablename__ = 'produto_para_venda'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    venda_id = Column(Integer, ForeignKey('vendas.id'), nullable=False)

    produto = relationship('ProductModel', back_populates='produto_para')
    venda = relationship('SaleModel', back_populates='venda_para')


class ProductModel(DefaultModel):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    tipo_produto = Column(String(255), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(precision=25, scale=2), nullable=False)
    tempo_fabrica = Column(Float, nullable=False)
    observacao = Column(String(255))
    infos = Column(String(255))
    categoria = Column(Boolean, nullable=False)
    detalhes = Column(String(255))
    url_imagens = Column(String(255))
    personalizacao = Column(String(255))
    nome_impressao = Column(String(255))
    msg_presente = Column(String(255))
    tipo_personalizado = Column(String(255))
    registrador_id = Column(Integer, ForeignKey('usuarios.id'),
                            nullable=False)  # quem criou
    
    usuario = relationship('UserModel', back_populates='produtos')
    produto_para = relationship('ProductToSaleModel', back_populates='produto')

class SaleModel(DefaultModel):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    valor_total = Column(Numeric(precision=25, scale=2), nullable=False)
    valor_unitario = Column(Numeric(precision=25, scale=2), nullable=False)
    quantidade = Column(Integer, nullable=False)
    frete = Column(Numeric(precision=25, scale=2), nullable=False)
    tipo_moeda = Column(String(20), nullable=False)
    tempo_envio = Column(Integer, nullable=False)
    tipo_entrega = Column(String(50), nullable=False)
    plataforma_pag = Column(String(50), nullable=False)
    periodo_envio = Column(String(20), nullable=False)
    estado_pedido = Column(String(100), nullable=False)
    obs_pedido = Column(String(255))
    motivo_devolucao = Column(String(255))
    metodo_pagamento_id = Column(Integer, ForeignKey('tipo_pagamentos.id'),
                                 nullable=False)
    comprador_id = Column(Integer, ForeignKey('usuarios.id'),
                          nullable=False)  # quem comprou
    endereco_entrega_id = Column(Integer, ForeignKey('enderecos.id'),
                                 nullable=False)
    endereco_cobranca_id = Column(Integer, ForeignKey('enderecos.id'),
                                  nullable=False)
    
    usuario = relationship('UserModel', back_populates='vendas')
    venda_para = relationship('ProductToSaleModel', back_populates='venda')
