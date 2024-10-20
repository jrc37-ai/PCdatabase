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
        
        for key in datos:
            setattr(componente, key, datos[key])
               
        # componente.type_id = datos['type_id']
        # componente.brand = datos['brand']
        # componente.model = datos['model']
        # componente.seller = datos['seller']
        # componente.price = datos['price']
        # componente.url = datos['url']
        # componente.features = datos['features']
        # componente.capacity = datos['capacity']
        # componente.speed = datos['speed']
        # componente.certification = datos['certification']
        # componente.resolution = datos['resolution']
        # componente.refresh = datos['refresh']
        # componente.rate = datos['rate']
        componente.selected = 0
        
        with Session(self.engine) as session:
            session.add(componente)
            session.commit()
    
    def modificar_componente(self, item, **datos):
        with Session(self.engine) as session:
            componente = session.query(ComponentModel).filter_by(item_id=item).one()
            
            for key in datos:
                setattr(componente, key, datos[key])
            
            session.commit()
        
    def get_item_types(self) -> List[ItemTypeModel]:
        item_types: ItemTypeModel = None
        with Session(self.engine) as session:
            item_types = session.query(ItemTypeModel).all()
        return item_types
    
    def get_components(self) -> List[ComponentModel]:
        elements: List[ComponentModel] = []
        with Session(self.engine) as session:
            elements = session.query(ComponentModel).options(
                joinedload(ComponentModel.item_type)
                ).all()
        components = self.from_database(elements)
            
        return components

    def from_database(self, elements):
        components = []
        for element in elements:
            dict = {}
            for columna in ComponentModel.__table__.columns:
                if columna.foreign_keys:
                    dict[columna.name] = element.item_type.name
                else:
                    dato = getattr(element, columna.name)
                    dict[columna.name] = "" if dato==None else dato
            components += [dict]
                
        return components
    
    def to_database(self, element):
        component = {}
        for key in element:
            if element[key] == "":
                component[key] = None
            elif element[key] in [obj.name for obj in self.Item_types]:
                component[key] = [obj.type_id for obj in self.Item_types
                                  if obj.name==element[key]][0]
            else:
                component[key] = element[key]
        
        return component        