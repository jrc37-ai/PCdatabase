from sqlalchemy import Column
from sqlalchemy import String, Integer, ForeignKey, DECIMAL, Text, SmallInteger
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ItemTypeModel(Base):
    __tablename__ = 'ItemType'

    type_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    
    items = relationship("ComponentModel", back_populates="item_type")

class ComponentModel(Base):
    __tablename__ = "Component"
    
    item_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey('ItemType.type_id'), nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)  
    seller = Column(String(30), nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)
    url = Column(String)
    features = Column(Text, nullable=False)
    capacity = Column(Integer)
    speed = Column(Integer)
    certification = Column(String)
    resolution = Column(String)
    refresh = Column(Integer)
    rate = Column(DECIMAL(3, 2))
    selected = Column(SmallInteger, nullable=False, default=0)
    
    item_type = relationship("ItemTypeModel", back_populates="items")