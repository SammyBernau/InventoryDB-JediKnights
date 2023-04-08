from typing import List
from typing import Optional
import psycopg2
from sqlalchemy import ForeignKey, Numeric, CheckConstraint, Date, func
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from Sam.inventoryDB_enums import product_type_enum, payment_method_enum, delivery_status_enum

engine = create_engine("postgresql+psycopg2://jediknights:yoda123@homeoftopgs.ddns.net/jediknights")


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'product'
    product_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    product_type: Mapped[str] = mapped_column(product_type_enum, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    pending_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # __table_args__ = (
    #     CheckConstraint('qty >= 0', name='non_negative_qty'),
    #     CheckConstraint('price >= 0.0', name='non_negative_price'),
    #     CheckConstraint('pending_qty >= 0', name='non_negative_pending_qty')
    # )


class ProductPriceHistory(Base):
    __tablename__ = 'product_price_history'
    price_history_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    previous_price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    date_changed: Mapped[Date] = mapped_column(Date, default=func.now(), nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), ForeignKey('product.product_id'), nullable=False)
    product: Mapped[Product] = relationship('product')

    # __table_args__ = (
    #     CheckConstraint('previous_price >= 0.0', name='positive_previous_price')
    # )


class Customer(Base):
    __tablename__ = 'customer'
    customer_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)


class Payment(Base):
    __tablename__ = 'payment'
    payment_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    payment_method: Mapped[str] = mapped_column(payment_method_enum, nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # __table_args__ = (
    #     CheckConstraint('total_price >= 0.0', name='positive_total_price'),
    # )


class CustomerOrder(Base):
    __tablename__ = 'customer_order'
    order_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    date: Mapped[Date] = mapped_column(Date, default=func.now(), nullable=False)
    total_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(50), ForeignKey('customer.customer_id'), nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), ForeignKey('product.product_id'), nullable=False)
    payment_id: Mapped[str] = mapped_column(String(50), ForeignKey('payment.payment_id'), nullable=False)
    customer: Mapped[Customer] = relationship('customer')
    product: Mapped[Product] = relationship('product')
    payment: Mapped[Payment] = relationship('payment')


class Delivery(Base):
    __tablename__ = 'delivery'
    delivery_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    delivery_date: Mapped[Date] = mapped_column(Date, default=func.now(), nullable=False)
    delivery_type: Mapped[str] = mapped_column(product_type_enum, nullable=False)
    delivery_status: Mapped[str] = mapped_column(delivery_status_enum, nullable=False)
    order_id: Mapped[str] = mapped_column(String(50), ForeignKey('customer_order.order_id'))
    customer_order: Mapped[CustomerOrder] = relationship('customer_order')


class Cart(Base):
    __tablename__ = 'cart'
    customer_id: Mapped[Customer] = mapped_column(String(50), ForeignKey('customer.customer_id'), primary_key=True,
                                                  nullable=False)
    product_id: Mapped[Product] = mapped_column(String(50), ForeignKey('product.product_id'), primary_key=True,
                                                nullable=False)


# creates tables only if they don't exist
Base.metadata.create_all(engine, checkfirst=True)
