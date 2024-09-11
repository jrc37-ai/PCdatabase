
from sqlalchemy import create_engine, MetaData, Table, Integer, Column
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.automap import automap_base

# Configura tu URI de conexión SQLite. Asegúrate de ajustar la ruta a tu archivo de base de datos.
database = 'sqlite:///database//PCdb.sqlite3'
engine = create_engine(database, echo=True)

Base = automap_base()
Base.prepare(engine, reflect=True)

ItemTypes = Base.classes.ItemType
Components = Base.classes.Component

# metadata = MetaData()
# metadata.reflect(bind=engine) # Reflejar las tablas existentes en la base de datos

# Base = declarative_base() # Crear una clase base para las declaraciones de modelos

# class ItemTypes(Base):
#     __table__ = Table('ItemType', metadata, autoload_with=engine)
#     # Relación con la tabla 'parent'
#     component = relationship("Components", back_populates="type")

# class Components(Base):
#     __table__ = Table('Component', metadata, autoload_with=engine)
#     # Relación con la tabla 'child'
#     type = relationship("ItemTypes", back_populates="component")

Session = sessionmaker(bind=engine)
session = Session()

processor = ItemTypes(
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

processor_query = session.query(ItemTypes).all()
print("Results.................................", [(elem.type_id, elem.name) for elem in processor_query])
     
# results = session.query(Components).all()
# for result in results:
#     print(result)    


    