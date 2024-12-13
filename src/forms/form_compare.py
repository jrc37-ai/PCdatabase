import tkinter as tk
from tkinter import ttk
from pprint import pprint

from database.dboperations import DBOps

from config import *

class FormCompare(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        self.panel_principal = panel_principal
        self.db = DBOps()
        
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.labelBarra = tk.Label(self.barra_superior, text="COMPARAR COMPONENTES")
        self.labelBarra.config(
            fg="#fff",
            font=("Helvetica", 14, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=8,
            anchor=tk.W,
            padx=20
        )
        self.labelBarra.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        if len(self.db.Components) == 0:
            self.labelnodata = tk.Label(
                self.panel_principal,
                text="AÚN NO HAY REGISTROS EN LA BASE DE DATOS",
                font=("Helvetica", 12, 'italic'),
                pady=20,
                anchor=tk.N
            )
            self.labelnodata.pack(side=tk.TOP, fill=tk.X)
        else:
            self.mostrar_opciones()
    
    def mostrar_opciones(self):
        cs = ttk.Style()
        cs.theme_use('vista')
        
        text = 'ELIGE COMPONENTE'
        
        unique_types = [component['category']['FORM_VALUE'].upper() for
                        component in self.db.Components]
        unique_types = list(set(unique_types))
        
        opciones = ttk.Menubutton(self.labelBarra,
                                  text=text)
        menu = tk.Menu(opciones, tearoff=False)
        
        for type in unique_types:
            menu.add_command(
                label=type,
                command=None)

        opciones["menu"] = menu

        opciones.pack(padx=20, pady=18)
                    