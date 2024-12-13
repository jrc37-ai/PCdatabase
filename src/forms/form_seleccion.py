import tkinter as tk
from tkinter import ttk

from database.dboperations import DBOps
from config import *

class FormSelected(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        self.panel_principal = panel_principal
        
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.titulo = tk.Label(self.barra_superior, text="RESULTADO")
        self.titulo.config(
            fg="#fff",
            font=("Helvetica", 14, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=2,
            anchor=tk.W,
            padx=20
        )
        self.titulo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.buscar_seleccionados()
    
    def buscar_seleccionados(self):
        self.db = DBOps()
        self.selected = self.db.get_selected()
    
    def mostrar_elementos(self):
        self.panel_selected = tk.Frame(self.panel_principal)
        self.panel_selected.pack(side=tk.TOP, fill=tk.X, expand=True)
        
        for type in self.db.Item_types:
            if type.name in [x['type_id'] for x in self.selected]:
                self.frame_component = tk.Frame(self.panel_principal)
                self.frame_component.pack(side=tk.TOP, fill=tk.X, expand=True)
                
                self.label_component = tk.Label()
            
            