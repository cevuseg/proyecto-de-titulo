"""
Comando de Django para generar documentación del sistema.
Genera documentación en formato Markdown sobre la configuración y uso.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from reports.models import PowerBIReport, Role, UserRole
from powerbi_reports.pbirs_client import PBIRSClient
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para generar documentación.
    Crea archivos Markdown con información del sistema.
    """
    help = 'Genera documentación del sistema de reportes'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar el directorio de salida y el formato.
        """
        parser.add_argument(
            '--output-dir',
            type=str,
            default='docs',
            help='Directorio donde guardar la documentación'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['md', 'html'],
            default='md',
            help='Formato de salida (md o html)'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la generación de documentación.
        Crea archivos con información del sistema.
        """
        try:
            self.stdout.write('Iniciando generación de documentación...')
            
            # Crear directorio de salida
            output_dir = options['output_dir']
            os.makedirs(output_dir, exist_ok=True)
            
            # Generar documentación
            self._generate_system_overview(output_dir)
            self._generate_reports_doc(output_dir)
            self._generate_roles_doc(output_dir)
            self._generate_config_doc(output_dir)
            
            self.stdout.write(self.style.SUCCESS(
                f'\nDocumentación generada en: {output_dir}'
            ))

        except Exception as e:
            logger.error(f"Error en generación de documentación: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la generación: {e}')
            )

    def _generate_system_overview(self, output_dir):
        """
        Genera documentación general del sistema.
        """
        content = f"""# Sistema de Reportes Power BI

## Descripción General
Este sistema permite la gestión y visualización de reportes de Power BI Report Server,
integrando la autenticación y autorización con roles de usuario.

## Características Principales
- Gestión de roles y permisos
- Integración con Power BI Report Server
- Panel de administración
- Sincronización automática de reportes

## Requisitos
- Python 3.8+
- Django 3.2+
- Power BI Report Server
- Base de datos PostgreSQL

## Configuración
Ver archivo `config.md` para detalles de configuración.

## Uso
Ver archivos `reports.md` y `roles.md` para instrucciones de uso.

## Última actualización
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(os.path.join(output_dir, 'overview.md'), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_reports_doc(self, output_dir):
        """
        Genera documentación de reportes.
        """
        reports = PowerBIReport.objects.all()
        
        content = """# Reportes Disponibles

## Lista de Reportes
"""
        
        for report in reports:
            content += f"""
### {report.name}
- **ID**: {report.report_id}
- **Descripción**: {report.description}
- **Workspace**: {report.workspace_id}
- **Path**: {report.path}
- **Roles con acceso**: {', '.join(role.name for role in report.roles.all())}
"""
        
        with open(os.path.join(output_dir, 'reports.md'), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_roles_doc(self, output_dir):
        """
        Genera documentación de roles.
        """
        roles = Role.objects.all()
        
        content = """# Roles y Permisos

## Roles Disponibles
"""
        
        for role in roles:
            users = User.objects.filter(userrole__role=role)
            reports = PowerBIReport.objects.filter(roles=role)
            
            content += f"""
### {role.name}
- **Descripción**: {role.description}
- **Grupo Windows**: {role.windows_group}
- **Usuarios**: {', '.join(user.username for user in users)}
- **Reportes accesibles**: {', '.join(report.name for report in reports)}
"""
        
        with open(os.path.join(output_dir, 'roles.md'), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_config_doc(self, output_dir):
        """
        Genera documentación de configuración.
        """
        pbirs_config = getattr(settings, 'PBIRS_CONFIG', {})
        
        content = """# Configuración del Sistema

## Configuración de PBIRS
"""
        
        for key, value in pbirs_config.items():
            if key in ['CLIENT_SECRET']:
                content += f"- **{key}**: [OCULTO]\n"
            else:
                content += f"- **{key}**: {value}\n"
        
        content += """
## Configuración de Django
- **DEBUG**: {settings.DEBUG}
- **ALLOWED_HOSTS**: {settings.ALLOWED_HOSTS}
- **DATABASE**: {settings.DATABASES['default']['ENGINE']}
"""
        
        with open(os.path.join(output_dir, 'config.md'), 'w', encoding='utf-8') as f:
            f.write(content) 