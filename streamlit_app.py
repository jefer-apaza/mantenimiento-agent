import streamlit as st
import requests
import json
from datetime import datetime

# Configurar página
st.set_page_config(
    page_title="Agente de Mantenimiento",
    page_icon="🔧",
    layout="wide"
)

# CSS para mejor rendimiento
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .diagnostico-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🔧 Agente de Mantenimiento Inteligente")
st.caption("Versión optimizada para 8GB RAM")

# Sidebar
with st.sidebar:
    st.header("Configuración")
    modelo = st.selectbox(
        "Modelo AI",
        ["phi", "tinyllama", "gemma:2b"],
        index=0
    )
    
    api_url = st.text_input(
        "URL API",
        value="http://localhost:8000",
        help="URL donde corre el servidor FastAPI"
    )
    
    if st.button("🔄 Verificar Conexión"):
        try:
            response = requests.get(f"{api_url}/")
            if response.status_code == 200:
                st.success("✅ API conectada")
                st.json(response.json())
            else:
                st.error("❌ Error en conexión")
        except:
            st.error("❌ No se pudo conectar")

# Contenido principal - DEFINIR PESTAÑAS AQUÍ, ANTES DE USARLAS
tab1, tab2, tab3 = st.tabs(["Diagnóstico", "Base de Conocimiento", "Sistema"])

