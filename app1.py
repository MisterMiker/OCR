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
    </style>
    """,
    unsafe_allow_html=True
)

# ---- App ----
st.title("Reconocimiento óptico de Caracteres")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

if img_file_buffer is not None:
    # Leer la imagen desde el buffer
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img
    
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    
    st.write(text)
