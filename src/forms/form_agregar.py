import tkinter as tk
from tkinter import ttk
from datetime import date
import locale

from database.dboperations import DBOps

from config import *

class FormAgregar(ttk.Frame):
    def __init__(self, panel_principal) -> None:
        super().__init__(panel_principal)
        locale.setlocale(locale.LC_TIME, 'spanish') # Establecer la configuración regional a español (España)
        self.field_entries = {}
        self.panel_principal = panel_principal
        self.db = DBOps()
        self.item = None
        self.texto_agregar = 'AGREGAR'
        self.comando = self.ingresar_datos
        self.fields_reset()
        self.panel_entradas()

    def top_bar(self, text='AGREGAR COMPONENTE'):
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        
        self.label_barra_superior = tk.Label(self.barra_superior, text=text)
        self.label_barra_superior.config(
            fg="#fff",
            font=("Helvetica", 14, 'bold'),
            bg=COLOR_BARRA_TABLA,
            height=2,
            anchor=tk.W,
            padx=20
        )
        self.label_barra_superior.pack(side=tk.LEFT, fill="x", expand=True)
        
    def panel_entradas(self):
        self.limpiar_panel(self.panel_principal)
        self.top_bar()
        
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
        style = ttk.Style()
        style.theme_settings("xpnative", {
            "TEntry": {
                "map": {
                    "foreground": [('disabled', "black")]
                    }
                }
            })
            
        style.theme_use("xpnative")
                
        for key in self.TEXT_FIELDS:  
            self.label_info_entry = tk.Frame(self.info_entry, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_info_entry.pack(side=tk.TOP, fill=tk.X, pady=1)
          
            self.TEXT_FIELDS[key]['ENTRY'] = ttk.Entry(self.label_info_entry,
                                    width=60,
                                    font=('Arial',12),
                                    style='xpnative.TEntry'
                                    )
            
            if key in ['date']:
                self.TEXT_FIELDS[key]['ENTRY'].insert(0, date.today().strftime("%d/%B/%Y"))
                
                self.TEXT_FIELDS[key]['ENTRY'].config(state=tk.DISABLED)
            else:
                self.TEXT_FIELDS[key]['ENTRY'].insert(0, self.TEXT_FIELDS[key]['ENTRY_VALUE'])
            
            text = self.TEXT_FIELDS[key]['FORM_NAME']
            self.TEXT_FIELDS[key]['LABEL'] = tk.Label(self.label_info_entry, text=text)
            self.TEXT_FIELDS[key]['LABEL'].config(
                fg=COLOR_TABLA_TEXTO,
                font=("Helvetica", 12),
                bg=COLOR_TABLA_TITULO_FONDO,
                width=20
                )              
            
            if key in ['item_id', 'selected']:
                continue
            
            self.TEXT_FIELDS[key]['LABEL'].pack(side=tk.LEFT)
            self.TEXT_FIELDS[key]['ENTRY'].pack(side=tk.LEFT, padx=10)
        
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
        
    def ingresar_datos(self):
        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key]['BD_VALUE'] = self.TEXT_FIELDS[
                key]['ENTRY_VALUE'] if self.TEXT_FIELDS[
                    key]['ENTRY_VALUE'] != "" else None 

        self.db.registrar_componente(**self.TEXT_FIELDS)
        
        self.boton_editar.config(
            text='NUEVO (+)'
            )
        
        self.fields_reset()
                
        self.boton_agregar.config(
            text='AGREGADO',
            background=BOTON_DISABLED,
            disabledforeground=BOTON_DISABLED_TEXTO,
            state=tk.DISABLED
        )       

    def modificar_datos(self):
        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key]['BD_VALUE'] = self.TEXT_FIELDS[
                key]['ENTRY_VALUE'] if self.TEXT_FIELDS[
                    key]['ENTRY_VALUE'] != "" else None 
      
        self.db.modificar_componente(self.item, **self.TEXT_FIELDS)
        
        self.boton_editar.config(
            text='VER TODO',
            command=self.ver_todo
            )
        
        self.fields_reset()
                
        self.boton_agregar.config(
            text='MODIFICADO',
            background=BOTON_DISABLED,
            disabledforeground=BOTON_DISABLED_TEXTO,
            state=tk.DISABLED
        )       
    
    def eliminar_datos(self):
        self.db.eliminar_componente(self.item)
        
        self.boton_agregar.config(
            text='ELIMINADO',
            background=BOTON_ELIMINADO,
            disabledforeground=BOTON_DISABLED_TEXTO,
            state=tk.DISABLED
        )
    
    def ver_todo(self):
        from forms.form_display import FormDisplay
        self.limpiar_panel(self.panel_principal)
        FormDisplay(self.panel_principal)
    
    def fields_reset(self):
        # Reiniciar los valores de los entry a None
        self.TEXT_FIELDS = DATA_FIELDS.copy()
        for key in self.TEXT_FIELDS:
            self.TEXT_FIELDS[key] = DATA_FIELDS[key].copy()
        
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
    