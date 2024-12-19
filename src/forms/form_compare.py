import tkinter as tk
from tkinter import ttk, StringVar
from pprint import pprint

from forms.form_display import FormDisplay

from database.dboperations import DBOps
from config import *

class FormCompare(FormDisplay, ttk.Frame):
    def __init__(self, panel_principal) -> None:
        self.panel_principal = panel_principal
        self.db = DBOps()
        
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.panel_lista = tk.Frame(self.panel_principal)
        self.panel_lista.pack(side=tk.TOP, fill=tk.X, expand=False)
        
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
        
        text = 'ELIGE COMPONENTE...'
        
        unique_types = [component['category']['FORM_VALUE'].upper() for
                        component in self.db.Components]
        unique_types = list(set(unique_types))
        
        max_len = [text] + unique_types
        max_len = [len(elem) for elem in max_len]
        max_len = max(max_len) + 5
        
        variable = StringVar()
        
        opciones = ttk.OptionMenu(
            self.labelBarra,
            variable,
            variable.set(text),
            *unique_types,
            command=self.compare_components
        )

        opciones.config(width=max_len)
        opciones.pack(padx=20, pady=18)

    def compare_components(self, variable):
        self.limpiar_panel(self.panel_lista)
        self.mostrar_items()

    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()