import requests
import json

def test_diagnostico():
    print("🧪 Probando API de diagnóstico...")
    
    data = {
        "equipo": "Laptop",
        "sintoma": "No enciende",
        "descripcion": "Presiono el botón de encendido pero no hay respuesta, no se encienden los LEDs ni el ventilador"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/diagnosticar",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ API funciona correctamente")
            print(f"Diagnóstico: {resultado['data']['diagnostico'][:100]}...")
        else:
            print(f"❌ Error en API: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ No se pudo conectar a la API: {e}")

def test_estado():
    print("\n📊 Probando estado del sistema...")
    try:
        response = requests.get("http://localhost:8000/estado", timeout=5)
        if response.status_code == 200:
            estado = response.json()
            print(f"✅ Sistema activo")
            print(f"   RAM usada: {estado['memoria_usada_GB']} GB")
            print(f"   Modelo: {estado['modelo_activo']}")
    except:
        print("❌ No se pudo obtener estado")

if __name__ == "__main__":
    test_diagnostico()
    test_estado()