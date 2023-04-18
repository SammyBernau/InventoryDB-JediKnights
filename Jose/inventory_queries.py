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
from sqlalchemy import func,distinct
from pprint import pprint
from project3_ORM import Product, ProductPriceHistory, Customer, Payment, CustomerOrder, Delivery

engine = create_engine("postgresql+psycopg2://jediknights:yoda123@homeoftopgs.ddns.net/jediknights")


class Base(DeclarativeBase):
    pass

with Session(engine) as session:
    query = session.query(Payment.payment_method,
     func.count(distinct(CustomerOrder.order_id)).label("Num_Of_Orders"),
     func.sum(Payment.total_price).label("Total_Revenue")) \
        .join(CustomerOrder, Payment.payment_id == CustomerOrder.payment_id) \
        .join(Product, Product.product_id == CustomerOrder.product_id) \
        .group_by(Payment.payment_method) \
        .order_by(func.sum(Payment.total_price))

    results = query.all()

    print("Query 1: List the  number of orders and the total revenue  for each payment method such as Venmo, credit card, etc\n")
    print("{:20} {:22} {}".format("Payment method","Number of Orders", "Total Revenue ($)"))
    for result in results:
        print("_________________________________________________________")
        print("|{:20} {:7} {:26}|".format(result.payment_method,result.Num_Of_Orders,result.Total_Revenue))
print("\n\n\n")



print("Query 2: List each customer name along with the product name they ordered with the  total price\n")
query = session.query(Customer.customer_id.label('Customer_ID'), Customer.name.label('Customer_Name'), Product.name.label('Product_Name'), Payment.total_price.label('total'))\
    .join(CustomerOrder, CustomerOrder.customer_id == Customer.customer_id)\
    .join(Product, Product.product_id == CustomerOrder.product_id)\
    .join(Payment, Payment.payment_id == CustomerOrder.payment_id)\
    .group_by(Customer.customer_id, Customer.name, Product.name,Payment.total_price)\
    .order_by(Customer.customer_id.asc())

data = query.all()
print("{:32}{:32}{}".format("Customer","Product","Total Price ($)"))
for result in data:
    print(" --------------------------------------------------------------------------")
    print("|{:30} {:20} {:21}|".format(result.Customer_Name, result.Product_Name, result.total))
    print(" --------------------------------------------------------------------------")
print("\n\n\n")

records = session.query(distinct(Delivery.order_id),Delivery.delivery_status,CustomerOrder.address,Customer.name,Payment.payment_method,Payment.total_price)\
       .join(CustomerOrder, Payment.payment_id == CustomerOrder.payment_id)\
       .join(Delivery, Delivery.order_id == CustomerOrder.order_id)\
       .join(Customer, Customer.customer_id == CustomerOrder.customer_id)\
       .where(Payment.total_price > 40.00)
print("Query 3: List the customer name, their payment method , order status along with total price of the order>$40\n\n")
print(" {:21}{:21}{:21}{}".format("Customer","Payment Method", "Delivery status", "Total Price ($)"))
for record in records:
     print(" --------------------------------------------------------------------------")
     print(f"|{record.name:20} {record.payment_method:20} {record.delivery_status:20} {record.total_price:10}|")
     print(" --------------------------------------------------------------------------")






#print the results




