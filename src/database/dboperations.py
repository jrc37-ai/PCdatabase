from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

from database.modelos import ItemTypeModel, ComponentModel

class DBOps():
    def __init__(self) -> None:
        # Ruta del archivo de base de datos.
        self.database = 'sqlite:///database//PCdb.sqlite3'
        self.engine = create_engine(self.database, echo=True)
        
        self.Item_types = self.get_item_types()
        self.Components = self.get_components()
    
    def registrar_componente(self, **datos):
        componente = ComponentModel()
        
        componente.type_id = datos['type_id']
        componente.brand = datos['brand']
        componente.model = datos['model']
        componente.seller = datos['seller']
        componente.price = datos['price']
        componente.url = datos['url']
        componente.features = datos['features']
        componente.capacity = datos['capacity']
        componente.speed = datos['speed']
        componente.certification = datos['certification']
        componente.resolution = datos['resolution']
        componente.refresh = datos['refresh']
        componente.rate = datos['rate']
        componente.selected = datos['selected']
        
        with Session(self.engine) as session:
            session.add(componente)
            session.commit()
    
    def modificar_componente(self, item, **datos):
        with Session(self.engine) as session:
            componente = session.query(ComponentModel).filter_by(item_id=item).one()

            componente.type_id = datos['type_id']
            componente.brand = datos['brand']
            componente.model = datos['model']
            componente.seller = datos['seller']
            componente.price = datos['price']
            componente.url = datos['url']
            componente.features = datos['features']
            componente.capacity = datos['capacity']
            componente.speed = datos['speed']
            componente.certification = datos['certification']
            componente.resolution = datos['resolution']
            componente.refresh = datos['refresh']
            componente.rate = datos['rate']
            componente.selected = datos['selected']
            
            session.commit()
        
    def get_item_types(self) -> List[ItemTypeModel]:
        item_types: ItemTypeModel = None
        with Session(self.engine) as session:
            item_types = session.query(ItemTypeModel).all()
        return item_types
    
    def get_components(self) -> List[ComponentModel]:
        components: List[ComponentModel] = []
        with Session(self.engine) as session:
            components = session.query(ComponentModel).options(
                joinedload(ComponentModel.item_type)
                ).all()
        
        return components

        
    # def db_query(self):
    #     self.Session = sessionmaker(bind=self.engine)
    #     self.session = self.Session()
        
    #     item_query = self.session.query(self.ItemTypes).all()
    #     type_dict = {elem.name: elem.type_id for elem in item_query}
        
    #     component_query = self.session.query(self.Components).all()
                      
    #     component_dict = []
    #     for component in component_query:
    #         component_dict += [
    #             {
    #                 column.name: getattr(component, column.name)
    #                 for column in self.Components.__table__.columns
    #             }
    #         ]
            
    #     self.session.close()
    #     return (type_dict, component_dict)

    # def get_columns(self):
    #      # Crear un inspector para obtener información sobre las columnas
    #     inspector = inspect(self.engine)

    #     # Obtener el nombre de la tabla correspondiente a self.Components
    #     table_name = self.Components.__mapper__.local_table.name

    #     # Obtener las columnas de la tabla
    #     columns = inspector.get_columns(table_name)
    #     return columns