import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Facultad de Minas - UNCP",
    page_icon="⛏️",
    layout="wide" # Usamos 'wide' para que el mapa y las fotos se vean mejor
)

# ---------------------------------------------------------
# 2. GESTIÓN DE DATOS (CONEXIÓN GOOGLE SHEETS)
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def cargar_padron_alumnos():
    # PEGA TU LINK AQUÍ (El mismo que ya te funcionaba)
    url_sheet = "https://docs.google.com/spreadsheets/d/15IDFloqIsKMEUk6_GqY-kf16HdSeycwwFzjh8_yy9rw/edit" 

    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=url_sheet)
        df = df.astype(str)
        
        # Limpieza de columnas
        df.columns = df.columns.str.lower().str.strip()
        
        if 'codigo' not in df.columns:
            # Retorno de emergencia si falla la estructura
            return pd.DataFrame(columns=['codigo', 'nombres'])
            
        df['codigo'] = df['codigo'].str.strip().str.upper()
        return df
        
    except Exception as e:
        # En producción podrías ocultar este error, pero sirve para depurar
        # st.error(f"Error: {e}") 
        return pd.DataFrame(columns=['codigo', 'nombres'])

# ---------------------------------------------------------
# 3. INTERFAZ DE LOGIN
# ---------------------------------------------------------
def mostrar_login():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.image("logo_minas.png", use_container_width=True)
        except:
            st.header("UNCP - MINAS")
            
        st.subheader("Acceso Estudiantil")

        codigo_input = st.text_input("Ingresa tu Código de Matrícula", max_chars=11)
        
        if st.button("Ingresar", type="primary", use_container_width=True):
            df_alumnos = cargar_padron_alumnos()
            
            # Buscamos el código
            usuario = df_alumnos[df_alumnos['codigo'] == codigo_input.strip().upper()]
            
            if not usuario.empty:
                st.session_state['logueado'] = True
                # Guardamos los datos en sesión de forma segura
                st.session_state['usuario_nombre'] = usuario.iloc[0]['nombres']
                st.session_state['usuario_codigo'] = usuario.iloc[0]['codigo']
                st.rerun()
            else:
                st.error("Código no encontrado o error de conexión.")

# ---------------------------------------------------------
# 4. APP PRINCIPAL (CON TU NUEVO DISEÑO VISUAL)
# ---------------------------------------------------------
def mostrar_app_principal():
    # --- SIDEBAR ---
    with st.sidebar:
        try:
            st.image("logo_minas.png", use_container_width=True)
        except:
            st.warning("Falta 'logo_minas.png'")

        st.divider()

        nombre_bonito = st.session_state.get('usuario_nombre', 'Estudiante').title()
        codigo_user = st.session_state.get('usuario_codigo', '---')
        
        st.write(f"👋 **Hola, {nombre_bonito}**")
        st.caption(f"🆔 ID: {codigo_user}")
        st.divider()
        
        menu = st.radio("Navegación", 
            ["Inicio / Facultad 🏫", "Mapa Minero 🗺️", "Laboratorios 🔬", "Normativa ⚖️"]
        )
        
        st.divider()
        if st.button("Cerrar Sesión", type="primary"):
            st.session_state['logueado'] = False
            st.rerun()

    # --- CONTENIDO ---
    
    # SECCIÓN 1: INICIO Y FACULTAD
    if menu == "Inicio / Facultad 🏫":
        st.title("Bienvenido a la FAIM - UNCP")
        tab_noticias, tab_seguridad, tab_circulos = st.tabs(["📰 Noticias", "🦺 Seguridad", "👥 Círculos"])
        
        with tab_noticias:
            st.info("📅 **Aviso:** Parciales inician el 15 de Octubre.")
            st.success("🎉 Aniversario del Círculo de Geomecánica.")

        with tab_seguridad:
            st.header("Seguridad y Evacuación")
            st.image("https://via.placeholder.com/800x400?text=AQUI+IRA+EL+CROQUIS", caption="Plano de Seguridad")

        with tab_circulos:
            st.header("Grupos de Estudio")
            col1, col2 = st.columns(2)
            with col1:
                st.write("🔹 Círculo de Geomecánica")
                st.write("🔹 Círculo de Seguridad Minera")
            with col2:
                st.write("🔹 Círculo de Ventilación")
                st.button("Unirme a un grupo +")

    # SECCIÓN 2: MAPA MINERO
    elif menu == "Mapa Minero 🗺️":
        st.title("Unidades Mineras del Perú")
        # Datos ficticios para ejemplo
        data_minas = pd.DataFrame({
            'lat': [-11.6036, -17.2521, -7.1421],
            'lon': [-76.1239, -70.6227, -78.5218],
            'Mina': ['Antamina', 'Toquepala', 'Yanacocha']
        })
        st.map(data_minas, latitude=-9.19, longitude=-75.01, zoom=5, size=20, color='#FFD700')

    # SECCIÓN 3: LABORATORIOS
    elif menu == "Laboratorios 🔬":
        st.title("Laboratorios FAIM")
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("https://via.placeholder.com/300x200/333333/FFFFFF?text=Rocas", use_container_width=True)
            if st.button("🪨 Mecánica de Rocas", use_container_width=True):
                st.session_state['lab_view'] = "Rocas"
            st.divider()
            st.image("https://via.placeholder.com/300x200/666666/FFFFFF?text=Ventilacion", use_container_width=True)
            if st.button("💨 Ventilación", use_container_width=True):
                 st.session_state['lab_view'] = "Ventilación"

        with col2:
            st.image("https://via.placeholder.com/300x200/999999/FFFFFF?text=Mineralogia", use_container_width=True)
            if st.button("💎 Mineralogía", use_container_width=True):
                st.session_state['lab_view'] = "Mineralogía"
            st.divider()
            st.image("https://via.placeholder.com/300x200/CCCCCC/000000?text=Topografia", use_container_width=True)
            if st.button("📏 Topografía", use_container_width=True):
                st.session_state['lab_view'] = "Topografía"
        
        # Detalle del lab seleccionado
        lab_actual = st.session_state.get('lab_view')
        if lab_actual:
            st.divider()
            st.subheader(f"Información: {lab_actual}")
            st.info("Selecciona un laboratorio arriba para ver sus detalles.")

    # SECCIÓN 4: NORMATIVA
    elif menu == "Normativa ⚖️":
        st.title("Marco Legal")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image("https://via.placeholder.com/200x250?text=DS-024", use_container_width=True)
            st.button("Ver DS-024")
        with c2:
            st.image("https://via.placeholder.com/200x250?text=Ley+General", use_container_width=True)
            st.button("Ver Ley General")
        with c3:
            st.image("https://via.placeholder.com/200x250?text=Ambiental", use_container_width=True)
            st.button("Ver Normas Amb.")

# ---------------------------------------------------------
# 5. CONTROL DE FLUJO (¡ESTO ES LO QUE FALTABA!)
# ---------------------------------------------------------
if 'logueado' not in st.session_state:
    st.session_state['logueado'] = False

if st.session_state['logueado']:
    mostrar_app_principal()  # <--- AQUÍ SE LLAMA A TU APP
else:
    mostrar_login()          # <--- AQUÍ SE LLAMA AL LOGIN