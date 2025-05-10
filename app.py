import streamlit as st
from frontend.login import mostrar_login
from frontend.user_panel import mostrar_user_panel
from frontend.admin_panel import mostrar_admin_panel

# Inicializa variables de sesión
if "auth" not in st.session_state:
    st.session_state["auth"] = False
    st.session_state["rol"] = ""
    st.session_state["token"] = ""
    st.session_state["correo"] = ""

# Renderizar vista según estado
if not st.session_state["auth"]:
    mostrar_login()
else:
    if st.session_state["rol"] == "admin":
        mostrar_admin_panel()
    else:
        mostrar_user_panel()
