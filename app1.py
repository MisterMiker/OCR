import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ---- Estilos personalizados ----
st.markdown(
    """
    <style>
        .stApp {
            background-color: #c2c5aa;
            color: #582f0e;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: #582f0e !important;
        }
        .resultado {
            background-color: #e9edc9;
            padding: 15px;
            border-radius: 10px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            color: #582f0e;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Encabezado ----
st.markdown("<h1 style='text-align:center;'>📷 OCR en Streamlit</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Extrae texto de una imagen o una foto tomada con tu cámara</p>", unsafe_allow_html=True)

# ---- Captura de imagen ----
img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

# ---- Procesamiento ----
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Aplicar filtro
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    
    # Mostrar imagen procesada
    st.subheader("📸 Imagen procesada")
    st.image(img_rgb, caption="Vista previa", use_column_width=True)

    # OCR con loader
    with st.spinner("Procesando imagen..."):
        text = pytesseract.image_to_string(img_rgb)
    
    # Mostrar texto reconocido
    st.subheader("🧾 Texto detectado")
    st.markdown(f"<div class='resultado'>{text}</div>", unsafe_allow_html=True)

    # Área editable y opción de descarga
    st.text_area("Editar texto detectado", text, height=200)
    st.download_button("💾 Descargar texto", text, file_name="texto_extraido.txt")

