
from sqlalchemy import create_engine, MetaData, Table, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship, sessionmaker

# Configura tu URI de conexión SQLite. Asegúrate de ajustar la ruta a tu archivo de base de datos.
database = 'sqlite:///database//PCdb.sqlite3'
engine = create_engine(database, echo=True)

metadata = MetaData()
metadata.reflect(bind=engine) # Reflejar las tablas existentes en la base de datos

Base = declarative_base() # Crear una clase base para las declaraciones de modelos

class ItemTypes(Base):
    __table__ = Table('ItemType', metadata, autoload_with=engine)
    # Relación con la tabla 'parent'
    component = relationship("Components", back_populates="type")

class Components(Base):
    __table__ = Table('Component', metadata, autoload_with=engine)
    # Relación con la tabla 'child'
    type = relationship("ItemTypes", back_populates="component")


Session = sessionmaker(bind=engine)
session = Session()

# item_type = Table('ItemType', metadata, autoload_with=engine)

# Definir una clase de modelo para la tabla reflejada
# class Components(Base):
#     __table__ = component

# class ItemTypes(Base):
#     __table__ = item_type


# with Session() as session:
    # procesador = ItemTypes(
	#     name =	"Procesador"
    # )
    
processor = ItemTypes(
    type_id = 0,
    name = "Procesador"
)
session.add(processor)
session.commit()

corei9 = Components(
    type_id = processor.type_id,
    brand = "Intel",
    model =	"Core i9",
    seller = "Cyberpuerta",
    price = "12500",
    url = "http://www.cyberpuerta.com",
    features =	"3.4 GHz",
    speed =	3.4,
    selected = 1
)
session.add(corei9)
session.commit()

# processor = session.query(ItemTypes).first()
# print(f'ItemTypes: {processor.name}, Component: {[elem.brand for elem in processor.corei9]}')
     
# results = session.query(Components).all()
# for result in results:
#     print(result)    
    