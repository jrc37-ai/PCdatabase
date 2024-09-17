import tkinter as tk
from tkinter import ttk
from config import *

class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        super().__init__(panel_principal)
        self.panel_principal = panel_principal

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
        
        self.boton_add_frame = tk.Frame(self.label_barra_superior)
        self.boton_add_frame.pack(side=tk.RIGHT)
        self.boton_add = tk.Button(self.boton_add_frame, text="AGREGAR")
        self.boton_add.pack(side=tk.RIGHT, fill='y')

        self.info_entry = tk.Frame(self.panel_principal)
        self.info_entry.pack(side=tk.TOP, fill=tk.Y, expand=False)
        self.label_info_entry = tk.Label(self.info_entry)
        self.label_info_entry.config(
            fg="#fff",
            bg=COLOR_CUERPO_PRINCIPAL
        )
        self.label_info_entry.pack(side=tk.TOP, fill="y", expand=False)

        self.mostrar_formulario()
        

    def mostrar_formulario(self):
        text_fields = [
            'Marca',
            'Modelo',
            'Tienda',
            'Precio',
            'URL',
            'Características',
            'Capacidad',
            'Velocidad',
            'Certificación',
            'Resolución',
            'Tasa de refresco',
            'Calificación'
        ]

        max_col = 4
        row = 0
        col = 0
        self.field_entries = {}
        for field in text_fields:
            # self.field_entries = {
            #   'Marca': (label, entry),
            #   'Modelo': (label, entry),
            #   ...
            # }
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
            # self.field_entries[field][1].configure(
            #     fg=COLOR_TABLA_TEXTO,
            #     font=("Helvetica", 12),
            #     bg=COLOR_TABLA_TITULO_FONDO,     
            #     width=20
            #     )
            
            col += 2
            if col >= max_col:
                col = 0
                row += 1
            