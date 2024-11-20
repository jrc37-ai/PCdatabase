import tkinter as tk
from config import *

class FormImagen():
    def __init__(self, panel_principal, imagen) -> None:
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)
        
        self.labelTitulo = tk.Label(self.barra_superior, text="Página")
        self.labelTitulo.config(
            fg="#222d33",
            font=("Helvetiva", 13),
            bg=COLOR_CUERPO_PRINCIPAL
        )
        self.labelTitulo.pack(side=tk.TOP, fill="both", expand=True)
        
        self.label_Imagen = tk.Label(self.barra_inferior, image=imagen)
        self.label_Imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_Imagen.config(
            fg="#fff",
            font=("Helvetiva", 13),
            bg=COLOR_CUERPO_PRINCIPAL
        )
        self.label_Imagen.pack(side=tk.TOP, fill="both", expand=True)