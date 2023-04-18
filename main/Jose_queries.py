from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from project3_ORM import *

engine = create_engine("postgresql+psycopg2://jediknights:yoda123@homeoftopgs.ddns.net/jediknights")


class Base(DeclarativeBase):
    pass


with Session(engine) as session:
    records = session.query(Delivery.delivery_status, CustomerOrder.address, Customer.name, Payment.payment_method,
                            Payment.total_price) \
        .join(CustomerOrder, Payment.payment_id == CustomerOrder.payment_id) \
        .join(Delivery, Delivery.order_id == CustomerOrder.order_id) \
        .join(Customer, Customer.customer_id == CustomerOrder.customer_id) \
        .where(Payment.total_price < 50.00)

for record in records:
    #  print(record.name,"has paid with",record.payment_method,"and their order is currently",record.delivery_status)
    print("---------------------------------------------------------------------------------------")
    print(f"||{record.name:20} {record.payment_method:20} {record.delivery_status:20} {record.total_price:10}||")
    print("---------------------------------------------------------------------------------------")

query = session.query(Customer.name, CustomerOrder.total_qty, Payment.payment_method) \
    .join(CustomerOrder, CustomerOrder.customer_id == Customer.customer_id) \
    .join(Payment, Payment.payment_id == CustomerOrder.payment_id) \
    .group_by(Customer.name, CustomerOrder.total_qty, Payment.payment_method) \
    .order_by(Customer.name.asc())

results = query.all()

for result in results:
    print("||{:20}||{:20}||{:20}||".format(result.name, result.total_qty, result.payment_method))

query = session.query(Customer.customer_id.label('Customer_ID'), Customer.name.label('Customer_Name'),
                      Product.name.label('Product_Name'), Payment.total_price.label('total')) \
    .join(CustomerOrder, CustomerOrder.customer_id == Customer.customer_id) \
    .join(Product, Product.product_id == CustomerOrder.product_id) \
    .join(Payment, Payment.payment_id == CustomerOrder.payment_id) \
    .group_by(Customer.customer_id, Customer.name, Product.name, Payment.total_price) \
    .order_by(Customer.customer_id.asc())

data = query.all()

# print the results

for result in data:
    print("{:30}{:20}{:20}".format(result.Customer_Name, result.Product_Name, result.total))
