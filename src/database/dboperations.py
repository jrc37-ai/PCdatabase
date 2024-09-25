from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import sessionmaker
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
        
    def db_query(self):
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        item_query = self.session.query(self.ItemTypes).all()
        type_dict = {elem.name: elem.type_id for elem in item_query}
        
        component_query = self.session.query(self.Components).all()
                      
        component_dict = []
        for component in component_query:
            component_dict += {
                        column.name: getattr(component, column.name)
                        for column in self.Components.__table__.columns
                }
        print(component_dict)
            
        self.session.close()
        return (type_dict, component_dict)

    def get_columns(self):
         # Crear un inspector para obtener información sobre las columnas
        inspector = inspect(self.engine)

        # Obtener el nombre de la tabla correspondiente a self.Components
        table_name = self.Components.__mapper__.local_table.name

        # Obtener las columnas de la tabla
        columns = inspector.get_columns(table_name)
        return columns