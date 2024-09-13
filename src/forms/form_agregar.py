import tkinter as tk
from tkinter import ttk
from config import *

class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        super().__init__(panel_principal)
        self.panel_principal = panel_principal

        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.barra_lateral = tk.Frame(self.panel_principal)
        self.barra_lateral.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        
        self.label_barra_superior = tk.Label(self.barra_superior, text="CREAR NUEVO TIPO")
        self.label_barra_superior.config(
            fg="#fff",
            font=("Helvetica", 13, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=3
        )
        self.label_barra_superior.pack(side=tk.TOP, fill="x", expand=False)

        self.label_barra_lateral = tk.Label(self.barra_lateral)
        self.label_barra_lateral.config(
            fg="#fff",
            bg=COLOR_BARRA_TABLA
        )
        self.label_barra_lateral.pack(side=tk.LEFT, fill="y", expand=False)

        self.mostrar_formulario()
        

    def mostrar_formulario(self):
        # campo_textos = [
        #     'Marca',
        #     'Modelo',
            
        # ]


        # label_brand = tk.Label(self.label_barra_lateral, text='Marca')
        # label_brand.config(
        #     fg=COLOR_TABLA_TEXTO,
        #     font=("Helvetica", 12),
        #     bg=COLOR_TABLA_TITULO_FONDO,
        #     width=10
        # )
        # label_brand.pack(side=tk.TOP, padx=5, pady=10)

        # self.campo_brand = tk.Entry(self.barra_lateral)
        # self.campo_brand.configure(
        #     fg=COLOR_TABLA_TEXTO,
        #     font=("Helvetica", 12),
        #     bg=COLOR_TABLA_TITULO_FONDO, 
        #     width=15
        # )
        # self.campo_brand.pack(side=tk.TOP, padx=5, pady=12)



        ########################## MARCA
        label_brand = tk.Label(self.label_barra_lateral, text='Marca')
        label_brand.config(
            fg=COLOR_TABLA_TEXTO,
            font=("Helvetica", 12),
            bg=COLOR_TABLA_TITULO_FONDO,
            width=10
        )
        label_brand.pack(side=tk.TOP, padx=5, pady=10)

        self.campo_brand = tk.Entry(self.barra_lateral)
        self.campo_brand.configure(
            fg=COLOR_TABLA_TEXTO,
            font=("Helvetica", 12),
            bg=COLOR_TABLA_TITULO_FONDO, 
            width=15
        )
        self.campo_brand.pack(side=tk.TOP, padx=5, pady=12)

        ########################## MODELO
        label_model = tk.Label(self.label_barra_lateral, text='Modelo')
        label_model.config(
            fg=COLOR_TABLA_TEXTO,
            font=("Helvetica", 12),
            bg=COLOR_TABLA_TITULO_FONDO,
            width=10
        )
        label_model.pack(side=tk.TOP, padx=5, pady=10)

        self.campo_model = tk.Entry(self.barra_lateral)
        self.campo_model.configure(
            fg=COLOR_TABLA_TEXTO,
            font=("Helvetica", 12),
            bg=COLOR_TABLA_TITULO_FONDO,
            width=15
        )
        self.campo_model.pack(side=tk.TOP, padx=5, pady=12)
        