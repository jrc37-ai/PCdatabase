import tkinter as tk
from tkinter import ttk
import pandas as pd
from database.dboperations import DBOps
from config import *


class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal, database, type_dict) -> None:
        super().__init__(panel_principal)
        self.field_entries = {}
        self.panel_principal = panel_principal
        self.database = database
        self.type_dict = type_dict
        self.text_fields = pd.DataFrame(
            TEXT_FIELDS,
            columns= list(TEXT_FIELDS.keys()) + ['BD_VALUE', 'ENTRY_VALUE']
            )
        print(self.text_fields)
        self.top_bar()
        self.panel_entradas()

    def top_bar(self, text='AGREGAR COMPONENTE'):
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.label_barra_superior = tk.Label(self.barra_superior, text=text)
        self.label_barra_superior.config(
            fg="#fff",
            font=("Helvetica", 13, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=3
        )
        self.label_barra_superior.pack(side=tk.TOP, fill="x", expand=False)
        
    def panel_entradas(self):
        self.limpiar_panel(self.panel_principal)
        self.info_entry = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.info_entry.pack(expand=False)
                
        self.mostrar_formulario()
        
        self.boton_continuar = tk.Button(self.info_entry)
        self.boton_continuar.config(
            text='CONTINUAR',
            font=('Arial', 12, 'bold'),
            borderwidth=4,
            width=40,
            relief='flat',
            overrelief='groove',
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            command=self.mostrar_resumen
            )
        self.boton_continuar.pack(side=tk.TOP, pady=10)
        
    def mostrar_formulario(self):
        for bd_name in TEXT_FIELDS['BD_NAME']:
            # self.field_entries = {
            #   'Marca': (label, entry),
            #   'Modelo': (label, entry),
            #   ...
            # }
            field = TEXT_FIELDS[key]
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
                              font=('Arial',12),
                              )
                    )
                self.field_entries[field][1].insert(0,self.value_dict[key])

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
        
    def mostrar_resumen(self):
        for column in self.value_dict:
            if len(self.field_entries[TEXT_FIELDS[column]][1].get()) == 0:
                self.value_dict[column] = ""
            else:
                self.value_dict[column] = self.field_entries[TEXT_FIELDS[column]][1].get()
                
        self.limpiar_panel(self.panel_principal)
        
        self.top_bar('RESUMEN')
                
        for field in self.value_dict:
            frame_resumen = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
            frame_resumen.pack(side=tk.TOP, pady=1)

            label_resumen_campo = tk.Label(frame_resumen, text=TEXT_FIELDS[field])
            label_resumen_dato = tk.Label(frame_resumen, text=self.value_dict[field])
            
            label_resumen_campo.config(
                    fg=COLOR_TABLA_TEXTO,
                    font=("Helvetica", 12),
                    bg=COLOR_TABLA_TITULO_FONDO,
                    width=20
                    )
            label_resumen_campo.pack(side=tk.LEFT)
            
            label_resumen_dato.config(
                    fg=COLOR_TABLA_TEXTO,
                    font=("Helvetica", 12),
                    bg=COLOR_TABLA_TITULO_FONDO,
                    width=20
                    )
            label_resumen_dato.pack(side=tk.LEFT)

        frame_botones = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        frame_botones.pack(side=tk.TOP, pady=10)
        
        self.boton_editar = tk.Button(frame_botones)
        self.boton_editar.config(
            text='EDITAR',
            font=('Arial', 12, 'bold'),
            borderwidth=4,
            width=40,
            relief='flat',
            overrelief='groove',
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            command=self.panel_entradas
            )
        self.boton_editar.pack(side=tk.LEFT)
        
        self.boton_agregar = tk.Button(frame_botones)
        self.boton_agregar.config(
            text='AGREGAR',
            font=('Arial', 12, 'bold'),
            borderwidth=4,
            width=40,
            relief='flat',
            overrelief='groove',
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            command=self.ingresar_datos,
        )
        self.boton_agregar.pack(side=tk.LEFT, padx=10)
        
    def ingresar_datos(self):
        componente = self.database.Components(
            type_id = self.type_dict[self.value_dict['type_id']],
            brand = self.value_dict['brand'],
            model =	self.value_dict['model'],
            seller = self.value_dict['seller'],
            price = self.value_dict['price'],
            url = self.value_dict['url'],
            features = self.value_dict['features'],
            capacity = self.value_dict['capacity'],
            speed = self.value_dict['speed'],
            certification = self.value_dict['certification'],
            resolution = self.value_dict['resolution'],
            refresh = self.value_dict['refresh'],
            rate = self.value_dict['rate'],
            selected = 0
            )
        self.database.session.add(componente)
        self.database.session.commit()
        
        self.boton_editar.config(
            text='NUEVO (+)',
            )
        self.value_dict = {key:"" for key in TEXT_FIELDS.keys()}
        
        self.boton_agregar.config(
            text='AGREGADO',
            background=BOTON_DISABLED,
            disabledforeground=BOTON_DISABLED_TEXTO,
            state=tk.DISABLED
        )       
    
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
    