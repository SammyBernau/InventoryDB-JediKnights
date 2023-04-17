from typing import List
from typing import Optional
from datetime import date
import psycopg2
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from pprint import pprint
from project3_ORM import Product, ProductPriceHistory, Customer, Payment, CustomerOrder, Delivery

engine = create_engine("postgresql+psycopg2://jediknights:yoda123@homeoftopgs.ddns.net/jediknights")


class Base(DeclarativeBase):
    pass

with Session(engine) as session:

    records = session.query(Delivery.delivery_status,CustomerOrder.address,Customer.name,Payment.payment_method,Payment.total_price)\
       .join(CustomerOrder, Payment.payment_id == CustomerOrder.payment_id)\
       .join(Delivery, Delivery.order_id == CustomerOrder.order_id)\
       .join(Customer, Customer.customer_id == CustomerOrder.customer_id)\
       .where(Payment.total_price < 50.00)
print("First query\n\n\n")


for record in records:
     #  print(record.name,"has paid with",record.payment_method,"and their order is currently",record.delivery_status)
     print(" --------------------------------------------------------------------------")
     print(f"|{record.name:20} {record.payment_method:20} {record.delivery_status:20} {record.total_price:10}|")
     print(" --------------------------------------------------------------------------")




query = session.query(Customer.name, CustomerOrder.total_qty, Payment.payment_method)\
     .join(CustomerOrder, CustomerOrder.customer_id == Customer.customer_id)\
     .join(Payment, Payment.payment_id == CustomerOrder.payment_id)\
     .group_by(Customer.name, CustomerOrder.total_qty, Payment.payment_method)\
     .order_by(Customer.name.asc())

results = query.all()
print("Second query\n\n\n")

for result in results:
    print(" --------------------------------------------------------------")
    print("|{:20} {:10} {:29}|".format(result.name,result.total_qty,result.payment_method))
    print(" --------------------------------------------------------------")

query = session.query(Customer.customer_id.label('Customer_ID'), Customer.name.label('Customer_Name'), Product.name.label('Product_Name'), Payment.total_price.label('total'))\
        .join(CustomerOrder, CustomerOrder.customer_id == Customer.customer_id)\
        .join(Product, Product.product_id == CustomerOrder.product_id)\
        .join(Payment, Payment.payment_id == CustomerOrder.payment_id)\
        .group_by(Customer.customer_id, Customer.name, Product.name,Payment.total_price)\
        .order_by(Customer.customer_id.asc())

data = query.all()


#print the results


print("Third query\n\n\n")

for result in data:
    print(" --------------------------------------------------------------------------")
    print("|{:30} {:20} {:21}|".format(result.Customer_Name, result.Product_Name, result.total))
    print(" --------------------------------------------------------------------------")



