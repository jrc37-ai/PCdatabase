from sqlalchemy import Column
from sqlalchemy import String, Integer, Numeric, Text, SmallInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ComponentModel(Base):
    __tablename__ = "Component"
    
    item_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    category = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)  
    price = Column(Numeric(6, 2, asdecimal=False), nullable=False)
    seller = Column(String, nullable=False)
    capacity = Column(String)
    frequency = Column(String)
    resolution = Column(String)
    features = Column(Text, nullable=False)
    rate = Column(String)
    url = Column(Text)
    date = Column(String, nullable=False)
    selected = Column(SmallInteger, nullable=False, default=0)