
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Configura tu URI de conexión SQLite. Asegúrate de ajustar la ruta a tu archivo de base de datos.
database = 'sqlite:///database//PCdb.sqlite3'
engine = create_engine(database, echo=True)
Base = declarative_base() # Crear una clase base para las declaraciones de modelos
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
metadata.reflect(bind=engine) # Reflejar las tablas existentes en la base de datos

component = Table('Component', metadata, autoload_with=engine)
item_type = Table('ItemType', metadata, autoload_with=engine)

# Definir una clase de modelo para la tabla reflejada
class Components(Base):
    __table__ = component

class ItemTypes(Base):
    __table__ = item_type


with Session() as session:
    procesador = ItemTypes(
	    name =	"Procesador"
    )
    
    corei9 = Components(
        type = ItemTypes(),
	    brand = "Intel",
	    model =	"Core i9",
	    seller = "Cyberpuerta",
	    price = "12500",
	    url = "http://www.cyberpuerta.com",
	    features =	"3.4 GHz",
	    speed =	3.4,
	    selected = 1
    )
    
    session.add_all([procesador, corei9])
    session.commit()
    
results = session.query(Components).all()
for result in results:
    print(result)    
    