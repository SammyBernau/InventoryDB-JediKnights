from sqlalchemy.orm import Session

from project3_ORM import *

engine = create_engine("postgresql+psycopg2://jediknights:yoda123@homeoftopgs.ddns.net/jediknights")

with Session(engine) as session:
    from sqlalchemy.orm import aliased

    # create aliases for tables
    p = aliased(Product)
    pp = aliased(ProductPriceHistory)

    # define the query
    query = (
        session.query(
            p.product_id,
            p.name,
            p.product_type,
            pp.date_changed,
            func.concat('$', p.price).label('current_price'),
            func.concat('$', pp.previous_price).label('previous_price'),
            func.concat('$', p.price - pp.previous_price).label('price_change')
        )
        .join(pp, p.product_id == pp.product_id)
        .order_by(p.product_id, pp.date_changed.desc())
    )

    # execute the query and print the results
    prod_id = "ID"
    prod_name = "Name"
    prod_type = "Type"
    date_changed = "Date Changed"
    curr = "Current Price"
    prev = "Previous Price"
    diff = "Price Difference"

    # Define separator row
    sep = "+{:-^20}+{:-^40}+{:-^40}+{:-^20}+{:-^20}+{:-^20}+{:-^20}+".format('', '', '', '', '', '', '')

    # Print query description
    print("List all products and their details along with their price adjustments")

    # Print header
    print(sep)
    print("|{:^20}|{:^40}|{:^40}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
        prod_id, prod_name, prod_type, date_changed, curr, prev, diff))
    print(sep)

    # Print rows
    results = query.all()
    for result in results:
        print("|{:^20}|{:^40}|{:^40}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
            result.product_id, result.name, result.product_type, str(result.date_changed),
            str(result.current_price), str(result.previous_price), str(result.price_change)))
        print(sep)
