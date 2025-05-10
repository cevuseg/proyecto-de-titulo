# main.py
from fastapi import FastAPI
from api import rutas_auth, rutas_usuarios, rutas_reportes, rutas_permisos
from api import rutas_usuarios


from configuracion import configurar_base_de_datos

app = FastAPI(title="Sistema de Gestión de Reportes Empresariales")

# Conectar a base de datos
configurar_base_de_datos()

# Incluir las rutas (routers)
app.include_router(rutas_auth.router)
app.include_router(rutas_usuarios.router)
app.include_router(rutas_reportes.router)
app.include_router(rutas_permisos.router)

# Puedes acceder a la documentación automática en http://127.0.0.1:8000/docs
