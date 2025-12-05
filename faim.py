import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ---------------------------------------------------------
# APP PRINCIPAL (NUEVA VERSIÓN VISUAL)
# ---------------------------------------------------------
def mostrar_app_principal():
    # --- SIDEBAR (BARRA LATERAL) ---
    with st.sidebar:
        # Intenta mostrar el logo si existe
        try:
            # Asegúrate de guardar tu escudo como 'logo_minas.png' en la carpeta
            st.image("logo_minas.png", use_container_width=True)
        except:
            st.warning("Falta 'logo_minas.png'")

        st.divider()

        # Nombre bonito (Capitalizado)
        # Usa .get() por seguridad si falla la sesión
        nombre_bonito = st.session_state.get('usuario_nombre', 'Estudiante').title()
        codigo_user = st.session_state.get('usuario_codigo', '---')
        
        st.write(f"👋 **Hola, {nombre_bonito}**")
        st.caption(f"🆔 ID: {codigo_user}")
        st.divider()
        
        # --- MENÚ ACTUALIZADO (Fusionado) ---
        menu = st.radio("Navegación", 
            ["Inicio / Facultad 🏫", "Mapa Minero 🗺️", "Laboratorios 🔬", "Normativa ⚖️"]
        )
        
        st.divider()
        if st.button("Cerrar Sesión", type="primary"):
            st.session_state['logueado'] = False
            st.rerun()

    # --- CONTENIDO DE LAS PÁGINAS ---

    # 1. SECCIÓN FUSIONADA: INICIO Y FACULTAD
    if menu == "Inicio / Facultad 🏫":
        st.title("Bienvenido a la FAIM - UNCP")
        
        # Usamos TABS para organizar la información fusionada
        tab_noticias, tab_seguridad, tab_circulos = st.tabs(["📰 Noticias", "🦺 Seguridad (Croquis)", "👥 Círculos"])
        
        with tab_noticias:
            st.info("📅 **Aviso Importante:** La semana de parciales inicia el 15 de Octubre.")
            st.success("🎉 Felicitaciones al Círculo de Geomecánica por su aniversario.")

        with tab_seguridad:
            st.header("Croquis de Seguridad")
            st.write("Mapas de evacuación, extintores y zonas seguras.")
            # Aquí iría la imagen del plano de la facultad en el futuro
            st.image("https://via.placeholder.com/800x400?text=PLANO+FACULTAD+MINAS", caption="Plano de Evacuación")

        with tab_circulos:
            st.header("Grupos de Estudio y Círculos")
            col1, col2 = st.columns(2)
            with col1:
                st.write("🔹 Círculo de Geomecánica")
                st.write("🔹 Círculo de Seguridad Minera")
            with col2:
                st.write("🔹 Círculo de Ventilación")
                st.button("Solicitar unirse a un grupo +")

    # 2. SECCIÓN: MAPA MINERO (CENTRADO EN PERÚ)
    elif menu == "Mapa Minero 🗺️":
        st.title("Unidades Mineras del Perú")
        st.write("Visualización de las principales operaciones mineras.")
        
        # DATOS DE EJEMPLO (Para que el mapa muestre puntos reales en Perú)
        # En el futuro, esto vendrá de tu base de datos
        data_minas = pd.DataFrame({
            'lat': [-11.6036, -17.2521, -7.1421],
            'lon': [-76.1239, -70.6227, -78.5218],
            'Mina': ['Antamina (Ejemplo)', 'Toquepala (Ejemplo)', 'Yanacocha (Ejemplo)']
        })
        
        # CONFIGURACIÓN DEL MAPA CENTRADO EN PERÚ
        # Latitud y Longitud central aproximada de Perú y Zoom 6
        st.map(data_minas, latitude=-9.19, longitude=-75.01, zoom=6, size=20, color='#FFD700')

    # 3. SECCIÓN: LABORATORIOS (VISUAL CON IMÁGENES)
    elif menu == "Laboratorios 🔬":
        st.title("Nuestros Laboratorios")
        st.write("Selecciona un ambiente para ver detalles y equipos.")
        st.divider()

        # Grilla de 2x2
        col1, col2 = st.columns(2)
        
        with col1:
            # Usamos placeholders. REEMPLAZAR con tus imágenes reales: st.image("rocas.jpg")
            st.image("https://via.placeholder.com/300x250/333333/FFFFFF?text=Mecánica+de+Rocas", use_container_width=True)
            if st.button("🪨 Ver Mecánica de Rocas", use_container_width=True):
                st.session_state['lab_seleccionado'] = "Rocas"

            st.divider() # Espacio vertical

            st.image("https://via.placeholder.com/300x250/666666/FFFFFF?text=Ventilación", use_container_width=True)
            if st.button("💨 Ver Ventilación", use_container_width=True):
                 st.session_state['lab_seleccionado'] = "Ventilación"

        with col2:
            st.image("https://via.placeholder.com/300x250/999999/FFFFFF?text=Mineralogía", use_container_width=True)
            if st.button("💎 Ver Mineralogía", use_container_width=True):
                st.session_state['lab_seleccionado'] = "Mineralogía"
            
            st.divider() # Espacio vertical

            st.image("https://via.placeholder.com/300x250/CCCCCC/000000?text=Topografía", use_container_width=True)
            if st.button("📏 Ver Topografía", use_container_width=True):
                st.session_state['lab_seleccionado'] = "Topografía"

        # --- SECCIÓN DETALLE (Aparece abajo al hacer click) ---
        st.divider()
        lab_activo = st.session_state.get('lab_seleccionado')
        
        if lab_activo == "Rocas":
             st.header("Detalle: Mecánica de Rocas")
             st.info("Equipos: Prensa de Compresión, Máquina Los Ángeles.")
        elif lab_activo == "Mineralogía":
             st.header("Detalle: Mineralogía y Petrología")
             st.info("Colección de muestras para visus.")
        elif lab_activo:
             st.header(f"Detalle: {lab_activo}")
             st.write("Información en construcción...")


    # 4. SECCIÓN: NORMATIVA (VISUAL CON IMÁGENES)
    elif menu == "Normativa ⚖️":
        st.title("Marco Legal Minero")
        st.write("Documentos y reglamentos clave.")
        st.divider()

        col_a, col_b, col_c = st.columns(3) # Grilla de 3 columnas

        with col_a:
            st.image("https://via.placeholder.com/200x250/FF0000/FFFFFF?text=DS-024", use_container_width=True)
            if st.button("📕 Ver DS-024-2016-EM", use_container_width=True):
                st.info("Abriendo Reglamento de Seguridad y Salud Ocupacional...")

        with col_b:
             # Ejemplo de color diferente
            st.image("https://via.placeholder.com/200x250/0000FF/FFFFFF?text=Ley+General", use_container_width=True)
            if st.button("📘 Ley General de Minería", use_container_width=True):
                st.info("Abriendo Ley General...")

        with col_c:
            st.image("https://via.placeholder.com/200x250/008000/FFFFFF?text=Normas+Ambientales", use_container_width=True)
            if st.button("📗 Normativa Ambiental", use_container_width=True):
                st.info("Abriendo normas ambientales...")