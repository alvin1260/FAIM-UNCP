import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Facultad de Minas - UNCP",
    page_icon="⛏️",
    layout="centered"
)

# ---------------------------------------------------------
# GESTIÓN DE DATOS (CORREGIDO)
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def cargar_padron_alumnos():
    """
    Conecta con Google Sheets usando la cuenta de servicio.
    """
    # 1. PEGA AQUÍ TU LINK ENTRE LAS COMILLAS
    url_sheet = "https://docs.google.com/spreadsheets/d/15IDFloqIsKMEUk6_GqY-kf16HdSeycwwFzjh8_yy9rw/edit" 

    try:
        # Crea la conexión
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Leemos ESPECIFICANDO la hoja explícitamente
        df = conn.read(spreadsheet=url_sheet)
        
        # Limpieza de datos
        df = df.astype(str)
        
        # Verificar que la columna 'codigo' exista antes de procesar
        if 'codigo' not in df.columns:
            st.error("Error: Tu Excel no tiene una columna llamada 'codigo' (todo minúscula).")
            return pd.DataFrame() # Retorna vacío seguro
            
        df['codigo'] = df['codigo'].str.strip().str.upper()
        return df
        
    except Exception as e:
        # Muestra el error exacto en pantalla para poder ayudarte
        st.error(f"Error conectando a Google Sheets: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# INTERFAZ DE LOGIN
# ---------------------------------------------------------
def mostrar_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Asegúrate de tener una imagen 'logo_uncp.png' en tu carpeta o comenta esta línea
        # st.image("logo_uncp.png", width=150) 
        st.header("Ingeniería de Minas")
        st.subheader("Acceso Estudiantil")

    codigo_input = st.text_input("Ingresa tu Código de Matricula (Ej: 2022...)", max_chars=11)
    
    if st.button("Ingresar al Sistema", type="primary"):
        with st.spinner("Validando credenciales..."):
            df_alumnos = cargar_padron_alumnos()
            
            # Buscamos el código
            usuario = df_alumnos[df_alumnos['codigo'] == codigo_input.upper()]
            
            if not usuario.empty:
                # ¡ÉXITO!
                st.session_state['logueado'] = True
                st.session_state['usuario_nombre'] = usuario.iloc[0]['nombres']
                st.session_state['usuario_codigo'] = usuario.iloc[0]['codigo']
                st.rerun()
            else:
                st.error("❌ Código no encontrado en el padrón actual.")
                st.info("Si eres cachimbo, contacta a tu delegado.")

# ---------------------------------------------------------
# APP PRINCIPAL (DESPUÉS DEL LOGIN)
# ---------------------------------------------------------
def mostrar_app_principal():
    # Barra lateral (Sidebar)
    with st.sidebar:
        st.write(f"👷‍♂️ **Hola, {st.session_state['usuario_nombre']}**")
        st.caption(f"ID: {st.session_state['usuario_codigo']}")
        st.divider()
        
        menu = st.radio("Navegación", 
            ["Inicio", "Mapa Minero 🗺️", "Laboratorios 🔬", "Normativa ⚖️", "Facultad 🏫"]
        )
        
        st.divider()
        if st.button("Cerrar Sesión"):
            st.session_state['logueado'] = False
            st.rerun()

    # Contenido de las páginas
    if menu == "Inicio":
        st.title("Panel de Noticias")
        st.info("📅 **Aviso:** La semana de parciales inicia el 15 de Octubre.")
        st.write("Bienvenido a la plataforma digital de la facultad.")

    elif menu == "Mapa Minero 🗺️":
        st.title("Unidades Mineras del Perú")
        st.write("Aquí irá el mapa interactivo con filtros por mineral (Au, Cu, Zn).")
        # Placeholder para el mapa futuro
        st.map(latitude=[-12.0], longitude=[-75.0], zoom=5) 

    elif menu == "Laboratorios 🔬":
        st.title("Gestión de Laboratorios")
        lab = st.selectbox("Selecciona un ambiente:", 
            ["Mecánica de Rocas", "Mineralogía", "Ventilación", "Topografía"])
        
        if lab == "Mecánica de Rocas":
            st.subheader("Mecánica de Rocas")
            st.write("**Equipos disponibles:** Prensa de Compresión, Máquina de Los Ángeles.")
            st.warning("⚠️ EPP Obligatorio: Zapatos de seguridad y Lentes.")
        elif lab == "Mineralogía":
             st.subheader("Colección de Minerales")
             st.write("Consulta las fichas técnicas de la pirita, calcopirita, galena, etc.")

    elif menu == "Normativa ⚖️":
        st.title("Base Legal Minera")
        busqueda = st.text_input("Buscar en DS-024 o Ley General de Minería", placeholder="Ej. Arnés, Ventilación...")
        if busqueda:
            st.write(f"Resultados simulados para: '{busqueda}'...")

    elif menu == "Facultad 🏫":
        st.title("Mi Facultad")
        tab1, tab2 = st.tabs(["Croquis Seguro", "Círculos de Estudio"])
        
        with tab1:
            st.write("📍 **Zonas Seguras y Extintores**")
            st.write("Mapa de evacuación y ubicación de botiquines.")
        
        with tab2:
            st.write("👥 **Grupos Activos**")
            st.write("- Círculo de Geomecánica")
            st.write("- Círculo de Seguridad Minera")
            st.button("Crear nuevo grupo de estudio +")

# ---------------------------------------------------------
# CONTROL DE FLUJO
# ---------------------------------------------------------
if 'logueado' not in st.session_state:
    st.session_state['logueado'] = False

if st.session_state['logueado']:
    mostrar_app_principal()
else:
    mostrar_login()