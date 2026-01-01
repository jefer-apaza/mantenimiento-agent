# 🤖 Agente Inteligente de Mantenimiento de Equipos

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLMs-orange.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema inteligente para diagnóstico y mantenimiento de equipos tecnológicos, optimizado para funcionar localmente en hardware limitado (8GB RAM).

## ✨ Características Principales

- �� **Diagnóstico Inteligente**: Analiza fallas usando modelos de lenguaje local
- 📚 **Base de Conocimiento**: Aprende de cada diagnóstico y mejora con el tiempo
- 🌐 **Interfaz Web**: UI intuitiva construida con Streamlit
- 🔧 **API REST**: Endpoints para integración con otros sistemas
- 💾 **Local y Privado**: Todo corre localmente, sin dependencias de cloud
- 🚀 **Optimizado para 8GB RAM**: Usa modelos ligeros y técnicas de eficiencia
- 📊 **Dashboard**: Métricas y estadísticas en tiempo real

## 🏗️ Arquitectura del Sistema
mantenimiento_agent/
├── app.py # API FastAPI principal
├── streamlit_app.py # Interfaz web Streamlit
├── database.py # Gestor de base de datos SQLite
├── ollama_handler.py # Integración con Ollama
├── models/
│ ├── agente.py # Lógica principal del agente
│ └── diagnostico_model.py # Modelos de datos
├── knowledge_base/ # Base de conocimiento
│ ├── equipos.json # Catálogo de equipos
│ ├── fallas.json # Fallas comunes
│ └── procedimientos.json # Guías de solución
├── data/ # Base de datos y almacenamiento
├── logs/ # Registros del sistema
├── requirements.txt # Dependencias Python
├── setup.sh # Script de instalación
└── start.sh # Script de inicio

## 🚀 Instalación Rápida

### Prerrequisitos
- Parrot OS / Ubuntu 22.04+ (o cualquier Linux)
- 8GB RAM mínimo
- 20GB espacio libre
- Python 3.11+

### Pasos de Instalación
```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/mantenimiento-agent.git
cd mantenimiento-agent

# 2. Ejecutar script de instalación
chmod +x setup.sh
./setup.sh

# 3. Iniciar el sistema
source venv/bin/activate
./start.sh both

Acceso al Sistema

    🌐 Interfaz Web: http://localhost:8501

    🔌 API REST: http://localhost:8000

    📚 Documentación API: http://localhost:8000/docs
