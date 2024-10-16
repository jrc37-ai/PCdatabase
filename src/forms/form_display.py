import tkinter as tk
from tkinter import ttk

from sqlalchemy.orm import Session

from forms.form_agregar import FormAgregar
from database.modelos import ComponentModel
from database.dboperations import DBOps
from config import *

class FormDisplay(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        super().__init__(panel_principal)
        self.panel_principal = panel_principal
        self.db = DBOps()
        
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.labelBarra = tk.Label(self.barra_superior, text="COMPONENTES")
        self.labelBarra.config(
            fg="#fff",
            font=("Helvetica", 14, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=2,
            anchor=tk.W,
            padx=20
        )
        self.labelBarra.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.mostrar_botones()
        self.mostrar_items()
    
    def mostrar_items(self):
        self.configurar_treeview()             
        
        for index, componente in enumerate(self.db.Components):
            values = []
            for columna in ComponentModel.__table__.columns:
                if columna.foreign_keys:
                    values += [componente.item_type.name]
                else:
                    values += [getattr(componente, columna.name)]
            values = tuple(values)
            
            self.treeview.insert(
                parent='',
                index=index,
                iid=index,
                text='',
                values=values
                )
        
    def configurar_treeview(self):
        self.configure_style()
        
        y_scroll = ttk.Scrollbar(self.panel_principal)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        frame_xscroll = ttk.Frame(self.panel_principal, height=1)
        frame_xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        x_scroll = ttk.Scrollbar(frame_xscroll, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.TOP, fill=tk.X)
        label_xscroll_down = ttk.Label(frame_xscroll)
        label_xscroll_down.pack(side=tk.TOP, fill=tk.X)
        
        self.treeview = ttk.Treeview(self.panel_principal,
                                     show='headings',
                                     yscrollcommand=y_scroll.set,
                                     xscrollcommand=x_scroll.set
                                     )
        
        columnas = ['Item']
        for columna in DATA_FIELDS:
            columnas += [columna]
        self.treeview['columns'] = tuple(columnas)
                    
        self.treeview.column('#0', width=0, stretch=tk.NO)
        self.treeview.heading('#0', text='')
        for columna in columnas:
            self.treeview.column(columna, anchor=tk.CENTER, width=120, stretch=tk.NO)
            self.treeview.heading(columna, text=columna)
        
        self.treeview.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.treeview.bind("<<TreeviewSelect>>", self.seleccion_linea)
        
        y_scroll.config(command=self.treeview.yview)
        x_scroll.config(command=self.treeview.xview)
    
    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview',
                        background=COLOR_TABLA_TEXTO_FONDO,  # Fondo oscuro para el Treeview
                        foreground=COLOR_TABLA_TEXTO,  # Texto blanco para el Treeview
                        fieldbackground=COLOR_TABLA_LIENZO,
                        font=('Arial', 8))  # Fondo del área de entrada
                        
        # Configura el estilo de los encabezados del Treeview
        style.configure('Treeview.Heading',
                        background=COLOR_TABLA_TITULO_FONDO,  # Fondo de los encabezados (gris oscuro)
                        foreground=COLOR_TABLA_TITULO_TEXTO,  # Texto de los encabezados (gris claro)
                        font=('Arial', 8))
                        
        # Mapear colores cuando se selecciona
        style.map('Treeview',
                  background=[('selected', COLOR_TABLA_SELECCION)],  # Fondo de las filas seleccionadas
                  foreground=[('selected', COLOR_TABLA_SELECCION_TEXTO)])  # Texto de las filas seleccionadas
        
        style.map('Treeview.Heading',
                  background=[('active', COLOR_TABLA_TITULO_SEL)],  # Fondo de los encabezados cuando se activa
                  foreground=[('active', COLOR_TABLA_TITULO_TEXSEL)])  # Texto de los encabezados cuando se activa
        
    def seleccion_linea(self, event):                
        self.btn_editar.config(state='normal')
        self.btn_eliminar.config(state='normal')
        
        seleccion = event.widget.selection()
        if seleccion:
            self.item = event.widget.item(seleccion[0], 'values')
    
    def mostrar_botones(self):
        self.btn_eliminar = tk.Button(self.labelBarra)
        self.btn_eliminar.config(
            text='Eliminar',
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
            command=self.eliminar_registro,
            state='disabled'
            )
        self.btn_eliminar.pack(side=tk.RIGHT, pady=10, padx=10)
        
        self.btn_editar = tk.Button(self.labelBarra)
        self.btn_editar.config(
            text='Editar',
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
            command=self.activar_panel_entradas,
            state='disabled'
            )
        self.btn_editar.pack(side=tk.RIGHT, pady=10, padx=10)
    
    def activar_panel_entradas(self):
        if self.item:
            self.entradas = FormAgregar(panel_principal=self.panel_principal,
                                        db_access=self.db)
            self.entradas.fields_reset()
            
            i = 1
            for key in self.entradas.TEXT_FIELDS:
                self.entradas.TEXT_FIELDS[key]['ENTRY_VALUE'] = self.item[i]
                i += 1
            
            self.entradas.combobox = [
                type.type_id-1
                for type in self.db.Item_types
                if type.name == self.entradas.TEXT_FIELDS['COMPONENTE']['ENTRY_VALUE']
                ][0]
            
        self.entradas.texto_agregar = 'MODIFICAR'
        self.entradas.comando = self.entradas.modificar_datos
        self.entradas.item = self.item[0]
        self.entradas.panel_entradas()
            
    def eliminar_registro(self):        
        pass