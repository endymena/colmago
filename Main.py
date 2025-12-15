"""
Sistema de Programa ColmaGo
Aplicación principal con menú de navegación
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import config
from modules.clientes import ClientesWindow
from modules.productos import ProductosWindow
from modules.compras import ComprasWindow
from modules.ventas import VentasWindow
from modules.empleados import EmpleadosWindow

from utils.logger import app_logger

class MainApplication:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        """Inicializa la aplicación principal"""
        app_logger.info("Iniciando Sistema ColmaGo")
        
        self.root = tk.Tk()
        self.root.title(config.APP_TITLE)
        
        # Detectar tamaño de pantalla y ajustar ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Ajustar tamaño según pantalla disponible
        if screen_width < 1024:  # Pantallas pequeñas
            window_width = int(screen_width * 0.9)
            window_height = int(screen_height * 0.9)
        else:  # Pantallas normales
            window_width = 900
            window_height = 700
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg=config.COLOR_BG)
        
        # Configurar tamaño mínimo más pequeño para tablets
        self.root.minsize(600, 500)
        
        # Centrar ventana
        self._centrar_ventana()
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        app_logger.info("Aplicación iniciada correctamente")
    
    def _centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _crear_interfaz(self):
        """Crea la interfaz del menú principal"""
        # Frame principal centrado
        main_frame = tk.Frame(self.root, bg=config.COLOR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame para centrar contenido
        center_frame = tk.Frame(main_frame, bg=config.COLOR_BG)
        center_frame.pack(expand=True)
        
        # Logo centrado
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "Logo de proyecto colmado-01.png")
            logo_image = Image.open(logo_path)
            # Redimensionar el logo a tamaño cuadrado más pequeño para asegurar visibilidad
            logo_image = logo_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                center_frame,
                image=self.logo_photo,
                bg=config.COLOR_BG
            )
            logo_label.pack(pady=(0, 20))
        except Exception as e:
            # Si no se puede cargar el logo, mostrar título de texto como fallback
            print(f"No se pudo cargar el logo: {e}")
            titulo = tk.Label(
                center_frame,
                text="🏢 Sistema de Programa ColmaGo",
                font=("Arial", 28, "bold"),
                bg=config.COLOR_BG,
                fg=config.COLOR_TEXT
            )
            titulo.pack(pady=(0, 20))
        
        # Subtítulo centrado
        subtitulo = tk.Label(
            center_frame,
            text=f"Versión {config.APP_VERSION}",
            font=("Arial", 12),
            bg=config.COLOR_BG,
            fg=config.COLOR_SECONDARY
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame de botones centrado
        buttons_frame = tk.Frame(center_frame, bg=config.COLOR_BG)
        buttons_frame.pack(pady=10)
        
        # Botones del menú
        botones = [
            ("👥 Clientes", self._abrir_clientes, config.COLOR_PRIMARY),
            ("📦 Productos", self._abrir_productos, config.COLOR_SUCCESS),
            ("🛒 Compras", self._abrir_compras, config.COLOR_WARNING),
            ("💰 Ventas", self._abrir_ventas, config.COLOR_DANGER),
            ("👔 Empleados", self._abrir_empleados, config.COLOR_SECONDARY),

        ]
        
        # Crear botones con tamaño uniforme usando pack
        for texto, comando, color in botones:
            btn = tk.Button(
                buttons_frame,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Arial", 13, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                height=2,
                anchor="center"
            )
            btn.pack(fill=tk.X, pady=3, padx=20, ipadx=50)
            
            # Efecto hover
            color_oscuro = self._oscurecer_color(color)
            btn.bind("<Enter>", lambda e, c=color_oscuro, b=btn: b.config(bg=c))
            btn.bind("<Leave>", lambda e, c=color, b=btn: b.config(bg=c))
        
        # Separador
        separador = tk.Frame(buttons_frame, height=2, bg=config.COLOR_SECONDARY)
        separador.pack(fill=tk.X, pady=12, padx=20)
        
        # Botón de salir
        btn_salir = tk.Button(
            buttons_frame,
            text="❌ Salir",
            command=self._on_closing,
            bg="#94a3b8",
            fg="white",
            font=("Arial", 13, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            anchor="center"
        )
        btn_salir.pack(fill=tk.X, pady=4, padx=20, ipadx=50)
        
        # Efecto hover para botón salir
        btn_salir.bind("<Enter>", lambda e: btn_salir.config(bg="#64748b"))
        btn_salir.bind("<Leave>", lambda e: btn_salir.config(bg="#94a3b8"))
        
        # Pie de página
        footer = tk.Label(
            self.root,
            text="Desarrollado con Python y Tkinter | Conectado a Supabase",
            font=("Arial", 9),
            bg=config.COLOR_SECONDARY,
            fg="white",
            pady=10
        )
        footer.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _crear_boton_menu(self, parent, texto, comando, color):
        """
        Crea un botón del menú principal
        
        Args:
            parent: Widget padre
            texto: Texto del botón
            comando: Función a ejecutar
            color: Color del botón
        """
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=color,
            fg="white",
            font=("Arial", 13, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            width=35,
            height=2
        )
        btn.pack(pady=8)
        
        # Efecto hover
        color_oscuro = self._oscurecer_color(color)
        btn.bind("<Enter>", lambda e: btn.config(bg=color_oscuro))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
    
    def _oscurecer_color(self, color):
        """
        Oscurece un color hexadecimal
        
        Args:
            color: Color en formato hexadecimal
        
        Returns:
            Color oscurecido
        """
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, r-30), max(0, g-30), max(0, b-30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _abrir_clientes(self):
        """Abre el módulo de clientes"""
        app_logger.info("Abriendo módulo de Clientes")
        ClientesWindow(self.root)
    
    def _abrir_productos(self):
        """Abre el módulo de productos"""
        app_logger.info("Abriendo módulo de Productos")
        ProductosWindow(self.root)
    
    def _abrir_compras(self):
        """Abre el módulo de compras"""
        app_logger.info("Abriendo módulo de Compras")
        ComprasWindow(self.root)
    
    def _abrir_ventas(self):
        """Abre el módulo de ventas"""
        app_logger.info("Abriendo módulo de Ventas")
        VentasWindow(self.root)
    
    def _abrir_empleados(self):
        """Abre el módulo de empleados"""
        app_logger.info("Abriendo módulo de Empleados")
        EmpleadosWindow(self.root)
    

    
    def _on_closing(self):
        """Maneja el cierre de la aplicación"""
        respuesta = messagebox.askyesno(
            "Confirmar salida",
            "¿Está seguro de que desea salir?"
        )
        if respuesta:
            app_logger.info("Cerrando aplicación ColmaGo")
            self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("=" * 50)
    print("🏢 Sistema de Programa ColmaGo")
    print(f"Versión {config.APP_VERSION}")
    print("=" * 50)
    print()
    
    # Crear y ejecutar aplicación
    app = MainApplication()
    app.run()

if __name__ == "__main__":
    main()
