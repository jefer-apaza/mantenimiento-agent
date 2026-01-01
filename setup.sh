#!/bin/bash
# setup.sh - Instalación optimizada para 8GB RAM

echo "🔧 Instalando Agente de Mantenimiento Optimizado..."

# Verificar Parrot OS
if ! grep -q "Parrot" /etc/os-release; then
    echo "⚠️  Advertencia: Este script está optimizado para Parrot OS"
fi

# Crear directorio
mkdir -p ~/mantenimiento_agent
cd ~/mantenimiento_agent

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.0
pip install sqlalchemy==2.0.23 aiofiles==23.2.0
pip install ollama==0.1.2 streamlit==1.28.0 requests==2.31.0

# Descargar modelo ligero
echo "🤖 Descargando modelo Phi (ligero)..."
ollama pull phi

# Crear estructura de directorios
echo "📁 Creando estructura..."
mkdir -p knowledge_base models data logs

# Dar permisos
chmod +x *.sh

echo "✅ Instalación completada!"
echo ""
echo "📋 PARA INICIAR:"
echo "1. Activar entorno: source venv/bin/activate"
echo "2. Iniciar API: python app.py"
echo "3. En otra terminal: streamlit run streamlit_app.py"
echo ""
echo "🌐 Acceder en: http://localhost:8501"