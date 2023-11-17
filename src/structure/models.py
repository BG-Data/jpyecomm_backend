from structure.connectors import Base
from sqlalchemy import String, Date, DateTime, Integer, \
      Numeric, Column, Boolean, Float, ForeignKey, \
        DateTime, BLOB, func
from sqlalchemy.orm import relationship
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
    __tablename__ = 'users'

    id = Column(Integer,
                primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True, unique=True)
    birthdate = Column(Date, nullable=False, index=True)
    lgpd = Column(Boolean, nullable=False)
    document = Column(String(18), nullable=False, index=True, unique=True)
    document_type = Column(String(10), nullable=False)
    user_type = Column(String(30), nullable=False, default='comprador')  # comprador, administrador(apenas devs) e vendedor
    deleted = Column(Boolean, nullable=False,
                     default=False)  # Usuário está desativado? (padrão é False) rmeoção lógica e não física

    addresses = relationship('AddressModel', back_populates='user')
    payments = relationship('UserToPayment', back_populates='user')
    products = relationship('ProductModel', back_populates='user')
    sales = relationship('SaleModel', back_populates='user')


class PaymentMethodModel(DefaultModel):
    __tablename__ = 'payment_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    payment_type = Column(String(100), nullable=False)

    payment_method = relationship('UserToPayment', back_populates='payment')


class UserToPayment(DefaultModel):
    __tablename__ = 'users_to_payment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    payment_id = Column(Integer, ForeignKey('payment_types.id'), nullable=False)

    user = relationship('UserModel', back_populates='payments')
    payment = relationship('PaymentMethodModel', back_populates='payment_method')


class ProductModel(DefaultModel):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    product_type = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_value = Column(Numeric(precision=25, scale=2), nullable=False)
    labor_time = Column(Float, nullable=False)
    obs = Column(String(255))
    infos = Column(String(255))
    category = Column(Boolean, nullable=False)
    details = Column(String(255))
    personalized_name = Column(String(255))
    personalized_type = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False)  # quem criou

    user = relationship('UserModel', back_populates='products')
    product_sale = relationship('SaleModel', back_populates='sale_product')
    files = relationship('ProductFilesModel', back_populates='product')


class ProductFilesModel(DefaultModel):
    __tablename__ = 'product_files'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'),
                        nullable=False)
    filename = Column(String(255), nullable=False)
    file = Column(BLOB, nullable=False)

    product = relationship('ProductModel', back_populates='files')


class AddressModel(DefaultModel):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    postal_code = Column(String(20), nullable=False)
    complement = Column(String(100))
    street = Column(String(100), nullable=False)
    neighborhood = Column(String(50), nullable=False)
    number = Column(String(20), nullable=False)
    state = Column(String(5), nullable=False)
    country = Column(String(50), nullable=False)
    reference_point = Column(String(250))
    address_type = Column(String(50), nullable=False)
    delivery = Column(Boolean, nullable=False)
    billing = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False,
                     onupdate='CASCADE')

    user = relationship('UserModel', back_populates='addresses')


class SaleModel(DefaultModel):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    total_value = Column(Numeric(precision=25, scale=2), nullable=False)
    unit_value = Column(Numeric(precision=25, scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    shipping_cost = Column(Numeric(precision=25, scale=2), nullable=False)
    currency_type = Column(String(20), nullable=False)
    delivery_time = Column(Integer, nullable=False)
    delivery_type = Column(String(50), nullable=False)
    payment_platform = Column(String(50), nullable=False)
    shipping_type = Column(String(20), nullable=False)  # corrente, util, etc
    order_status = Column(String(100), nullable=False)
    order_notes = Column(String(255), nullable=True)
    return_reason = Column(String(255), nullable=True)
    print_name = Column(String(255), nullable=True)
    gift_message = Column(String(255), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'),
                        nullable=False)
    payment_method_id = Column(Integer, ForeignKey('payment_types.id'),
                               nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'),
                      nullable=False)  # quem comprou
    delivery_address_id = Column(Integer, ForeignKey('addresses.id'),
                                 nullable=False)
    billing_address_id = Column(Integer, ForeignKey('addresses.id'),
                                nullable=False)

    user = relationship('UserModel', back_populates='sales')
    sale_product = relationship('ProductModel',
                                back_populates='product_sale')
