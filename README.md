# Proyecto de Título - Sistema de Reportes

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

## Descripción de Componentes

### Archivos Principales

#### manage.py
Script principal de Django que permite ejecutar comandos administrativos como:
- Crear migraciones
- Ejecutar el servidor de desarrollo
- Crear superusuarios
- Ejecutar pruebas

#### requirements.txt
Lista de dependencias del proyecto, incluyendo:
- Django y sus extensiones
- Bibliotecas para el manejo de datos
- Herramientas de desarrollo

### Carpeta reports/

#### models.py
Define la estructura de la base de datos:
- Modelos para almacenar datos de reportes
- Relaciones entre entidades
- Campos y validaciones

#### views.py
Contiene la lógica de negocio principal:
- Vistas para mostrar reportes
- Procesamiento de datos
- Lógica de presentación

#### urls.py
Configura las rutas URL de la aplicación:
- Mapeo de URLs a vistas
- Patrones de URL
- Nombres de URLs

#### forms.py
Define los formularios de la aplicación:
- Validación de datos
- Campos personalizados
- Procesamiento de formularios

#### utils.py
Funciones de utilidad:
- Procesamiento de datos
- Funciones auxiliares
- Herramientas comunes

#### decorators.py
Decoradores personalizados:
- Control de acceso
- Validación de permisos
- Funcionalidades transversales

#### middleware.py
Middleware personalizado:
- Procesamiento de solicitudes
- Modificación de respuestas
- Funcionalidades globales

#### signals.py
Manejo de señales de Django:
- Eventos del sistema
- Acciones automáticas
- Notificaciones

#### context_processors.py
Procesadores de contexto:
- Variables globales para plantillas
- Datos compartidos
- Configuración de contexto

### Carpetas Especializadas

#### management/
Contiene comandos personalizados de Django para:
- Tareas administrativas
- Scripts de mantenimiento
- Herramientas de gestión

#### migrations/
Almacena las migraciones de la base de datos:
- Cambios en la estructura
- Actualizaciones de esquema
- Historial de modificaciones

#### templates/
Plantillas HTML:
- Diseño de páginas
- Componentes reutilizables
- Estructura visual

#### templatetags/
Etiquetas personalizadas para plantillas:
- Funciones de formato
- Filtros personalizados
- Utilidades de plantilla

### powerbi_reports/
Carpeta dedicada a almacenar:
- Reportes de Power BI
- Archivos de configuración
- Recursos relacionados

## Instalación y Uso

1. Clonar el repositorio
2. Crear un entorno virtual
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar migraciones: `python manage.py migrate`
5. Iniciar el servidor: `python manage.py runserver`

## Requisitos del Sistema

- Python 3.8 o superior
- Django 3.2 o superior
- Base de datos compatible (PostgreSQL recomendado)
- Navegador web moderno

## Contribución

Para contribuir al proyecto:
1. Crear una rama para la nueva funcionalidad
2. Realizar cambios y pruebas
3. Enviar un pull request con la descripción de los cambios

## Licencia

Este proyecto está bajo la Licencia MIT. 
