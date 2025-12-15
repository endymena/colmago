"""
Módulo de Base de Datos
Gestiona la conexión y operaciones CRUD con Supabase
Incluye fallback a CSV local si Supabase no está disponible
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from supabase import create_client, Client
import config

class Database:
    """Clase para gestionar la conexión y operaciones con Supabase"""
    
    def __init__(self):
        """Inicializa la conexión a Supabase"""
        self.supabase: Optional[Client] = None
        self.connected = False
        self.csv_mode = False
        self.csv_dir = "data_backup"
        
        # Crear directorio para backups CSV si no existe
        if not os.path.exists(self.csv_dir):
            os.makedirs(self.csv_dir)
        
        self._connect()
    
    def _connect(self):
        """Establece conexión con Supabase"""
        try:
            if config.SUPABASE_URL and config.SUPABASE_KEY:
                self.supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
                # Probar la conexión
                self.supabase.table(config.TABLA_CLIENTES).select("*").limit(1).execute()
                self.connected = True
                self.csv_mode = False
                print("✅ Conectado a Supabase exitosamente")
            else:
                raise Exception("Credenciales de Supabase no configuradas")
        except Exception as e:
            print(f"⚠️ No se pudo conectar a Supabase: {e}")
            print("📁 Usando modo CSV local como respaldo")
            self.connected = False
            self.csv_mode = True
    
    def _get_csv_path(self, tabla: str) -> str:
        """Obtiene la ruta del archivo CSV para una tabla"""
        return os.path.join(self.csv_dir, f"{tabla}.csv")
    
    def _read_csv(self, tabla: str) -> List[Dict]:
        """Lee datos desde un archivo CSV"""
        csv_path = self._get_csv_path(tabla)
        if not os.path.exists(csv_path):
            return []
        
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def _write_csv(self, tabla: str, datos: List[Dict]):
        """Escribe datos a un archivo CSV"""
        if not datos:
            return
        
        csv_path = self._get_csv_path(tabla)
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=datos[0].keys())
            writer.writeheader()
            writer.writerows(datos)
    
    def select(self, tabla: str, filtros: Optional[Dict] = None) -> List[Dict]:
        """
        Selecciona registros de una tabla
        
        Args:
            tabla: Nombre de la tabla
            filtros: Diccionario con filtros opcionales
        
        Returns:
            Lista de registros
        """
        try:
            if self.csv_mode:
                datos = self._read_csv(tabla)
                if filtros:
                    # Aplicar filtros manualmente
                    datos = [d for d in datos if all(d.get(k) == v for k, v in filtros.items())]
                return datos
            else:
                query = self.supabase.table(tabla).select("*")
                if filtros:
                    for key, value in filtros.items():
                        query = query.eq(key, value)
                response = query.execute()
                return response.data
        except Exception as e:
            print(f"❌ Error al seleccionar de {tabla}: {e}")
            return []
    
    def insert(self, tabla: str, datos: Dict) -> bool:
        """
        Inserta un nuevo registro en una tabla
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con los datos a insertar
        
        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            if self.csv_mode:
                registros = self._read_csv(tabla)
                # Generar ID si no existe
                if 'id' not in datos:
                    max_id = max([int(r.get('id', 0)) for r in registros], default=0)
                    datos['id'] = str(max_id + 1)
                registros.append(datos)
                self._write_csv(tabla, registros)
                return True
            else:
                self.supabase.table(tabla).insert(datos).execute()
                return True
        except Exception as e:
            print(f"❌ Error al insertar en {tabla}: {e}")
            return False
    
    def update(self, tabla: str, id_registro: int, datos: Dict) -> bool:
        """
        Actualiza un registro existente
        
        Args:
            tabla: Nombre de la tabla
            id_registro: ID del registro a actualizar
            datos: Diccionario con los datos a actualizar
        
        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            if self.csv_mode:
                registros = self._read_csv(tabla)
                for i, r in enumerate(registros):
                    if r.get('id') == str(id_registro):
                        registros[i].update(datos)
                        break
                self._write_csv(tabla, registros)
                return True
            else:
                self.supabase.table(tabla).update(datos).eq('id', id_registro).execute()
                return True
        except Exception as e:
            print(f"❌ Error al actualizar en {tabla}: {e}")
            return False
    
    def delete(self, tabla: str, id_registro: int) -> bool:
        """
        Elimina un registro
        
        Args:
            tabla: Nombre de la tabla
            id_registro: ID del registro a eliminar
        
        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            if self.csv_mode:
                registros = self._read_csv(tabla)
                registros = [r for r in registros if r.get('id') != str(id_registro)]
                self._write_csv(tabla, registros)
                return True
            else:
                self.supabase.table(tabla).delete().eq('id', id_registro).execute()
                return True
        except Exception as e:
            print(f"❌ Error al eliminar de {tabla}: {e}")
            return False
    
    def get_connection_status(self) -> str:
        """Retorna el estado de la conexión"""
        if self.csv_mode:
            return "CSV Local"
        elif self.connected:
            return "Supabase"
        else:
            return "Desconectado"

# Instancia global de la base de datos
db = Database()
