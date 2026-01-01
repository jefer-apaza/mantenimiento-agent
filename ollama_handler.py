import ollama
import json
import time
from typing import Dict, Any, List

class OllamaHandlerOptimized:
    def __init__(self, model="phi"):
        self.model = model
        self.max_tokens = 512  # Reducido para ahorrar RAM
        self.temperature = 0.3  # Más determinista
        
    def generar_diagnostico(self, contexto: str) -> Dict[str, Any]:
        """Generar diagnóstico optimizado para baja RAM"""
        
        prompt = f"""Eres un técnico especialista en mantenimiento de equipos.
        
Contexto:
{contexto}

Responde ÚNICAMENTE en formato JSON con esta estructura exacta:
{{
    "diagnostico": "diagnóstico principal",
    "causas_posibles": ["causa1", "causa2", "causa3"],
    "pasos_solucion": ["paso1", "paso2", "paso3"],
    "herramientas_necesarias": ["herramienta1", "herramienta2"],
    "tiempo_estimado_minutos": 30,
    "nivel_dificultad": "Bajo/Medio/Alto",
    "precauciones": ["precaucion1", "precaucion2"]
}}

Mantén las respuestas concisas y prácticas.
"""
        
        try:
            # Configuración optimizada para baja RAM
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': self.max_tokens,
                    'temperature': self.temperature,
                    'top_k': 20,
                    'top_p': 0.8,
                    'repeat_penalty': 1.1,
                    'num_thread': 2  # Usar solo 2 threads
                }
            )
            
            # Parsear respuesta JSON
            respuesta_texto = response['response']
            
            # Intentar extraer JSON
            try:
                # Buscar contenido entre {}
                inicio = respuesta_texto.find('{')
                fin = respuesta_texto.rfind('}') + 1
                
                if inicio != -1 and fin != -1:
                    json_str = respuesta_texto[inicio:fin]
                    return json.loads(json_str)
                else:
                    raise ValueError("No se encontró JSON en la respuesta")
                    
            except json.JSONDecodeError:
                # Fallback: respuesta estructurada simple
                return {
                    "diagnostico": respuesta_texto[:100],
                    "causas_posibles": ["Por determinar"],
                    "pasos_solucion": ["1. Contactar técnico especializado"],
                    "herramientas_necesarias": ["Herramientas básicas"],
                    "tiempo_estimado_minutos": 60,
                    "nivel_dificultad": "Medio",
                    "precauciones": ["Desconectar equipo antes de manipular"]
                }
                
        except Exception as e:
            print(f"Error en Ollama: {e}")
            return {
                "diagnostico": "Error en el diagnóstico",
                "causas_posibles": ["Error del sistema"],
                "pasos_solucion": ["Reintentar o contactar soporte"],
                "herramientas_necesarias": [],
                "tiempo_estimado_minutos": 0,
                "nivel_dificultad": "Bajo",
                "precauciones": []
            }
    
    def diagnosticar_falla(self, equipo: str, sintoma: str, 
                          descripcion: str, casos_similares: List[Dict]) -> Dict[str, Any]:
        """Diagnóstico principal"""
        
        # Construir contexto
        contexto_casos = ""
        if casos_similares:
            contexto_casos = "\nCasos similares resueltos:\n"
            for caso in casos_similares[:3]:  # Limitar a 3 casos
                contexto_casos += f"- {caso['sintoma']}: {caso['soluciones'][0] if caso['soluciones'] else 'Sin solución registrada'}\n"
        
        contexto = f"""
INFORMACIÓN DE LA FALLA:
- Equipo: {equipo}
- Síntoma principal: {sintoma}
- Descripción detallada: {descripcion}
{contexto_casos}

Proporciona un diagnóstico técnico práctico.
"""
        
        return self.generar_diagnostico(contexto)