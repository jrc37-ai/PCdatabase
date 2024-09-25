from sqlalchemy import create_engine, MetaData, Table, Integer, Column, inspect
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.automap import automap_base

class DBOps():
    def __init__(self) -> None:
        # Configura tu URI de conexión SQLite. Asegúrate de ajustar la ruta a tu archivo de base de datos.
        self.database = 'sqlite:///database//PCdb.sqlite3'
        self.engine = create_engine(self.database, echo=True)

        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

        self.ItemTypes = self.base.classes.ItemType
        self.Components = self.base.classes.Component
        
    def item_types_query(self):
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        query = self.session.query(self.ItemTypes).all()
        type_dict = {elem.name: elem.type_id for elem in query}
        self.session.close()
        return (type_dict)

    def get_columns(self):
         # Crear un inspector para obtener información sobre las columnas
        inspector = inspect(self.engine)

        # Obtener el nombre de la tabla correspondiente a self.Components
        table_name = self.Components.__mapper__.local_table.name

        # Obtener las columnas de la tabla
        columns = inspector.get_columns(table_name)
        return columns