with tab1:
    st.header("Reportar Falla")
    
    # Inicializar variables en session_state
    if 'diagnostico_realizado' not in st.session_state:
        st.session_state.diagnostico_realizado = False
    if 'diagnostico_data' not in st.session_state:
        st.session_state.diagnostico_data = None
    
    # FORMULARIO separado del resultado
    with st.form("reporte_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            equipo = st.selectbox(
                "Tipo de Equipo",
                ["Laptop", "Desktop", "Impresora", "Monitor", "Router", 
                 "Switch", "Servidor", "Otro"]
            )
            
            if equipo == "Otro":
                equipo = st.text_input("Especificar equipo")
            
            modelo_equipo = st.text_input("Modelo específico (opcional)")
        
        with col2:
            sintoma = st.text_input("Síntoma principal", 
                                   placeholder="Ej: No enciende, sin señal, error de impresión")
            
            urgencia = st.select_slider(
                "Nivel de urgencia",
                options=["Baja", "Media", "Alta", "Crítica"]
            )
        
        descripcion = st.text_area(
            "Descripción detallada",
            height=100,
            placeholder="Describe la falla con detalle: cuándo empezó, qué has probado, etc."
        )
        
        submit_button = st.form_submit_button("🔍 Diagnosticar", type="primary")
        
        if submit_button:
            if not equipo or not sintoma:
                st.error("Por favor, completa al menos el equipo y el síntoma")
            else:
                # Guardar datos temporalmente
                st.session_state.form_data = {
                    "equipo": equipo,
                    "sintoma": sintoma,
                    "descripcion": descripcion,
                    "modelo": modelo_equipo,
                    "urgencia": urgencia
                }
                st.session_state.diagnostico_realizado = True
    
    # MOSTRAR RESULTADOS FUERA DEL FORMULARIO
    if st.session_state.diagnostico_realizado and 'form_data' in st.session_state:
        with st.spinner("Analizando falla..."):
            try:
                data = st.session_state.form_data
                
                # Enviar a API (sin el campo urgencia que no está en el modelo)
                api_data = {k: v for k, v in data.items() if k != 'urgencia'}
                
                response = requests.post(
                    f"{api_url}/diagnosticar",
                    json=api_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    diagnostico = resultado.get("data", {})
                    st.session_state.diagnostico_data = diagnostico
                    
                    st.success("✅ Diagnóstico completado")
                    
                    # Mostrar resultados
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.subheader("📋 Diagnóstico")
                        st.info(diagnostico.get("diagnostico", "No disponible"))
                        
                        st.subheader("🔍 Causas Posibles")
                        causas = diagnostico.get("causas_posibles", [])
                        for causa in causas:
                            st.write(f"• {causa}")
                    
                    with col_b:
                        st.subheader("🛠️ Solución")
                        pasos = diagnostico.get("pasos_solucion", [])
                        for i, paso in enumerate(pasos, 1):
                            st.write(f"{i}. {paso}")
                        
                        st.subheader("⚠️ Precauciones")
                        precauciones = diagnostico.get("precauciones", [])
                        for prec in precauciones:
                            st.warning(f"• {prec}")
                    
                    # Información adicional
                    with st.expander("📊 Detalles técnicos"):
                        col_c, col_d, col_e = st.columns(3)
                        
                        with col_c:
                            st.metric(
                                "Tiempo estimado",
                                f"{diagnostico.get('tiempo_estimado_minutos', 0)} min"
                            )
                        
                        with col_d:
                            dificultad = diagnostico.get("nivel_dificultad", "Media")
                            st.metric("Dificultad", dificultad)
                        
                        with col_e:
                            herramientas = diagnostico.get("herramientas_necesarias", [])
                            st.metric("Herramientas", len(herramientas))
                        
                        if herramientas:
                            st.write("**Herramientas necesarias:**")
                            for herramienta in herramientas:
                                st.write(f"🔨 {herramienta}")
                    
                else:
                    st.error(f"Error en el diagnóstico: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("⏳ Tiempo de espera agotado. El modelo puede estar ocupado.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # FEEDBACK - FUERA DE CUALQUIER FORMULARIO
    if st.session_state.diagnostico_realizado and st.session_state.diagnostico_data:
        st.divider()
        st.subheader("¿Fue útil este diagnóstico?")
        
        col_si, col_no = st.columns(2)
        with col_si:
            if st.button("✅ Sí, resolvió el problema", key="feedback_si"):
                st.success("¡Gracias por tu feedback!")
                # Aquí podrías enviar feedback a la API
                st.session_state.diagnostico_realizado = False
        with col_no:
            if st.button("❌ No, no fue útil", key="feedback_no"):
                st.info("Lamentamos que no fuera útil. Contacta a un técnico.")
                st.session_state.diagnostico_realizado = False

with tab2:
    st.header("Base de Conocimiento")
    
    try:
        response = requests.get(f"{api_url}/equipos")
        if response.status_code == 200:
            data = response.json()
            equipos = data.get("equipos", [])
            
            st.write(f"Equipos registrados: {len(equipos)}")
            
            for equipo in equipos:
                with st.expander(f"{equipo['tipo']} - {equipo['marca']} {equipo.get('modelo', '')}"):
                    st.write(f"**Marca:** {equipo['marca']}")
                    st.write(f"**Modelo:** {equipo.get('modelo', 'No especificado')}")
        else:
            st.error("Error al cargar equipos")
    except:
        st.warning("Conecta a la API para ver la base de conocimiento")

with tab3:
    st.header("Estado del Sistema")
    
    if st.button("📊 Obtener métricas"):
        try:
            response = requests.get(f"{api_url}/estado")
            if response.status_code == 200:
                estado = response.json()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Memoria Total", f"{estado['memoria_total_GB']} GB")
                    st.metric("Memoria Libre", f"{estado['memoria_libre_GB']} GB")
                
                with col2:
                    st.metric("Memoria Usada", f"{estado['memoria_usada_GB']} GB")
                    st.metric("Memoria Proceso", f"{estado['memoria_proceso_MB']} MB")
                
                with col3:
                    st.metric("CPU", f"{estado['cpu_porcentaje']}%")
                    st.metric("Modelo", estado['modelo_activo'])
                
                # Gráfico simple de memoria
                import pandas as pd
                mem_data = pd.DataFrame({
                    'Tipo': ['Usada', 'Libre'],
                    'GB': [estado['memoria_usada_GB'], estado['memoria_libre_GB']]
                })
                
                st.bar_chart(mem_data.set_index('Tipo'))
                
            else:
                st.error("Error al obtener estado")
        except:
            st.error("No se pudo conectar al servidor")
    
    st.divider()
    st.subheader("Instrucciones Rápidas")
    
    st.write("""
    1. **Iniciar servidor API:** `python app.py`
    2. **Iniciar interfaz web:** `streamlit run streamlit_app.py`
    3. **Acceder en navegador:** `http://localhost:8501`
    4. **Verificar API:** `http://localhost:8000`
    
    **Para ahorrar RAM:**
    - Cerrar otras aplicaciones
    - Usar modelo 'phi' o 'tinyllama'
    - Reiniciar si el sistema se vuelve lento
    """)

# Footer
st.divider()
st.caption(f"Sistema de diagnóstico técnico | {datetime.now().year} | Optimizado para 8GB RAM")