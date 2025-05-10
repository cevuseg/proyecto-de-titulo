import streamlit as st

def mostrar_user_panel():
    st.set_page_config(page_title="Panel de Usuario", layout="wide")

    # Ocultar menú lateral y barra superior
    st.markdown("""
        <style>
            #MainMenu, header, footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # ================== PANEL SUPERIOR ==================
    col_logo, col_titulo = st.columns([1, 6])
    with col_logo:
        if st.button("🔒 Cerrar sesión"):
            st.session_state.clear()
            st.success("Sesión cerrada correctamente.")
            st.rerun()

    with col_titulo:
        st.markdown("<h3 style='text-align: center;'>📊 Sistema de Reportes</h3>", unsafe_allow_html=True)

    st.markdown("---")

    # ================== PANEL PRINCIPAL ==================
    col1, col2 = st.columns([1, 4])

    # ----------- LADO IZQUIERDO: Árbol de sucursales y áreas -----------
    with col1:
        st.markdown("### 🏢 Sucursal")
        with st.expander("📍 Santiago", expanded=True):
            st.markdown("- Ventas")
            st.markdown("- Finanzas")
        with st.expander("📍 Valparaíso", expanded=True):
            st.markdown("- Marketing")
            st.markdown("- TI")

    # ----------- LADO DERECHO: Reportes y búsqueda -----------
    with col2:
        st.text_input("📂 Ruta actual", value="Santiago\\Ventas")

        st.markdown("### Reportes disponibles")

        col_r1, col_r2, col_r3, col_add = st.columns(4)

        with col_r1:
            st.markdown("📄\n\n2023")

        with col_r2:
            st.markdown("📄\n\n2024")

        with col_r3:
            st.markdown("📄\n\n2025")

        with col_add:
            st.markdown("➕\n\nAgregar")
