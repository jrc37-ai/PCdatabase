import tkinter as tk
from tkinter import ttk

from config import *

class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal, db_access) -> None:
        super().__init__(panel_principal)
        self.field_entries = {}
        self.panel_principal = panel_principal
        self.db = db_access
        self.item = None
        self.texto_agregar = 'AGREGAR'
        self.comando = self.ingresar_datos
        self.fields_reset()
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
        self.info_entry.pack(expand=False, pady=10)
                
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
        for key in self.TEXT_FIELDS:
            self.label_info_entry = tk.Frame(self.info_entry, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_info_entry.pack(side=tk.TOP, fill=tk.X, pady=1)

            if key in ['COMPONENTE']:
                font = ("Helvetica", 12, 'bold')
                self.TEXT_FIELDS[key]['ENTRY'] = ttk.Combobox(self.label_info_entry, width=30, font=('Arial', 12))
                self.TEXT_FIELDS[key]['ENTRY']['values'] = [type.name for type in self.db.Item_types]
                self.TEXT_FIELDS[key]['ENTRY'].set(self.TEXT_FIELDS[key]['ENTRY']['values'][self.combobox])
            else:
                font = ("Helvetica", 12)
                self.TEXT_FIELDS[key]['ENTRY'] = ttk.Entry(self.label_info_entry,
                                        style=ttk.Style().theme_use('xpnative'),
                                        width=60,
                                        font=('Arial',12)
                                        )
                self.TEXT_FIELDS[key]['ENTRY'].insert(0,self.TEXT_FIELDS[key]['ENTRY_VALUE'])
            
            self.TEXT_FIELDS[key]['LABEL'] = tk.Label(self.label_info_entry, text=key)
            self.TEXT_FIELDS[key]['LABEL'].config(
                fg=COLOR_TABLA_TEXTO,
                font=font,
                bg=COLOR_TABLA_TITULO_FONDO,
                width=20
                )              
               
            self.TEXT_FIELDS[key]['LABEL'].pack(side=tk.LEFT)
            self.TEXT_FIELDS[key]['ENTRY'].pack(side=tk.LEFT, padx=10)
        
    def mostrar_resumen(self):
        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key]['ENTRY_VALUE'] = self.TEXT_FIELDS[key]['ENTRY'].get()
            # if len(self.TEXT_FIELDS[key]['ENTRY_VALUE']) == 0:
            #     self.TEXT_FIELDS[key]['BD_VALUE'] = None
            # else:
            #     self.TEXT_FIELDS[key]['BD_VALUE'] = self.TEXT_FIELDS[key]['ENTRY_VALUE']

        self.limpiar_panel(self.panel_principal)
        
        self.top_bar('RESUMEN')
        
        for key in self.TEXT_FIELDS:
            frame_resumen = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
            frame_resumen.pack(side=tk.TOP, pady=1)

            label_resumen_campo = tk.Label(frame_resumen, text=key)
            label_resumen_dato = tk.Label(frame_resumen, text=self.TEXT_FIELDS[key]['ENTRY_VALUE'])
            
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
        self.combobox = [
            type.type_id-1
            for type in self.db.Item_types
            if type.name == self.TEXT_FIELDS['COMPONENTE']['ENTRY_VALUE']
            ][0]
               
        self.boton_agregar = tk.Button(frame_botones)
        self.boton_agregar.config(
            text=self.texto_agregar, # AGREGAR O MODIFICAR
            font=('Arial', 12, 'bold'),
            borderwidth=4,
            width=40,
            relief='flat',
            overrelief='groove',
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            command=self.comando,
        )
        self.boton_agregar.pack(side=tk.LEFT, padx=10)
        
    def ingresar_datos(self):
        element = {
            self.TEXT_FIELDS[key]['BD_NAME']:
            self.TEXT_FIELDS[key]['ENTRY_VALUE']
            for key in self.TEXT_FIELDS
            }
        
        componente = self.db.to_database(element)
        
        # componente = {
        #     'type_id': [
        #         type.type_id
        #         for type in self.db.Item_types
        #         if type.name == self.TEXT_FIELDS['COMPONENTE']['BD_VALUE']
        #         ][0],
        #     'brand': self.TEXT_FIELDS['Marca']['BD_VALUE'],
        #     'model': self.TEXT_FIELDS['Modelo']['BD_VALUE'],
        #     'seller': self.TEXT_FIELDS['Tienda']['BD_VALUE'],
        #     'price': self.TEXT_FIELDS['Precio']['BD_VALUE'],
        #     'url': self.TEXT_FIELDS['URL']['BD_VALUE'],
        #     'features': self.TEXT_FIELDS['Características']['BD_VALUE'],
        #     'capacity': self.TEXT_FIELDS['Capacidad']['BD_VALUE'],
        #     'speed': self.TEXT_FIELDS['Velocidad']['BD_VALUE'],
        #     'certification': self.TEXT_FIELDS['Certificación']['BD_VALUE'],
        #     'resolution': self.TEXT_FIELDS['Resolución']['BD_VALUE'],
        #     'refresh': self.TEXT_FIELDS['Tasa de refresco']['BD_VALUE'],
        #     'rate': self.TEXT_FIELDS['Calificación']['BD_VALUE'],
        #     'selected': 0
        # }

        self.db.registrar_componente(**componente)
        
        self.boton_editar.config(
            text='NUEVO (+)',
            )
        
        self.fields_reset()
                
        self.boton_agregar.config(
            text='AGREGADO',
            background=BOTON_DISABLED,
            disabledforeground=BOTON_DISABLED_TEXTO,
            state=tk.DISABLED
        )       

    def modificar_datos(self):
        element = {
            self.TEXT_FIELDS[key]['BD_NAME']:
            self.TEXT_FIELDS[key]['ENTRY_VALUE']
            for key in self.TEXT_FIELDS
            }
        
        componente = self.db.to_database(element)

        # componente = {
        #     'type_id': [
        #         type.type_id
        #         for type in self.db.Item_types
        #         if type.name == self.TEXT_FIELDS['COMPONENTE']['BD_VALUE']
        #         ][0],
        #     'brand': self.TEXT_FIELDS['Marca']['BD_VALUE'],
        #     'model': self.TEXT_FIELDS['Modelo']['BD_VALUE'],
        #     'seller': self.TEXT_FIELDS['Tienda']['BD_VALUE'],
        #     'price': self.TEXT_FIELDS['Precio']['BD_VALUE'],
        #     'url': self.TEXT_FIELDS['URL']['BD_VALUE'],
        #     'features': self.TEXT_FIELDS['Características']['BD_VALUE'],
        #     'capacity': self.TEXT_FIELDS['Capacidad']['BD_VALUE'],
        #     'speed': self.TEXT_FIELDS['Velocidad']['BD_VALUE'],
        #     'certification': self.TEXT_FIELDS['Certificación']['BD_VALUE'],
        #     'resolution': self.TEXT_FIELDS['Resolución']['BD_VALUE'],
        #     'refresh': self.TEXT_FIELDS['Tasa de refresco']['BD_VALUE'],
        #     'rate': self.TEXT_FIELDS['Calificación']['BD_VALUE'],
        #     'selected': 0
        # }
        
        self.db.modificar_componente(self.item, **componente)
        
        self.boton_editar.config(
            text='VER TODO'
            )
        
        self.fields_reset()
                
        self.boton_agregar.config(
            text='MODIFICADO',
            background=BOTON_DISABLED,
            disabledforeground=BOTON_DISABLED_TEXTO,
            state=tk.DISABLED
        )       
            
    def fields_reset(self):
         # Reiniciar los valores de los entry a None
        self.TEXT_FIELDS = DATA_FIELDS.copy()
        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key] = DATA_FIELDS[key].copy()
        self.combobox = 0
        
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
    