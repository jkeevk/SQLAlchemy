import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
   
    __tablename__ = "publisher"
    
    id = sq.Column(sq.Integer, primary_key=True)
    publisher_name = sq.Column(sq.String(length=40), nullable=False)


class Book(Base):
   
    __tablename__ = "book"
    
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=80), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")


class Shop(Base):
   
    __tablename__ = "shop"
    
    id = sq.Column(sq.Integer, primary_key=True)
    shop_name = sq.Column(sq.String(length=40))


class Stock(Base):

    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")


class Sale(Base):
   
    __tablename__ = "sale"
    
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(10,2), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

