from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # <-- Agregar esto
from pydantic import BaseModel
from typing import Optional
import uvicorn
import json
import traceback
import psutil  # <-- Mover aquí
import os
from datetime import datetime  # <-- Agregar esto

from database import DatabaseManager
from ollama_handler import OllamaHandlerOptimized
from models.agente import AgenteMantenimientoOptimizado

# Inicializar componentes
db = DatabaseManager()
ollama = OllamaHandlerOptimized(model="phi")  # Usar phi por ser más ligero
agente = AgenteMantenimientoOptimizado(db, ollama)

app = FastAPI(title="Agente de Mantenimiento Optimizado", version="1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class ReporteFalla(BaseModel):
    equipo: str
    sintoma: str
    descripcion: str
    modelo: Optional[str] = None
    historial: Optional[str] = None

class Feedback(BaseModel):
    caso_id: int
    exito: bool
    notas: Optional[str] = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "servicio": "Agente de Mantenimiento",
        "modelo": ollama.model,
        "optimizado": "8GB RAM"
    }

@app.post("/diagnosticar")
async def diagnosticar(reporte: ReporteFalla):
    """Endpoint principal para diagnóstico"""
    try:
        diagnostico = agente.procesar_reporte(reporte.model_dump())
        
        return {
            "success": True,
            "data": diagnostico,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/equipos")
async def listar_equipos():
    """Listar equipos en la base de conocimiento"""
    try:
        # Intentar obtener equipos desde la base de datos
        equipos_data = db.listar_equipos()
        
        if isinstance(equipos_data, list) and len(equipos_data) > 0:
            return {
                "success": True,
                "equipos": [{"tipo": e[0], "marca": e[1], "modelo": e[2]} for e in equipos_data]
            }
        else:
            # Si no hay datos, devolver lista vacía
            return {
                "success": True,
                "equipos": [],
                "message": "Base de datos vacía. Usa la función de inicialización."
            }
        
    except Exception as e:
        print(f"ERROR en /equipos: {traceback.format_exc()}")
        # Devolver lista vacía en caso de error
        return {
            "success": True,
            "equipos": [],
            "error": str(e),
            "message": "Error al cargar equipos. Base de datos puede estar vacía."
        }

@app.post("/feedback")
async def registrar_feedback(feedback: Feedback):
    """Registrar feedback sobre diagnóstico"""
    try:
        agente.aprender_de_solucion(feedback.caso_id, feedback.exito, feedback.notas)
        return {"success": True, "message": "Feedback registrado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estado")
async def estado_sistema():
    """Estado del sistema y uso de recursos"""
    memoria = psutil.virtual_memory()
    proceso = psutil.Process(os.getpid())
    
    return {
        "memoria_total_GB": round(memoria.total / (1024**3), 2),
        "memoria_usada_GB": round(memoria.used / (1024**3), 2),
        "memoria_libre_GB": round(memoria.free / (1024**3), 2),
        "memoria_proceso_MB": round(proceso.memory_info().rss / (1024**2), 2),
        "cpu_porcentaje": psutil.cpu_percent(),
        "modelo_activo": ollama.model
    }

# MANEJADOR DE EXCEPCIONES GLOBAL - FUERA DE LAS FUNCIONES
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"Error: {exc}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"message": "Error interno del servidor", "detail": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        workers=1  # Solo 1 worker para ahorrar RAM
    )