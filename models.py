import datetime

from sqlalchemy import Column, Date, Float, Integer, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB_PATH


metadata = MetaData()
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    id_order = Column(Integer)
    order_number = Column(Integer)
    price_usd = Column(Integer)
    price_rub = Column(Float)
    delivery_date = Column(Date)

    def __init__(self, data: list[str], usd_rates):
        self.id_order = data[0]
        self.order_number = int(data[1])
        self.price_usd = int(data[2])
        self.price_rub = self.price_usd * usd_rates
        self.delivery_date = datetime.datetime.strptime(
            data[3].replace('.', '-'), '%d-%m-%Y'
        ).date()


def create_table():
    Base.metadata.create_all(engine)


def drop_table():
    if Base.metadata.tables is None:
        return
    Base.metadata.drop_all(engine)
