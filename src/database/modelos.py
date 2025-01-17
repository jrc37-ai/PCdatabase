from sqlalchemy import Column
from sqlalchemy import String, Integer, Numeric, Text, SmallInteger
from sqlalchemy.orm import declarative_base, validates
from rich import print

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
    
    @validates('price')
    def validate_price(self, key, price):
        try:
            val_price = float(price)
        except ValueError:
            print("--------- El precio debe ser un número.")
            raise ValueError("El precio debe ser un número.")
        
        if val_price <= 0:
            print("--------- El precio debe ser mayor que cero.")
            raise ValueError("El precio debe ser mayor que cero.")
        
        return price