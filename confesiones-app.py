import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

# Fondo con degradado CSS personalizado (ejemplo: negro a púrpura de Twitch)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #010744 0%, #190336 60%, #130233 100%);
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Estilizar específicamente el botón de envío del formulario */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #9146FF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 0.6rem 1rem !important;
        transition: background-color 0.3s ease !important;
    }

    /* Efecto al pasar el cursor (Hover) */
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #772CE8 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración básica de la página
st.set_page_config(
    page_title="Shisqueic's Secrets Room",
    page_icon="assets/Shisqueic.png",
    layout="centered"
)

st.title("🌠 Confesiones Anónimas!!")

st.image("assets/Ballon dialog.png", width=500)

st.markdown(
    "⚠️IMPORTANTE⚠️ "
)

st.write("Tu mensaje se enviará de forma **100% anónima**")
st.write("‼️Comentarios sobre la streamer, contenido demasiado subido de tono, temas sensibles, amenazas, o cualquier comentario imprudente, será eliminado y no se leerá en stream.‼️")


# Comentarios sobre la streamer, contenido demasiado subido de tono, temas sensibles, amenazas, o cualquier comentario que nosotros (moderadores) veamos imprudente, será eliminado y no se leerá en stream.

# Establecer la conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulario de envío
with st.form(key="form_confesion", clear_on_submit=True):
    confesion_texto = st.text_area(
        label="Tu confesión:",
        height=150,
        max_chars=1000,
        placeholder="Escribe aquí tu confesión sin pena..."
    )
    
    btn_enviar = st.form_submit_button(label="💫 Enviar Confesión 💫")

    if btn_enviar:
        if not confesion_texto.strip():
            st.warning("Escribe algo antes de enviar tu confesión.")
        else:
            try:
                # Leer datos existentes (ttl=0 evita traer datos cacheados desactualizados)
                df_existente = conn.read(ttl=0)

                # Determinar el siguiente ID
                nuevo_id = len(df_existente) + 1 if df_existente is not None and not df_existente.empty else 1
                zona_horaria = ZoneInfo("America/Mexico_City")
                fecha_hora = datetime.now(zona_horaria).strftime("%Y-%m-%d %H:%M:%S")

                # Crear el nuevo registro
                nueva_confesion = pd.DataFrame([{
                    "ID": nuevo_id,
                    "Fecha": fecha_hora,
                    "Confesion": confesion_texto.strip(),
                    "Estatus": "Pendiente"
                }])

                # Concatenar con los datos existentes
                if df_existente is not None and not df_existente.empty:
                    df_actualizado = pd.concat([df_existente, nueva_confesion], ignore_index=True)
                else:
                    df_actualizado = nueva_confesion

                # Sobrescribir el Google Sheet con la lista actualizada
                conn.update(data=df_actualizado)

                st.success("¡Tu confesión se envió correctamente!")
            except Exception as e:
                st.error(f"Ocurrió un error al guardar la confesión: {e}")


st.link_button("🌠 Sigue a Asurenchan en todas sus Redes!!! (Click aqui) 🌠", "https://linktr.ee/asurenchan?utm_source=linktree_profile_share&ltsid=10969edd-b477-4c0e-88fb-92fc03462193", use_container_width=True)
