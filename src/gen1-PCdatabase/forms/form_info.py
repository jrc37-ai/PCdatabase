import tkinter as tk
import util.util_ventana as util_ventana

class FormInfo(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.construirWidget()
    
    def config_window(self):
        self.title('Info')
        w, h = 200, 100
        util_ventana.centrar_ventana(self, w, h)
    
    def construirWidget(self):
        self.labelVersion = tk.Label(self, text="Versión: 1.0")
        self.labelVersion.config(
            fg="#000000",
            font=("Helvetica", 13),
            pady=10,
            width=20
        )
        self.labelVersion.pack()
        
        self.labelAutor = tk.Label(self, text="Autor: JRC")
        self.labelAutor.config(
            fg="#000000",
            font=("Helvetica", 13),
            pady=10,
            width=20
        )
        self.labelAutor.pack()
        