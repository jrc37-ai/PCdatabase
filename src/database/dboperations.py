from sqlalchemy import create_engine, MetaData, Table, Integer, Column
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
        type_ids = [elem.type_id for elem in query] 
        names = [elem.name for elem in query] 
        self.session.close()
        return (type_ids, names)

    # def func():
    #     processor = ItemTypes(
    #         name = "Procesador"
    #     )
    #     session.add(processor)
    #     session.commit()

    #     corei9 = Components(
    #         type_id = processor.type_id,
    #         brand = "Intel",
    #         model =	"Core i9",
    #         seller = "Cyberpuerta",
    #         price = "12500",
    #         url = "http://www.cyberpuerta.com",
    #         features =	"3.4 GHz",
    #         speed =	3.4,
    #         selected = 1
    #     )
    #     session.add(corei9)
    #     session.commit()

        
            
        # results = session.query(Components).all()
        # for result in results:
        #     print(result)    


            
