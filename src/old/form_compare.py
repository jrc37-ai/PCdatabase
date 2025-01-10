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
            self.boton_marcar()
            self.mostrar_opciones()
            self.configurar_treeview()
        
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
        
        self.variable = StringVar()
        
        opciones = ttk.OptionMenu(
            self.labelBarra,
            self.variable,
            self.variable.set(text),
            *unique_types,
            command=self.compare_components
        )

        opciones.config(width=max_len)
        opciones.pack(side=tk.RIGHT, padx=20, pady=18)

    def compare_components(self, variable):
        self.treeview.delete(*self.treeview.get_children())
        
        componentes = [component for component in self.db.Components if
                         component["category"]["BD_VALUE"].upper() == variable]

        index = 1
        for component in componentes:
            values = []
            for key in component:
                values += [component[key]['FORM_VALUE']]
            
            highlight = ('highlight',) if component['selected']['FORM_VALUE'] == 1 else ('normal',)
            
            values = tuple(values)
            
            self.treeview.insert(
                parent='',
                index=index,
                iid=index,
                text='',
                tags=highlight,
                values=values
                )
            index += 1
    
    def seleccion_linea(self, event):                
        self.btn_marcar.config(state='normal')
        
        self.seleccion = event.widget.selection()
        if self.seleccion:
            self.linea = event.widget.item(self.seleccion[0], 'values')

    def marcar_seleccion(self):
        if self.linea:
            self.seleccionado()     
            
            same_type = [component['item_id']['BD_VALUE'] for
                            component in self.db.Components
                         if component['category']['BD_VALUE'] ==
                            self.TEXT_FIELDS['category']['ENTRY_VALUE']
                         ]
            
            for item in same_type: ### Todos los componentes del mismo tipo se configurar como selected = 0
                self.db.marcar_componente(item, selected=0)
            
            self.db.marcar_componente(self.linea[0], selected=1)
        
        self.db.Components = self.db.get_components()
        self.compare_components(self.variable.get())
    
    def boton_marcar(self):
        self.btn_marcar = tk.Button(self.labelBarra)
        self.btn_marcar.config(
            text='Seleccionar',
            font=('Arial', 10, 'bold'),
            borderwidth=4,
            width=10,
            relief='flat',
            overrelief='groove',
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            disabledforeground=COLOR_BARRA_TABLA,
            command=self.marcar_seleccion,
            state='disabled'
            )
        self.btn_marcar.pack(side=tk.RIGHT, pady=10, padx=10)
