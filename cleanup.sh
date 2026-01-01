#!/bin/bash
# cleanup.sh - Limpiar recursos

echo "🧹 Limpiando recursos..."

# Detener servicios
pkill -f "uvicorn app:app"
pkill -f "streamlit"

# Limpiar cache de Ollama
ollama ps | grep -v "NAME" | awk '{print $1}' | xargs -I {} ollama stop {}

# Limpiar cache de Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Liberar memoria
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

echo "✅ Limpieza completada"
echo "💾 Memoria libre: $(free -h | awk '/^Mem:/ {print $4}')"