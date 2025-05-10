import streamlit as st

def mostrar_admin_panel():
    st.set_page_config(page_title="Panel de Administración", page_icon="🛠️", layout="wide")

    # Ocultar menú, header y footer
    st.markdown("""
        <style>
            #MainMenu, header, footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # Divide pantalla en menú lateral (20%) y contenido (80%)
    menu, contenido = st.columns([1, 4])  # ajusta proporción si quieres más o menos ancho

    with menu:
        st.markdown("### 🔲 Menú")
        st.button("📁 Reportes")
        st.button("👥 admin.usuarios")
        st.markdown("<hr style='border-left: 2px solid black; height: 100vh; position: absolute; right: 0;'>",
                    unsafe_allow_html=True)

    with contenido:
        st.markdown("## 🧭 PANEL DE ADMINISTRACIÓN")
        st.markdown("#### TEXTO DE INFORMACIÓN")
        st.write("Aquí podrás gestionar módulos del sistema, usuarios y reportes.")

    # Botón de cerrar sesión
    st.markdown("---")
    if st.button("🔒 Cerrar sesión"):
        st.session_state.clear()
        st.success("Sesión cerrada correctamente.")
        st.rerun()
