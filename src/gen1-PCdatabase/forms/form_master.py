import tkinter as tk
from config import *

import util.util_ventana as util_ventana
import util.util_imagen as util_imagen

from forms.form_agregar import FormAgregar
from forms.form_info import FormInfo
from forms.form_display import FormDisplay
from forms.form_seleccion import FormSelect
from forms.form_imagenes import FormImagen

from database.dboperations import DBOps

class FormMasterDesign(tk.Tk):
    def __init__(self):
        super().__init__()
        self.img_add = util_imagen.leer_imagen("logo.jpg", (800,500))
        self.db_access = DBOps()
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.panel_display()

    def config_window(self):
        # Configuración inicial de la ventana
        self.title('ProyectoPC')
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)
    
    def paneles(self):
        # Creación de paneles (barra superior, menú lateral y cuerpo principal)
        self.barra_superior = tk.Frame(self, bg = COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL, width=150)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        self.labelTitulo = tk.Label(self.barra_superior, text='PROYECTO PC')
        self.labelTitulo.config(fg='#fff',
                                font=("Helvetica", 17, 'bold'),
                                bg=COLOR_BARRA_SUPERIOR,
                                pady=10,
                                width=16)
        self.labelTitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        ancho_menu = 16
        alto_menu = 2

        self.buttonAdd = tk.Button(self.menu_lateral)
        self.buttonDisplay = tk.Button(self.menu_lateral)
        self.buttonBuild = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Componente (+) ", self.buttonAdd, self.panel_agregar),
            ("Ver TODO", self.buttonDisplay, self.panel_display),
            ("Ver SELECCIÓN ", self.buttonBuild, self.panel_select)
        ]

        for text, button, comando in buttons_info:
            self.configurar_boton_menu(button, text, ancho_menu, alto_menu, comando)
            
        self.buttonInfo.config(
            text="( i )",
            anchor='center',
            font=('Helvetica', 12),
            bd=0,
            bg=COLOR_MENU_LATERAL,
            fg='white',
            width=ancho_menu,
            height=alto_menu, 
            command=self.abrir_panel_info
            )
        self.buttonInfo.pack(side=tk.BOTTOM)
        self.bind_hover_events(self.buttonInfo)
        
    def configurar_boton_menu(self, button, text, ancho_menu, alto_menu, comando):
        button.config(text=text,
                      anchor="e",
                      font=('Helvetica', 12),
                      bd=0,
                      bg=COLOR_MENU_LATERAL,
                      fg='white',
                      width=ancho_menu,
                      height=alto_menu, 
                      command=comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)
    
    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))
    
    def on_enter(self, event, button):
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')
    
    def on_leave(self, event, button):
        button.config(bg=COLOR_MENU_LATERAL, fg='white')
    
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
    
    def panel_agregar(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormAgregar(self.cuerpo_principal, self.db_access)
    
    def panel_display(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormDisplay(self.cuerpo_principal)
    
    def abrir_panel_info(self):
        FormInfo()
    
    def panel_select(self):
        self.limpiar_panel(self.cuerpo_principal)
        # FormImagen(self.cuerpo_principal, self.img_add)
        FormSelect(self.cuerpo_principal)
        
    # def panel_edit(self):
    #     self.limpiar_panel(self.cuerpo_principal)
    #     FormImagen(self.cuerpo_principal, self.img_add)

        