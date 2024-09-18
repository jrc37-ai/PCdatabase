import tkinter as tk
from tkinter import ttk
from database.dboperations import DBOps
from config import *

class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal, type_names) -> None:
        super().__init__(panel_principal)
        self.field_entries = {}
        self.panel_principal = panel_principal
        self.type_names = type_names
        self.top_bar()
        self.component_bar()
        self.panel_entradas()
        self.ingresar_datos()

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
        self.info_entry.pack(side=tk.TOP, fill=tk.BOTH, expand=False)      
                
        self.label_info_entry = tk.Label(self.info_entry)
        self.label_info_entry.config(
            fg="#fff",
            bg=COLOR_CUERPO_PRINCIPAL
        )
        self.label_info_entry.pack(side=tk.TOP, fill="y", expand=False)    
        self.mostrar_formulario()
        
        self.boton_add = ttk.Button(self.info_entry, text="AGREGAR", width=30)
        self.boton_add.pack(side=tk.TOP, pady=10, padx=10)
        
    def component_bar(self):
        self.barra_componente = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_componente.pack(side=tk.TOP)
        
        self.field_entries['Componente'] = (
            tk.Label(self.barra_componente, text='Componente'),
            ttk.Combobox(self.barra_componente, width=30)
            )
        self.field_entries['Componente'][0].config(
                fg=COLOR_TABLA_TEXTO,
                font=("Helvetica", 12),
                bg=COLOR_TABLA_TITULO_FONDO,
                width=20
                )
                
        self.field_entries['Componente'][1]['values'] = self.type_names
        
        self.field_entries['Componente'][0].pack(side=tk.LEFT, pady=10)
        self.field_entries['Componente'][1].pack(side=tk.LEFT, pady=10, padx=20)
    
    def ingresar_datos(self):
        for field in self.field_entries.keys():
            componente = Components(
                type_id = processor.type_id,
                brand = "Intel",
                model =	"Core i9",
                seller = "Cyberpuerta",
                price = "12500",
                url = "http://www.cyberpuerta.com",
                features =	"3.4 GHz",
                speed =	3.4,
                selected = 1
            )
            
    
    def mostrar_formulario(self):
        max_col = 4
        row = 0
        col = 0
        for field in TEXT_FIELDS:
            # self.field_entries = {
            #   'Marca': (label, entry),
            #   'Modelo': (label, entry),
            #   ...
            # }
            if field in ['URL', 'Características']:
                self.field_entries[field] = (
                    tk.Label(self.label_info_entry, text=field),
                    tk.Text(self.label_info_entry)
                )
                self.field_entries[field][1].config(width=15, height=5, )
            else:
                self.field_entries[field] = (
                    tk.Label(self.label_info_entry, text=field),
                    ttk.Entry(self.label_info_entry, style=ttk.Style().theme_use('xpnative'))
                    )
                
            ## TK.LABEL
            self.field_entries[field][0].grid(row=row, column=col, padx=5, pady=10)
            self.field_entries[field][0].config(
                fg=COLOR_TABLA_TEXTO,
                font=("Helvetica", 12),
                bg=COLOR_TABLA_TITULO_FONDO,
                width=20
                )
            
            ## TK.ENTRY
            self.field_entries[field][1].grid(row=row, column=col+1, padx=5, pady=10, ipadx=40)
                        
            col += 2
            if col >= max_col:
                col = 0
                row += 1
            