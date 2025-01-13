import tkinter as tk
from tkinter import ttk, StringVar
from rich import print
import locale

import util.util_imagen as util_imagen
from forms.form_agregar import FormAgregar

from database.dboperations import DBOps
from config import *


class FormDisplay(FormAgregar, ttk.Frame):
    def __init__(self, panel_principal) -> None:
        self.panel_principal = panel_principal
        self.img_add = util_imagen.leer_imagen("logo.jpg", (800, 500))
        self.db = DBOps()
        locale.setlocale(locale.LC_TIME, 'spanish') # Establecer la configuración regional a español

        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.labelBarra = tk.Label(self.barra_superior, text="COMPONENTES")
        self.labelBarra.config(
            fg="#fff",
            font=("Helvetica", 14, "bold"),
            bg=COLOR_BARRA_TABLA,
            height=2,
            anchor=tk.W,
            padx=20,
        )
        self.labelBarra.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if len(self.db.Components) == 0:
            self.labelnodata = tk.Label(
                self.panel_principal,
                text="AÚN NO HAY REGISTROS EN LA BASE DE DATOS",
                font=("Helvetica", 12, "italic"),
                pady=20,
                anchor=tk.N,
            )
            self.labelnodata.pack(side=tk.TOP, fill=tk.X)
        else:
            self.mostrar_botones()
            self.configurar_treeview()
            self.mostrar_items()

    def mostrar_items(self, variable=None):
        self.treeview.delete(*self.treeview.get_children())

        componentes = [
            component
            for component in self.db.Components
            if component["category"]["BD_VALUE"].upper() == variable
        ]
        if not componentes:
            componentes = self.db.Components

        index = 1
        for component in componentes:
            values = []
            for key in component:
                values += [component[key]["TREE_VALUE"]]

            highlight = (
                ("highlight",)
                if component["selected"]["TREE_VALUE"] == 1
                else ("normal",)
            )

            values = tuple(values)

            self.treeview.insert(
                parent="",
                index=index,
                iid=index,
                text="",
                tags=highlight,
                values=values,
            )
            index += 1

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

        self.treeview = ttk.Treeview(
            self.panel_principal,
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
        )

        self.columnas = [DATA_FIELDS[key]["FORM_NAME"] for key in DATA_FIELDS]

        self.treeview["columns"] = tuple(self.columnas)

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.heading("#0", text="")
        for columna in self.columnas:
            self.treeview.column(columna, anchor=tk.CENTER, width=120, stretch=tk.NO)
            self.treeview.heading(columna, text=columna)

        self.treeview.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.treeview.bind("<<TreeviewSelect>>", self.seleccion_linea)

        self.treeview.tag_configure(
            "highlight", background=COLOR_SELECCIONADO
        )  # Color de fondo para elementos marcados
        self.treeview.tag_configure(
            "normal", background=COLOR_TABLA_TEXTO_FONDO
        )  # Color de fondo para elementos no marcados

        y_scroll.config(command=self.treeview.yview)
        x_scroll.config(command=self.treeview.xview)

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview",
            background=COLOR_TABLA_TEXTO_FONDO,  # Fondo oscuro para el Treeview
            foreground=COLOR_TABLA_TEXTO,  # Texto blanco para el Treeview
            fieldbackground=COLOR_TABLA_LIENZO,
            font=("Arial", 8),
        )  # Fondo del área de entrada

        # Configura el estilo de los encabezados del Treeview
        self.style.configure(
            "Treeview.Heading",
            background=COLOR_TABLA_TITULO_FONDO,  # Fondo de los encabezados (gris oscuro)
            foreground=COLOR_TABLA_TITULO_TEXTO,  # Texto de los encabezados (gris claro)
            font=("Arial", 8),
        )

        # Mapear colores cuando se selecciona
        self.style.map(
            "Treeview",
            background=[
                ("selected", COLOR_TABLA_SELECCION)
            ],  # Fondo de las filas seleccionadas
            foreground=[("selected", COLOR_TABLA_SELECCION_TEXTO)],
        )  # Texto de las filas seleccionadas

        self.style.map(
            "Treeview.Heading",
            background=[
                ("active", COLOR_TABLA_TITULO_SEL)
            ],  # Fondo de los encabezados cuando se activa
            foreground=[("active", COLOR_TABLA_TITULO_TEXSEL)],
        )  # Texto de los encabezados cuando se activa

    def seleccion_linea(self, event):
        self.btn_editar.config(state="normal")
        self.btn_eliminar.config(state="normal")
        self.btn_marcar.config(state="normal")

        self.seleccion = event.widget.selection()
        if self.seleccion:
            self.linea = event.widget.item(self.seleccion[0], "values")
            # self.sel = event.widget.item(self.seleccion[0], tags='seleccion')

    def filtrar_componentes(self):
        cs = ttk.Style()
        cs.theme_use("vista")

        text = "FILTRAR COMPONENTE..."

        unique_types = [
            component["category"]["FORM_VALUE"].upper()
            for component in self.db.Components
        ]
        unique_types = list(set(unique_types)) + ["VER TODO"]

        max_len = [text] + unique_types
        max_len = [len(elem) for elem in max_len]
        max_len = max(max_len) + 5

        self.variable = StringVar()

        opciones = ttk.OptionMenu(
            self.labelBarra,
            self.variable,
            self.variable.set(text),
            *unique_types,
            command=self.mostrar_items
        )

        opciones["menu"].insert_separator(len(unique_types) - 1)
        opciones.config(width=max_len)
        opciones.pack(side=tk.RIGHT, padx=20, pady=18)

    def mostrar_botones(self):
        self.btn_eliminar = tk.Button(self.labelBarra)
        self.btn_eliminar.config(
            text="Eliminar",
            font=("Arial", 10, "bold"),
            borderwidth=4,
            width=10,
            relief="flat",
            overrelief="groove",
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            disabledforeground=COLOR_BARRA_TABLA,
            command=self.iniciar_resumen,
            state="disabled",
        )
        self.btn_eliminar.pack(side=tk.RIGHT, pady=10, padx=10)

        self.btn_editar = tk.Button(self.labelBarra)
        self.btn_editar.config(
            text="Editar",
            font=("Arial", 10, "bold"),
            borderwidth=4,
            width=10,
            relief="flat",
            overrelief="groove",
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            disabledforeground=COLOR_BARRA_TABLA,
            command=self.activar_panel_entradas,
            state="disabled",
        )
        self.btn_editar.pack(side=tk.RIGHT, pady=10, padx=10)

        self.btn_marcar = tk.Button(self.labelBarra)
        self.btn_marcar.config(
            text="Seleccionar",
            font=("Arial", 10, "bold"),
            borderwidth=4,
            width=10,
            relief="flat",
            overrelief="groove",
            background=BOTON_ADD_FONDO,
            foreground=BOTON_ADD_TEXTO,
            activebackground=BOTON_ADD_FONDO,
            activeforeground=BOTON_ADD_TEXTO,
            disabledforeground=COLOR_BARRA_TABLA,
            command=self.marcar_seleccion,
            state="disabled",
        )
        self.btn_marcar.pack(side=tk.RIGHT, pady=10, padx=10)

        self.filtrar_componentes()

    def activar_panel_entradas(self):
        if self.linea:
            self.seleccionado()

            self.texto_agregar = "MODIFICAR"
            self.comando = self.modificar_datos
            self.item = self.linea[0]
            self.panel_entradas()

    def iniciar_resumen(self):
        if self.linea:
            self.seleccionado()

            for key in self.TEXT_FIELDS:
                self.TEXT_FIELDS[key]["ENTRY"] = ttk.Combobox(None, width=0)
                self.TEXT_FIELDS[key]["ENTRY"].set(self.TEXT_FIELDS[key]["ENTRY_VALUE"])

            self.texto_agregar = "ELIMINAR"
            self.comando = self.eliminar_datos
            self.item = self.linea[0]
            self.mostrar_resumen()
            self.boton_editar.config(text="ATRÁS", command=self.ver_todo)
        
    def mostrar_resumen(self):
        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key]['ENTRY_VALUE'] = self.TEXT_FIELDS[key]['ENTRY'].get()
            
        self.limpiar_panel(self.panel_principal)
        self.top_bar('RESUMEN')
        
        for key in self.TEXT_FIELDS:
            frame_resumen = tk.Frame(self.panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
            frame_resumen.pack(side=tk.TOP, pady=1)

            label_resumen_campo = tk.Label(frame_resumen, text=self.TEXT_FIELDS[key]['FORM_NAME'])
            label_resumen_dato = tk.Label(frame_resumen, text=self.TEXT_FIELDS[key]['ENTRY_VALUE'])
            
            if key in ['item_id', 'selected']:
                continue
            
            label_resumen_campo.config(
                    fg=COLOR_TABLA_TEXTO,
                    font=("Helvetica", 12),
                    bg=COLOR_TABLA_TITULO_FONDO,
                    width=20
                    )
            label_resumen_campo.pack(side=tk.LEFT, padx=10)
            
            label_resumen_dato.config(
                    fg=COLOR_TABLA_TEXTO,
                    font=("Helvetica", 12),
                    bg=COLOR_TABLA_TITULO_FONDO,
                    width=40
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

    def marcar_seleccion(self):
        if self.linea:
            self.seleccionado()

            same_type = [
                component["item_id"]["BD_VALUE"]
                for component in self.db.Components
                if component["category"]["BD_VALUE"]
                == self.selected["category"]["BD_VALUE"]
            ]

            ### Todos los componentes del mismo tipo se configuran como selected = 0
            for item in same_type:
                self.db.marcar_componente(item, selected=0)

            self.db.marcar_componente(self.linea[0], selected=1)

            self.db = DBOps()
            self.mostrar_items(self.variable.get())

    def seleccionado(self):
        self.fields_reset()

        self.selected = self.db.get_one_component(self.linea[0])

        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key]["ENTRY_VALUE"] = self.selected[key]["FORM_VALUE"]
