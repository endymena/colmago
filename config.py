"""
Módulo de Configuración
Gestiona las variables de entorno y configuración de la aplicación
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validar que las credenciales estén configuradas
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ ADVERTENCIA: Las credenciales de Supabase no están configuradas.")
    print("Por favor, crea un archivo .env con SUPABASE_URL y SUPABASE_KEY")

# Configuración de la aplicación
APP_TITLE = "Sistema de Programa ColmaGo"
APP_VERSION = "1.0.0"

# Nombres de las tablas en Supabase
TABLA_CLIENTES = "clientes"
TABLA_PRODUCTOS = "productos"
TABLA_COMPRAS = "compras"
TABLA_VENTAS = "ventas"
TABLA_EMPLEADOS = "empleados"

# Configuración de UI
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2

# Colores del tema
COLOR_PRIMARY = "#2563eb"
COLOR_SECONDARY = "#64748b"
COLOR_SUCCESS = "#10b981"
COLOR_DANGER = "#ef4444"
COLOR_WARNING = "#f59e0b"
COLOR_BG = "#f8fafc"
COLOR_TEXT = "#1e293b"
