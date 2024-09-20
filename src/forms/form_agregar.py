import tkinter as tk
from tkinter import ttk
from database.dboperations import DBOps
from config import *

class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal, database) -> None:
        super().__init__(panel_principal)
        self.field_entries = {}
        self.panel_principal = panel_principal
        self.database = database
        self.top_bar()
        self.panel_entradas()

    def top_bar(self):
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.label_barra_superior = tk.Label(self.barra_superior, text="AGREGAR COMPONENTE")
        self.label_barra_superior.config(
            fg="#fff",
            font=("Helvetica", 13, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=3
        )
        self.label_barra_superior.pack(side=tk.TOP, fill="x", expand=False)
        
    def panel_entradas(self):
        self.info_entry = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.info_entry.pack(expand=False)
                
        self.mostrar_formulario()
        
        self.boton_add = tk.Button(self.info_entry,
                                   text="AGREGAR",
                                   font=('Arial', 12, 'bold'),
                                   borderwidth=4,
                                   width=40,
                                   relief='flat',
                                   overrelief='groove',
                                   background=BOTON_ADD_FONDO,
                                   foreground=BOTON_ADD_TEXTO,
                                   activebackground=BOTON_ADD_FONDO,
                                   activeforeground=BOTON_ADD_TEXTO,
                                   command=self.ingresar_datos
                                   )
        self.boton_add.pack(side=tk.TOP, pady=10, padx=10)
        
    def mostrar_formulario(self):
        for field in TEXT_FIELDS.values():
            # self.field_entries = {
            #   'Marca': (label, entry),
            #   'Modelo': (label, entry),
            #   ...
            # }
            self.label_info_entry = tk.Frame(self.info_entry, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_info_entry.pack(side=tk.TOP, fill=tk.X, pady=1)

            if field in ['Componente']:
                self.component_bar(field)
            else:
                self.field_entries[field] = (
                    tk.Label(self.label_info_entry, text=field),
                    ttk.Entry(self.label_info_entry,
                              style=ttk.Style().theme_use('xpnative'),
                              width=60,
                              font=('Arial',12)
                              )
                    )
                
                ## TK.LABEL
                self.field_entries[field][0].config(
                    fg=COLOR_TABLA_TEXTO,
                    font=("Helvetica", 12),
                    bg=COLOR_TABLA_TITULO_FONDO,
                    width=20
                    )
                self.field_entries[field][0].pack(side=tk.LEFT)
            
                ## TK.ENTRY
                self.field_entries[field][1].pack(side=tk.LEFT, padx=10)

    def component_bar(self, field):
        self.type_dict = self.database.item_types_query()
        
        self.field_entries[field] = (
            tk.Label(self.label_info_entry, text=field.upper()),
            ttk.Combobox(self.label_info_entry, width=30, font=('Arial', 12))
            )
        
        ## TK.LABEL
        self.field_entries[field][0].config(
            fg=COLOR_TABLA_TEXTO,
            font=("Helvetica", 12, 'bold'),
            bg=COLOR_TABLA_TITULO_FONDO,
            width=18
            )
        self.field_entries[field][0].pack(side=tk.LEFT, pady=10)

        ## TK.ENTRY
        self.field_entries[field][1]['values'] = list(self.type_dict.keys())
        self.field_entries[field][1].pack(side=tk.LEFT, padx=10, pady=10)
        

    def ingresar_datos(self):
        value_dict = TEXT_FIELDS.copy()
        for column in value_dict:
            if len(self.field_entries[TEXT_FIELDS[column]][1].get()) == 0:
                value_dict[column] = None
            else:
                value_dict[column] = self.field_entries[TEXT_FIELDS[column]][1].get()            
        
        componente = self.database.Components(
            type_id = self.type_dict[value_dict['type_id']],
            brand = value_dict['brand'],
            model =	value_dict['model'],
            seller = value_dict['seller'],
            price = value_dict['price'],
            url = value_dict['url'],
            features = value_dict['features'],
            capacity = value_dict['capacity'],
            speed = value_dict['speed'],
            certification = value_dict['certification'],
            resolution = value_dict['resolution'],
            refresh = value_dict['refresh'],
            rate = value_dict['rate'],
            selected = 0
            )
        self.database.session.add(componente)
        self.database.session.commit()
            