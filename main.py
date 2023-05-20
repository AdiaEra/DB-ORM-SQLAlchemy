import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:пароль@localhost:5432/books_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as f:
    data = json.load(f)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    # session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


def info_sale(name):
    res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).join(Publisher).join(
        Stock).join(Shop).join(Sale).filter(Publisher.name == name).all()

    for c in res:
        print(f'{c.title:<39} | {c.name:<8} | {c.price * c.count:<5} | {c.date_sale}')


print(info_sale(name="O’Reilly"))
