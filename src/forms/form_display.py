import tkinter as tk
from tkinter import ttk
from config import *

class FormDisplay(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        super().__init__(panel_principal)
        self.panel_principal = panel_principal
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.labelBarra = tk.Label(self.barra_superior, text="COMPONENTES")
        self.labelBarra.config(
            fg="#fff",
            font=("Helvetica", 13, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=3
        )
        self.labelBarra.pack(side=tk.TOP, fill="x", expand=False)
        self.mostrar_items()
    
    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview',
                        background=COLOR_TABLA_TEXTO_FONDO,  # Fondo oscuro para el Treeview
                        foreground=COLOR_TABLA_TEXTO,  # Texto blanco para el Treeview
                        fieldbackground=COLOR_TABLA_LIENZO,
                        font=('Arial', 10))  # Fondo del área de entrada
                        
        # Configura el estilo de los encabezados del Treeview
        style.configure('Treeview.Heading',
                        background=COLOR_TABLA_TITULO_FONDO,  # Fondo de los encabezados (gris oscuro)
                        foreground=COLOR_TABLA_TITULO_TEXTO,  # Texto de los encabezados (gris claro)
                        font=('Arial', 10, 'bold'))
                        
        # Mapear colores cuando se selecciona
        style.map('Treeview',
                  background=[('selected', COLOR_TABLA_SELECCION)],  # Fondo de las filas seleccionadas
                  foreground=[('selected', COLOR_TABLA_SELECCION_TEXTO)])  # Texto de las filas seleccionadas
        
        style.map('Treeview.Heading',
                  background=[('active', COLOR_TABLA_TITULO_SEL)],  # Fondo de los encabezados cuando se activa
                  foreground=[('active', COLOR_TABLA_TITULO_TEXSEL)])  # Texto de los encabezados cuando se activa
        
    def mostrar_items(self):
        self.configure_style()
        self.treeview = ttk.Treeview(self, columns=("size", "lastmod"))
        self.treeview.heading("#0", text="ARCHIVO")
        self.treeview.heading("size", text="TAMAÑO")
        self.treeview.heading("lastmod", text="MODIFICACIÓN")
        self.treeview.column("#0", anchor=tk.CENTER)
        self.treeview.column("size", anchor=tk.CENTER)
        self.treeview.column("lastmod", anchor=tk.CENTER)
        self.treeview.insert(
            "",
            tk.END,
            text="README.txt",
            values=("850 bytes", "18:30")
        )
        self.treeview.insert(
            "",
            tk.END,
            text="Dos.dos",
            values=("1000 bytes", "20:30")
        )
        self.treeview.pack(expand=True, fill='both')
        self.pack(expand=True, fill='both')
        