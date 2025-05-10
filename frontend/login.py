import streamlit as st
import requests
import os
import base64  # Necesario para codificar la imagen en base64

# URL del backend (puede venir desde .env o variable de entorno)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


# Función principal del login
def mostrar_login():
    # Configuración general
    st.set_page_config(page_title="Inicio de sesión", layout="wide", initial_sidebar_state="collapsed")

     # lado izquierdo, separador, lado derecho
    col1, col_sep, col2 = st.columns([1, 0.02, 1])

    # ======================== LADO IZQUIERDO ============================
    with col1:
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
          # Mostrar imagen desde carpeta local
        col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.image("imagenes/logo.png", width=100)
        # Espacio vertical superior
        

        # Títulos centrados
        st.markdown("<h3 style='text-align: center;'>Sistema de Reportes</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center;'>Puedes visualizar gráficos, reportes y acceder según tu rol.</p>",
            unsafe_allow_html=True
        )
         # ================= SEPARADOR =================
    with col_sep:
        st.markdown(
            """
            <div style='height: 80vh; width: 4px; background-color: #000000; margin: auto;'></div>
            """,
            unsafe_allow_html=True
        )


    # ======================== LADO DERECHO ============================
    with col2:
        # Imagen superior centrada (icono usuario)
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-right: 20px;">
                <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Título centrado
        st.markdown(
            """
            <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; margin-top: 30px;'>
                <h3 style='margin-bottom: 20px;'>Login</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Formulario de inicio de sesión
        correo = st.text_input("Correo")
        contrasena = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if not correo or not contrasena:
                st.warning("Por favor completa todos los campos.")
                return

            try:
                response = requests.post(
                    f"{BACKEND_URL}/login",
                    json={"correo": correo, "contrasena": contrasena}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state["auth"] = True
                    st.session_state["token"] = data["access_token"]
                    st.session_state["correo"] = correo

                    user_data = requests.get(
                        f"{BACKEND_URL}/usuarios/correo/{correo}",
                        headers={"Authorization": f"Bearer {data['access_token']}"}
                    )

                    if user_data.status_code == 200:
                        st.session_state["rol"] = user_data.json()["rol"]
                        st.success("Sesión iniciada correctamente.")
                        st.rerun()
                    else:
                        st.error("No se pudo obtener el rol del usuario.")
                else:
                    st.error("Credenciales incorrectas.")
            except Exception as e:
                st.error(f"Error al conectar con el servidor: {e}")
