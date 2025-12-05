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
# GESTIÓN DE DATOS (VERSIÓN TOLERANTE A ERRORES)
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def cargar_padron_alumnos():
    # PEGA TU LINK AQUÍ
    url_sheet = "https://docs.google.com/spreadsheets/d/15IDFloqIsKMEUk6_GqY-kf16HdSeycwwFzjh8_yy9rw/edit?pli=1&gid=0#gid=0" 

    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=url_sheet)
        df = df.astype(str)
        
        # --- LIMPIEZA AUTOMÁTICA DE CABECERAS ---
        # Esto convierte "CÓDIGO " -> "codigo"
        df.columns = df.columns.str.lower().str.strip()
        
        # Validación
        if 'codigo' not in df.columns:
            st.error("⚠️ Error de Formato en Excel")
            st.write("El sistema buscaba la columna: `codigo`")
            st.write("Pero encontró estas columnas en tu Excel:", df.columns.tolist())
            # Retornamos un DataFrame vacío pero con la estructura correcta para que no explote
            return pd.DataFrame(columns=['codigo', 'nombres'])
            
        df['codigo'] = df['codigo'].str.strip().str.upper()
        return df
        
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame(columns=['codigo', 'nombres'])
        
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
                
                # --- CORRECCIÓN AQUÍ ---
                # Usamos 'usuario_nombre' para que coincida con lo que pide el menú principal
                # Asegúrate que 'nombres' coincida con la cabecera de tu Excel (columna B)
                st.session_state['usuario_nombre'] = usuario.iloc[0]['nombres']
                st.session_state['usuario_codigo'] = usuario.iloc[0]['codigo']
                
                st.rerun()

# ---------------------------------------------------------
# APP PRINCIPAL (DESPUÉS DEL LOGIN)
# ---------------------------------------------------------
def mostrar_app_principal():
    with st.sidebar:
        # --- CORRECCIÓN AQUÍ ---
        # Usamos .get() para que si no encuentra el nombre, ponga "Estudiante" en vez de dar error
        nombre_mostrar = st.session_state.get('usuario_nombre', 'Estudiante')
        codigo_mostrar = st.session_state.get('usuario_codigo', '---')
        
        st.write(f"👷‍♂️ **Hola, {nombre_mostrar}**")
        st.caption(f"ID: {codigo_mostrar}")

        # ... resto del código ...
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