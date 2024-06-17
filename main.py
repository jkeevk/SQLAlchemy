import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import *
import configparser

# функция получения данных для подключения к БД из .ini файла
def get_settings(): 
        config = configparser.ConfigParser()
        config.read("settings.ini") 
        prefix = config["SETTINGS"]["prefix"]
        name = config["SETTINGS"]["name"]
        password = config["SETTINGS"]["password"]
        adress = config["SETTINGS"]["adress"]
        data_base = config["SETTINGS"]["data_base"]
        return prefix, name, password, adress, data_base

# функция заполнения БД из файла
def fill_db(file_name):
    with open(file_name) as f:
        data = json.load(f)        
    for i in data:
        if i['model'] == 'publisher':
            pub_ = Publisher(publisher_name=i['fields']['name'])
            session.add(pub_)
        elif i['model'] == 'book':
            book_ = Book(title=i['fields']['title'], 
                         id_publisher=i['fields']['id_publisher']
                         )
            session.add(book_)
        elif i['model'] == 'shop':
            shop_ = Shop(shop_name=i['fields']['name'])
            session.add(shop_)       
        elif i['model'] == 'stock':
            stock_ = Stock(id_book=i['fields']['id_book'], 
                           id_shop=i['fields']['id_shop'], 
                           count=i['fields']['count']
                           )
            session.add(stock_)
        elif i['model'] == 'sale':
            sale_ = Sale(price=i['fields']['price'], 
                         date_sale=i['fields']['date_sale'], 
                         id_stock=i['fields']['id_stock'], 
                         count=i['fields']['count']
                         )
            session.add(sale_)
        session.commit()

# функция поиска книги
def find_book(res):
    query = session.query(Book.title, Shop.shop_name, Sale.price, Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res.isdigit():
        query = query.filter(Publisher.id == res).all()
        for title, name, price, date_sale in query:
                print(f"{title:<39} | {name:<10} | {price:^5} | {date_sale.strftime('%d-%m-%Y')}")
    else:
        query = query.filter(Publisher.publisher_name == res).all()
        for title, name, price, date_sale in query:
                print(f"{title:<39} | {name:<10} | {price:^5} | {date_sale.strftime('%d-%m-%Y')}")


if __name__ == '__main__':
    prefix, name, password, adress, data_base = get_settings()
    DSN = f'{prefix}://{name}:{password}@{adress}/{data_base}'
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    create_tables(engine)
    fill_db('tests_data.json')
    res = input('Введите id или имя издателя: ')
    # res = "O\u2019Reilly" # для отладки
    find_book(res)

    session.close()
