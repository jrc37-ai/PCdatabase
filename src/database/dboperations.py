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
                if key == 'price':
                    FIELDS[key]['FORM_VALUE'] = "$ {:,.2f}".format(dato)
            components += [FIELDS]
                
        return components
    
    def registrar_componente(self, **datos):
        componente = ComponentModel()
        
        for key in datos:
            if key in ['item_id', 'selected']:
                continue
            setattr(componente, key, datos[key]['BD_VALUE'])
        
        with Session(self.engine) as session:
            session.add(componente)
            session.commit()
    
    def modificar_componente(self, item, **datos):
        with Session(self.engine) as session:
            componente = session.query(ComponentModel).filter_by(item_id=item).one()
            
            for key in datos:
                if key in ['item_id', 'selected']:
                    continue
                setattr(componente, key, datos[key]['BD_VALUE'])
            
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
    
    
    