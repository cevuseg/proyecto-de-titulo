# Sistema de Visualización de Reportes Power BI

## Índice
1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Componentes del Sistema](#componentes-del-sistema)
5. [Guía de Instalación](#guía-de-instalación)
6. [Configuración del Sistema](#configuración-del-sistema)
7. [Manual de Usuario](#manual-de-usuario)
8. [Desarrollo y Contribución](#desarrollo-y-contribución)
9. [Requisitos del Sistema](#requisitos-del-sistema)
10. [Solución de Problemas](#solución-de-problemas)
11. [Licencia](#licencia)

## Descripción General

Este sistema es una plataforma web desarrollada en Django que permite la gestión y visualización de reportes de Power BI Report Server (PBIRS). El sistema está diseñado para proporcionar una interfaz intuitiva y segura para acceder a reportes empresariales, con un robusto sistema de control de acceso basado en roles y grupos de Windows/Active Directory.

## Características Principales

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

## Estructura del Proyecto

```
proyecto-de-titulo/
│
├── reports/                    # Aplicación principal de reportes
│   ├── __init__.py            # Archivo de inicialización de la aplicación
│   ├── admin.py               # Configuración del panel de administración
│   ├── apps.py                # Configuración de la aplicación
│   ├── decorators.py          # Decoradores personalizados
│   ├── forms.py               # Formularios de la aplicación
│   ├── middleware.py          # Middleware personalizado
│   ├── models.py              # Modelos de datos
│   ├── signals.py             # Señales de Django
│   ├── tests.py               # Pruebas unitarias
│   ├── urls.py                # Configuración de URLs
│   ├── utils.py               # Utilidades y funciones auxiliares
│   ├── views.py               # Vistas y lógica de negocio
│   ├── context_processors.py  # Procesadores de contexto
│   │
│   ├── management/           # Comandos personalizados de Django
│   ├── migrations/           # Migraciones de la base de datos
│   ├── templates/            # Plantillas HTML
│   └── templatetags/         # Etiquetas personalizadas de plantillas
│
├── powerbi_reports/          # Carpeta para reportes de Power BI
├── manage.py                 # Script de administración de Django
└── requirements.txt          # Dependencias del proyecto
```

## Componentes del Sistema

### Archivos Principales

#### manage.py
Script principal de Django que permite ejecutar comandos administrativos como:
- Crear migraciones
- Ejecutar el servidor de desarrollo
- Crear superusuarios
- Ejecutar pruebas
- Gestionar la base de datos

#### requirements.txt
Lista de dependencias del proyecto, incluyendo:
- Django y sus extensiones
- Bibliotecas para el manejo de datos
- Herramientas de desarrollo
- Dependencias de Power BI

### Carpeta reports/

#### models.py
Define la estructura de la base de datos:
- Modelos para almacenar datos de reportes
- Relaciones entre entidades
- Campos y validaciones
- Configuración de permisos

#### views.py
Contiene la lógica de negocio principal:
- Vistas para mostrar reportes
- Procesamiento de datos
- Lógica de presentación
- Control de acceso

#### urls.py
Configura las rutas URL de la aplicación:
- Mapeo de URLs a vistas
- Patrones de URL
- Nombres de URLs
- Endpoints de API

#### forms.py
Define los formularios de la aplicación:
- Validación de datos
- Campos personalizados
- Procesamiento de formularios
- Interfaz de usuario

#### utils.py
Funciones de utilidad:
- Procesamiento de datos
- Funciones auxiliares
- Herramientas comunes
- Integración con Power BI

#### decorators.py
Decoradores personalizados:
- Control de acceso
- Validación de permisos
- Funcionalidades transversales
- Seguridad

#### middleware.py
Middleware personalizado:
- Procesamiento de solicitudes
- Modificación de respuestas
- Funcionalidades globales
- Logging y monitoreo

#### signals.py
Manejo de señales de Django:
- Eventos del sistema
- Acciones automáticas
- Notificaciones
- Sincronización

#### context_processors.py
Procesadores de contexto:
- Variables globales para plantillas
- Datos compartidos
- Configuración de contexto
- Personalización

### Carpetas Especializadas

#### management/
Contiene comandos personalizados de Django para:
- Tareas administrativas
- Scripts de mantenimiento
- Herramientas de gestión
- Automatización

#### migrations/
Almacena las migraciones de la base de datos:
- Cambios en la estructura
- Actualizaciones de esquema
- Historial de modificaciones
- Control de versiones

#### templates/
Plantillas HTML:
- Diseño de páginas
- Componentes reutilizables
- Estructura visual
- Interfaz de usuario

#### templatetags/
Etiquetas personalizadas para plantillas:
- Funciones de formato
- Filtros personalizados
- Utilidades de plantilla
- Componentes UI

### powerbi_reports/
Carpeta dedicada a almacenar:
- Reportes de Power BI
- Archivos de configuración
- Recursos relacionados
- Documentación

## Guía de Instalación

### Requisitos Previos
- Python 3.8 o superior
- PostgreSQL 12 o superior
- Power BI Report Server
- Git

### Pasos de Instalación

1. **Clonar el Repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto-de-titulo
   ```

2. **Crear Entorno Virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Base de Datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear Superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar Servidor**
   ```bash
   python manage.py runserver
   ```

## Configuración del Sistema

### Configuración de Power BI
1. Configurar conexión a PBIRS en `settings.py`
2. Establecer credenciales de acceso
3. Configurar permisos de usuario

### Configuración de Base de Datos
1. Configurar PostgreSQL
2. Establecer variables de entorno
3. Ejecutar migraciones

### Configuración de Seguridad
1. Configurar autenticación
2. Establecer roles y permisos
3. Configurar grupos de Windows

## Manual de Usuario

### Acceso al Sistema
1. Navegar a la URL del sistema
2. Iniciar sesión con credenciales
3. Acceder al dashboard principal

### Gestión de Reportes
1. Ver lista de reportes disponibles
2. Filtrar por categoría o fecha
3. Exportar reportes
4. Compartir reportes

### Gestión de Usuarios
1. Crear nuevos usuarios
2. Asignar roles
3. Gestionar permisos
4. Configurar preferencias

## Desarrollo y Contribución

### Guía de Contribución
1. Fork del repositorio
2. Crear rama de desarrollo
3. Realizar cambios
4. Enviar pull request

### Estándares de Código
- PEP 8
- Docstrings
- Tests unitarios
- Documentación

### Proceso de Desarrollo
1. Planificación
2. Desarrollo
3. Testing
4. Revisión
5. Despliegue

## Requisitos del Sistema

### Requisitos Mínimos
- Python 3.8+
- Django 3.2+
- PostgreSQL 12+
- 4GB RAM
- 10GB espacio en disco

### Requisitos Recomendados
- Python 3.9+
- Django 4.0+
- PostgreSQL 13+
- 8GB RAM
- 20GB espacio en disco

## Solución de Problemas

### Problemas Comunes
1. Error de conexión a PBIRS
2. Problemas de autenticación
3. Errores de base de datos
4. Problemas de rendimiento

### Guía de Depuración
1. Revisar logs
2. Verificar configuración
3. Probar conexiones
4. Validar permisos

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
