import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_path="data/knowledge_base.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializar base de datos optimizada"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla optimizada para equipos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            marca TEXT,
            modelo TEXT,
            caracteristicas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabla optimizada para fallas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fallas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_tipo TEXT NOT NULL,
            sintoma TEXT NOT NULL,
            descripcion TEXT,
            causas TEXT,  -- JSON array
            soluciones TEXT,  -- JSON array
            frecuencia INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabla optimizada para historial
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_tipo TEXT NOT NULL,
            sintoma TEXT NOT NULL,
            diagnostico TEXT,
            solucion TEXT,
            exito BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Índices para mejor rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fallas_equipo ON fallas(equipo_tipo)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fallas_sintoma ON fallas(sintoma)')
        
        conn.commit()
        conn.close()
        
        # Cargar datos iniciales si no existen
        self._load_initial_data()
    
    

    def _load_initial_data(self):
        """Cargar datos iniciales de mantenimiento común"""
        initial_data = [
            # Equipos de computación
            ("Laptop", "Lenovo", "ThinkPad T480", 
             "Intel i5, 8GB RAM, SSD 256GB, Windows 10"),
            ("Desktop", "HP", "ProDesk 400 G6",
             "Intel i3, 4GB RAM, HDD 1TB, Windows 10"),
            ("Impresora", "HP", "LaserJet Pro MFP M428fdw",
             "Láser, multifunción, WiFi, Ethernet"),
            ("Monitor", "Dell", "UltraSharp U2419H",
             "24\", IPS, 1920x1080, HDMI/DisplayPort"),
            ("Router", "TP-Link", "Archer C7",
             "Dual-band, 1750 Mbps, 4 puertos LAN"),
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM equipos")
        if cursor.fetchone()[0] == 0:
            for equipo in initial_data:
                cursor.execute(
                    "INSERT INTO equipos (tipo, marca, modelo, caracteristicas) VALUES (?, ?, ?, ?)",
                    equipo
                )
        
        # Fallas comunes iniciales
        common_issues = [
            ("Laptop", "No enciende", "El equipo no muestra señal de vida",
             '["Batería agotada", "Adaptador dañado", "Problema de motherboard"]',
             '["Probar con otro cargador", "Retirar batería y conectar solo con cable", "Verificar led de carga"]'),
            
            ("Impresora", "Atascamiento de papel", "El papel se traba al imprimir",
             '["Papel mal colocado", "Rodillos sucios", "Tipo de papel incorrecto"]',
             '["Apagar y retirar papel cuidadosamente", "Limpiar rodillos con paño seco", "Usar papel recomendado"]'),
            
            ("Monitor", "Sin señal", "Muestra 'No signal' o pantalla negra",
             '["Cable suelto", "Puerto dañado", "Configuración incorrecta"]',
             '["Verificar conexiones", "Probar otro cable", "Cambiar fuente de entrada"]'),
        ]
        
        cursor.execute("SELECT COUNT(*) FROM fallas")
        if cursor.fetchone()[0] == 0:
            for issue in common_issues:
                cursor.execute(
                    """INSERT INTO fallas (equipo_tipo, sintoma, descripcion, causas, soluciones) 
                       VALUES (?, ?, ?, ?, ?)""",
                    issue
                )
        
        conn.commit()
        conn.close()
    


    def buscar_fallas_similares(self, equipo_tipo: str, sintoma: str) -> List[Dict]:
        """Buscar fallas similares en la base de conocimiento"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Búsqueda por palabras clave
        keywords = sintoma.split()[:5]  # Tomar primeras 5 palabras
        query = """
        SELECT * FROM fallas 
        WHERE equipo_tipo LIKE ? 
        AND ("""
        
        params = [f"%{equipo_tipo}%"]
        for i, keyword in enumerate(keywords):
            if i > 0:
                query += " OR "
            query += f"sintoma LIKE ? OR descripcion LIKE ?"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        
        query += ") ORDER BY frecuencia DESC LIMIT 5"
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        # Parsear JSON en causas y soluciones
        for result in results:
            result['causas'] = json.loads(result['causas'])
            result['soluciones'] = json.loads(result['soluciones'])
        
        conn.close()
        return results
    
    def registrar_diagnostico(self, equipo_tipo: str, sintoma: str, 
                             diagnostico: str, solucion: str, exito: bool = None):
        """Registrar diagnóstico en historial"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO historial (equipo_tipo, sintoma, diagnostico, solucion, exito)
               VALUES (?, ?, ?, ?, ?)""",
            (equipo_tipo, sintoma, diagnostico, solucion, exito)
        )
        
        conn.commit()
        conn.close()

    def listar_equipos(self):
        """Lista todos los equipos únicos en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si la tabla existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='equipos'")
            if not cursor.fetchone():
                print("Tabla 'equipos' no existe. Creando...")
                self._init_db()  # Re-inicializar si no existe
            
            cursor.execute("SELECT DISTINCT tipo, marca, modelo FROM equipos ORDER BY tipo")
            equipos = cursor.fetchall()
            conn.close()
            
            return equipos
        except Exception as e:
            print(f"Error en listar_equipos: {e}")
            return []