# Sistema de Visualización de Reportes Power BI

Este sistema permite la gestión y visualización de reportes de Power BI Report Server (PBIRS) con control de acceso basado en roles y grupos de Windows/Active Directory, desarrollado en Django.

---

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Gestión de Usuarios y Roles](#gestión-de-usuarios-y-roles)
- [Gestión de Reportes](#gestión-de-reportes)
- [Comandos Personalizados](#comandos-personalizados)
- [Buenas Prácticas](#buenas-prácticas)
- [Licencia](#licencia)

---

## Descripción General

Este sistema permite:
- Visualizar reportes de Power BI Report Server según permisos de usuario.
- Gestionar usuarios, roles y su mapeo a grupos de Windows/AD.
- Controlar el acceso a reportes mediante roles y grupos de Windows.
- Integrarse con SQL Server y PBIRS para autenticación y visualización segura.

---

## Estructura del Proyecto

```
proyecto-de-titulo-main/
├── manage.py                  # Script de administración de Django
├── requirements.txt           # Dependencias del proyecto
├── powerbi_reports/           # Configuración principal del proyecto Django
│   ├── settings.py            # Configuración global y PBIRS
│   ├── urls.py                # URLs principales
│   ├── pbirs_client.py        # Cliente para interactuar con PBIRS
│   └── ...
├── reports/                   # Aplicación principal de reportes
│   ├── models.py              # Modelos de datos: roles, usuarios, reportes
│   ├── views.py               # Vistas y lógica de negocio
│   ├── urls.py                # URLs de la app de reportes
│   ├── admin.py               # Configuración del panel de administración
│   ├── forms.py               # Formularios de gestión
│   ├── templates/             # Plantillas HTML
│   ├── management/commands/   # Comandos personalizados de Django
│   └── ...
└── ...
```

---

## Requisitos
- Python 3.8 o superior
- SQL Server instalado y configurado
- Power BI Report Server instalado y configurado
- Acceso a usuarios y grupos de Windows/AD

---

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd proyecto-de-titulo-main
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos y PBIRS
- Edita `powerbi_reports/settings.py`:
  - Configura la sección `DATABASES` para tu SQL Server.
  - Ajusta las credenciales y URLs en `PBIRS_CONFIG`.

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor
```bash
python manage.py runserver
```

---

## Gestión de Usuarios y Roles

- **Usuarios**: Se gestionan desde el panel de administración web (`/admin`) o desde el panel personalizado.
- **Roles**: Se pueden crear, editar y eliminar. Cada rol puede mapearse a un grupo de Windows/AD (campo `windows_group`).
- **Asignación**: Los usuarios pueden tener múltiples roles. Los roles controlan el acceso a reportes.
- **Cambio de contraseña**: Se puede cambiar desde el panel de usuarios.

---

## Gestión de Reportes

- Los reportes de Power BI se sincronizan automáticamente desde PBIRS.
- Cada reporte puede asignarse a uno o varios roles.
- Los usuarios solo ven los reportes para los que tienen permisos según su rol y grupo de Windows.

---

## Comandos Personalizados

El sistema incluye varios comandos de administración:

- `sync_reports`: Sincroniza los reportes desde PBIRS.
- `check_permissions`: Verifica los permisos de usuarios y roles en PBIRS.
- `cleanup_reports`: Elimina reportes obsoletos que ya no existen en PBIRS.
- `export_reports`: Exporta la configuración de reportes y roles a JSON.
- `import_reports`: Importa reportes y roles desde un archivo JSON.
- `backup_reports`: Realiza un respaldo completo de la configuración y datos.
- `validate_config`: Valida la configuración del sistema y la conexión con PBIRS.
- `generate_docs`: Genera documentación automática del sistema.

Ejemplo de uso:
```bash
python manage.py sync_reports
python manage.py check_permissions --user <usuario>
```

---

## Buenas Prácticas
- Mantén sincronizados los roles de Django y los grupos de Windows/AD.
- Asigna permisos en PBIRS solo a los grupos, no a usuarios individuales.
- Usa HTTPS en producción.
- Mantén el archivo `.env` seguro y fuera del control de versiones.
- Realiza copias de seguridad regulares usando los comandos incluidos.
- Actualiza las dependencias periódicamente.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles. 