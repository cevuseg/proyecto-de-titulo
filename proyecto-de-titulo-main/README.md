# 🚀 Sistema de Visualización de Reportes Power BI

<div align="center">

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

[![Documentation](https://img.shields.io/badge/Documentation-Complete-blue?style=for-the-badge)](https://github.com/your-repo/docs)
[![Version](https://img.shields.io/badge/Version-1.0.0-green?style=for-the-badge)](https://github.com/your-repo/releases)

</div>

## 📋 Índice
- [🎯 Descripción General](#-descripción-general)
- [✨ Características Principales](#-características-principales)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔧 Componentes del Sistema](#-componentes-del-sistema)
- [🚀 Guía de Instalación](#-guía-de-instalación)
- [⚙️ Configuración del Sistema](#-configuración-del-sistema)
- [📖 Manual de Usuario](#-manual-de-usuario)
- [👨‍💻 Desarrollo y Contribución](#-desarrollo-y-contribución)
- [💻 Requisitos del Sistema](#-requisitos-del-sistema)
- [🔍 Solución de Problemas](#-solución-de-problemas)
- [🔒 Seguridad](#-seguridad)
- [🛠️ Mantenimiento](#-mantenimiento)
- [📚 API y Documentación](#-api-y-documentación)
- [🚀 Despliegue](#-despliegue)
- [🏗️ Arquitectura del Sistema](#-arquitectura-del-sistema)
- [🔄 Guía de Migración](#-guía-de-migración)
- [⭐ Mejores Prácticas](#-mejores-prácticas)
- [📞 Contacto y Soporte](#-contacto-y-soporte)

## 🎯 Descripción General

Este sistema es una plataforma web desarrollada en Django que permite la gestión y visualización de reportes de Power BI Report Server (PBIRS). El sistema está diseñado para proporcionar una interfaz intuitiva y segura para acceder a reportes empresariales, con un robusto sistema de control de acceso basado en roles y grupos de Windows/Active Directory.

<div align="center">
  <img src="https://via.placeholder.com/800x400?text=Sistema+de+Reportes" alt="Sistema de Reportes" width="800"/>
</div>

## ✨ Características Principales

<div align="center">

| 🔐 Seguridad | 📊 Visualización | 👥 Gestión |
|:------------:|:---------------:|:----------:|
| Autenticación 2FA | Reportes Interactivos | Usuarios y Roles |
| Control de Acceso | KPIs en Tiempo Real | Grupos Windows/AD |
| Encriptación | Exportación Múltiple | Permisos Granulares |

</div>

### 🚀 Características Destacadas
- 🔐 Autenticación y autorización basada en roles
- 📊 Integración nativa con Power BI Report Server
- 👥 Gestión de usuarios y grupos de Windows/AD
- 📱 Interfaz responsiva y moderna
- 🔄 Sincronización automática de reportes
- 📈 Visualización de métricas y KPIs
- 🔍 Búsqueda avanzada de reportes
- 📱 Soporte para dispositivos móviles
- 📊 Exportación de datos en múltiples formatos
- 🔔 Sistema de notificaciones

## 📁 Estructura Detallada del Proyecto

### 📂 Estructura Principal
```
proyecto-de-titulo/
│
├──README.md
├── proyecto-de-titulo-main/
    │
    │
    ├── 📂 reports/                    # Aplicación principal de reportes
    │   ├── 📄 __init__.py            # Inicialización de la aplicación
    │   ├── 📄 admin.py               # Configuración del panel de administración
    │   ├── 📄 apps.py                # Configuración de la aplicación
    │   ├── 📄 decorators.py          # Decoradores personalizados
    │   ├── 📄 forms.py               # Formularios de la aplicación
    │   ├── 📄 middleware.py          # Middleware personalizado
    │   ├── 📄 models.py              # Modelos de datos
    │   ├── 📄 signals.py             # Señales de Django
    │   ├── 📄 tests.py               # Pruebas unitarias
    │   ├── 📄 urls.py                # Configuración de URLs
    │   ├── 📄 utils.py               # Utilidades y funciones auxiliares
    │   ├── 📄 views.py               # Vistas y lógica de negocio
    │   │
    │   ├── 📂 management/           # Comandos personalizados
    │   │   └── 📂 commands/         # Scripts de administración
    │   │
    │   ├── 📂 migrations/           # Migraciones de la base de datos
    │   │   └── 📄 __init__.py
    │   │
    │   ├── 📂 templates/            # Plantillas HTML
    │   │   └── 📂 reports/
    │   │       ├── 📄 base.html           # Plantilla base
    │   │       ├── 📄 login.html          # Página de inicio de sesión
    │   │       ├── 📄 dashboard.html      # Panel principal
    │   │       ├── 📄 view_report.html    # Visualización de reportes
    │   │       ├── 📄 manage_users.html   # Gestión de usuarios
    │   │       └── 📄 manage_roles.html   # Gestión de roles
    │   │
    │   └── 📂 templatetags/         # Etiquetas personalizadas
    │       └── 📄 custom_tags.py    # Etiquetas personalizadas
    │
    ├── 📂 powerbi_reports/          # Reportes Power BI
    ├── 📄 manage.py                 # Script de administración
    └── 📄 requirements.txt          # Dependencias
```

### 📄 Descripción Detallada de Archivos

#### 📂 Archivos Principales

##### 📄 manage.py
Script principal de Django que permite:
- Ejecutar el servidor de desarrollo
- Crear migraciones
- Aplicar migraciones
- Crear superusuarios
- Ejecutar pruebas

##### 📄 requirements.txt
Lista de dependencias del proyecto:
- Django y extensiones
- Bibliotecas de Power BI
- Herramientas de desarrollo
- Dependencias de base de datos

#### 📂 Carpeta reports/

##### 📄 models.py
Define la estructura de la base de datos:
- Modelo de Usuario
- Modelo de Rol
- Modelo de Reporte
- Modelo de Permiso
- Relaciones entre modelos

##### 📄 views.py
Contiene la lógica de negocio:
- Vistas de autenticación
- Vistas de reportes
- Vistas de gestión de usuarios
- Vistas de gestión de roles
- Vistas de dashboard

##### 📄 urls.py
Configura las rutas URL:
- Rutas de autenticación
- Rutas de reportes
- Rutas de administración
- Rutas de API

##### 📄 forms.py
Define los formularios:
- Formulario de login
- Formulario de usuario
- Formulario de rol
- Formulario de reporte

##### 📄 utils.py
Funciones de utilidad:
- Procesamiento de datos
- Integración con Power BI
- Funciones de seguridad
- Herramientas comunes

#### 📂 Plantillas HTML

##### 📄 base.html
Plantilla base que define:
- Estructura HTML común
- Menú de navegación
- Pie de página
- Estilos globales
- Scripts comunes

##### 📄 login.html
Página de inicio de sesión con:
- Formulario de login
- Validación de credenciales
- Mensajes de error
- Enlaces de recuperación

##### 📄 dashboard.html
Panel principal que muestra:
- Resumen de reportes
- KPIs principales
- Accesos rápidos
- Notificaciones

##### 📄 view_report.html
Visualización de reportes con:
- Integración Power BI
- Controles de filtrado
- Opciones de exportación
- Compartir reportes

##### 📄 manage_users.html
Gestión de usuarios incluye:
- Lista de usuarios
- Formulario de creación
- Edición de permisos
- Asignación de roles

##### 📄 manage_roles.html
Gestión de roles con:
- Lista de roles
- Permisos por rol
- Asignación de usuarios
- Configuración de acceso

#### 📂 Carpetas Especializadas

##### 📂 management/commands/
Scripts de administración:
- Sincronización de reportes
- Backup de datos
- Limpieza de sistema
- Tareas programadas

##### 📂 migrations/
Archivos de migración:
- Cambios en modelos
- Actualizaciones de esquema
- Datos iniciales
- Rollbacks

##### 📂 templatetags/
Etiquetas personalizadas:
- Filtros de formato
- Funciones de utilidad
- Componentes reutilizables
- Helpers de plantilla

### 🔄 Flujo de Datos

1. **Autenticación**
   - Usuario accede a login.html
   - Credenciales validadas en views.py
   - Redirección a dashboard.html

2. **Visualización**
   - Usuario selecciona reporte
   - view_report.html carga datos
   - Power BI renderiza visualización

3. **Gestión**
   - Administrador accede a manage_users.html
   - Gestiona roles en manage_roles.html
   - Cambios reflejados en base de datos

### 📊 Integración con Power BI

1. **Conexión**
   - Configuración en settings.py
   - Autenticación con PBIRS
   - Manejo de tokens

2. **Visualización**
   - Embedding de reportes
   - Filtros dinámicos
   - Exportación de datos

3. **Sincronización**
   - Actualización automática
   - Caché de reportes
   - Manejo de errores

## 🚀 Guía de Instalación

### 📋 Requisitos Previos
- Python 3.8+
- PostgreSQL 12+
- Power BI Report Server
- Git

### 🛠️ Pasos de Instalación

```bash
# 1. Clonar el Repositorio
git clone <url-del-repositorio>
cd proyecto-de-titulo

# 2. Crear Entorno Virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar Dependencias
pip install -r requirements.txt

# 4. Configurar Base de Datos
python manage.py migrate

# 5. Crear Superusuario
python manage.py createsuperuser

# 6. Iniciar Servidor
python manage.py runserver
```

## 💻 Requisitos del Sistema

<div align="center">

| Componente | Mínimo | Recomendado |
|:----------:|:------:|:-----------:|
| Python | 3.8+ | 3.9+ |
| Django | 3.2+ | 4.0+ |
| PostgreSQL | 12+ | 13+ |
| RAM | 4GB | 8GB |
| Disco | 10GB | 20GB |

</div>

## 📞 Contacto y Soporte

<div align="center">

| Canal | Detalles |
|:-----:|:---------|
| 📧 Email | soporte@ejemplo.com |
| 💬 Slack | #soporte-proyecto |
| 🎫 Jira | Proyecto de Soporte |
| 📱 Chat | En vivo 24/7 |

</div>

### ⏰ Horario de Soporte
- 🏢 Lunes a Viernes: 9:00 - 18:00
- 🚨 Emergencias: 24/7
- ⭐ Soporte prioritario: 8:00 - 20:00

### 📚 Recursos Adicionales
- 🎥 Video tutoriales
- 📊 Webinars mensuales
- 📖 Documentación técnica
- 👥 Guías de usuario
- 💻 Ejemplos de código
- 🏆 Casos de éxito



---

<div align="center">
  <sub>Construido con ❤️ por el equipo de desarrollo</sub>
</div> 
