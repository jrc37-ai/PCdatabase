import tkinter as tk
from tkinter import ttk
from rich import print

from database.dboperations import DBOps
from config import *

class FormResultado(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        self.panel_principal = panel_principal
        self.db = DBOps()

        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.titulo = tk.Label(self.barra_superior, text="RESULTADO")
        self.titulo.config(
            fg=BLANCO,
            font=("Helvetica", 14, 'bold'),
            bg=BG_LABEL_RESULTADO,
            height=2,
            anchor=tk.W,
            padx=20
        )
        self.titulo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.barra_lateral = tk.Frame(self.panel_principal)
        self.barra_lateral.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        
        self.menu_lateral = tk.Label(self.barra_lateral)
        self.menu_lateral.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.barra_costo = tk.Frame(self.panel_principal)
        self.barra_costo.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.suma_num = 0
        self.suma_tex = f"COSTO TOTAL:  ${self.suma_num:,.2f}"
        self.label_costo = tk.Label(self.barra_costo)
        self.label_costo.config(
            text=self.suma_tex,
            fg=NEGRO,
            font=("Helvetica", 14, 'bold'),
            bg=BLANCO,
            height=2,
            anchor=tk.CENTER,
            padx=20
        )
        self.label_costo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.menu_tipos()
        self.configurar_treeview()
    
    def menu_tipos(self):
        self.tipos = [component['category']['BD_VALUE'] for 
                      component in self.db.Components 
                      if component['selected']['BD_VALUE'] == 1]
        self.tipos = list(set(self.tipos))
        
        self.checkbutton_style()

        self.checkbuttons_vars = [tk.StringVar() for tipo in self.tipos]
        checkbuttons = []
        for index, tipo in enumerate(self.tipos):
            checkbutton = ttk.Checkbutton(self.menu_lateral,
                                          text=str(tipo).upper(),
                                          onvalue=tipo,
                                          offvalue='',
                                          style='Toolbutton',
                                          cursor='hand2',
                                          variable=self.checkbuttons_vars[index],
                                          command=self.mostrar_elementos)
            checkbutton.pack(side=tk.TOP, fill=tk.X, expand=False)
            checkbuttons.append(checkbutton)
    
    def mostrar_elementos(self):
        self.treeview.delete(*self.treeview.get_children())
        
        checked = [var.get() for var in self.checkbuttons_vars if var.get()]
        
        checked_dict = [component for component in self.db.Components 
                         if component['category']['BD_VALUE'] in checked]
        
        self.selected = [component for component in checked_dict 
                         if component['selected']['BD_VALUE'] == 1]
        
        index = 1     
        for component in self.selected:
            values = [component[key]['TREE_VALUE']
                      for key in component
                      if component[key]['FORM_NAME'] in self.columnas]    
            
            values = tuple(values)

            self.treeview.insert(
                parent='',
                index=index,
                iid=index,
                text='',
                values=values
                )
            index += 1
        
        self.costo_total()
    
    def costo_total(self):
        self.suma_num = sum([component['price']['BD_VALUE'] for component in self.selected])
        self.suma_tex = f"COSTO TOTAL:  ${self.suma_num:,.2f}"
        
        self.label_costo.config(text=self.suma_tex)

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
            show='headings',
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        
        self.columnas = [
            'CATEGORÍA',
            'MARCA',
            'MODELO',
            'PRECIO',
            'TIENDA'
        ]
        self.treeview['columns'] = tuple(self.columnas)
        
        width = self.panel_principal.winfo_width()
        width = width//len(self.columnas)      

        self.treeview.column('#0', width=0, stretch=tk.NO)
        self.treeview.heading('#0', text='')
        for columna in self.columnas:
            self.treeview.column(columna, anchor=tk.CENTER, stretch=True, width=width-22)
            self.treeview.heading(columna, text=columna)
        
        self.treeview.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
    
        # self.treeview.tag_configure("normal", background=COLOR_TABLA_TEXTO_FONDO) # Color de fondo para elementos no marcados
        
        y_scroll.config(command=self.treeview.yview)
        x_scroll.config(command=self.treeview.xview)
    
    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('Treeview',
                        background=COLOR_TABLA_TEXTO_FONDO,  
                        foreground=NEGRO,  
                        fieldbackground=COLOR_TABLA_LIENZO,
                        font=('Helvetica', 10)
                    )  
                        
        # Configura el estilo de los encabezados del Treeview
        self.style.configure('Treeview.Heading',
                        background=BG_HEADING_RESULTADO,  # Fondo de los encabezados
                        foreground=BLANCO,  # Texto de los encabezados
                        font=('Helvetica', 10, 'bold')
                    )
        
        self.style.map('Treeview.Heading',
                  background=[('active', BG_HEAD_ACT_RESULTADO)],  # Fondo de los encabezados cuando se activa
                  foreground=[('active', FG_HEAD_ACT_RESULTADO)]   # Texto de los encabezados cuando se activa
                ) 
        
    def checkbutton_style(self):
        self.chk = ttk.Style()
        
        self.chk.configure("Toolbutton", anchor=tk.CENTER)
        self.chk.map(
            "Toolbutton",
            indicatorbackground=[("active", BLANCO)],
            background=[("active", AZUL), ("selected", VERDE)],
            foreground=[("active", BLANCO), ("selected", BLANCO)],
        )
