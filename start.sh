#!/bin/bash
# start.sh - Script de inicio optimizado

cd ~/mantenimiento_agent

# Activar entorno virtual
source venv/bin/activate

# Limpiar cache de Python
python -c "import sys; sys.path.clear()"

# Configurar límites de RAM para Python
export PYTHONUNBUFFERED=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1

echo "🚀 Iniciando Agente de Mantenimiento..."
echo "💾 RAM disponible: $(free -h | awk '/^Mem:/ {print $4}')"

# Opciones:
case "$1" in
    api)
        echo "🌐 Iniciando API en puerto 8000..."
        uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
        ;;
    web)
        echo "🖥️  Iniciando interfaz web en puerto 8501..."
        streamlit run streamlit_app.py --server.port 8501 --server.headless true
        ;;
    both)
        echo "⚡ Iniciando ambos servicios..."
        # Iniciar API en background
        uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1 &
        API_PID=$!
        
        # Esperar 3 segundos
        sleep 3
        
        # Iniciar interfaz web
        streamlit run streamlit_app.py --server.port 8501 --server.headless true
        
        # Al cerrar, terminar API también
        kill $API_PID
        ;;
    *)
        echo "Uso: ./start.sh {api|web|both}"
        echo "  api  - Solo servidor API"
        echo "  web  - Solo interfaz web"
        echo "  both - Ambos servicios"
        exit 1
        ;;
esac