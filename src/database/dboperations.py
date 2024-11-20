from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.modelos import ComponentModel
from config import *

class DBOps():
    def __init__(self) -> None:
        # Ruta del archivo de base de datos.
        self.database = 'sqlite:///database//PCdb.sqlite3'
        self.engine = create_engine(self.database, echo=True)
        
        self.Components = self.get_components()

    def get_components(self) -> List[ComponentModel]:
        elements: List[ComponentModel] = []
        with Session(self.engine) as session:
            elements = session.query(ComponentModel).all()
        components = self.from_database(elements)
            
        return components
    
    def from_database(self, elements):
        components = []
        
        for element in elements:
            FIELDS = DATA_FIELDS.copy()
            for key in FIELDS:
                FIELDS[key] = DATA_FIELDS[key].copy()
                dato = getattr(element, key)
                FIELDS[key]['BD_VALUE'] = dato
                if dato is not None:
                    FIELDS[key]['FORM_VALUE'] = dato
            components += [FIELDS]
                
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

    
    def registrar_componente(self, **datos):
        componente = ComponentModel()
        
        for key in datos:
            setattr(componente, key, datos[key])
               
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
            
    def eliminar_componente(self, item):
        with Session(self.engine) as session:
            componente = session.query(ComponentModel).filter_by(item_id=item).one()
            if componente:
                session.delete(componente)
                session.commit()
    
    def marcar_componente(self, item, selected):
        with Session(self.engine) as session:
            componente = session.query(ComponentModel).filter_by(item_id=item).one()
            
            setattr(componente, 'selected', selected)

            session.commit()
    
    
    