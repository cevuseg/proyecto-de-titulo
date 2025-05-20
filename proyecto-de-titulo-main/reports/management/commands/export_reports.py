"""
Comando de Django para exportar reportes a formato JSON.
Permite exportar la configuración de reportes para respaldo o migración.
"""

from django.core.management.base import BaseCommand
from django.core import serializers
from reports.models import PowerBIReport, Role
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para exportar reportes a JSON.
    Exporta la configuración de reportes y roles.
    """
    help = 'Exporta reportes y roles a formato JSON'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar el directorio de salida y el formato.
        """
        parser.add_argument(
            '--output-dir',
            type=str,
            default='exports',
            help='Directorio donde guardar los archivos exportados'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'pretty'],
            default='pretty',
            help='Formato de salida (json o pretty)'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la exportación de reportes.
        Exporta la configuración a archivos JSON.
        """
        try:
            self.stdout.write('Iniciando exportación de reportes...')
            
            # Crear directorio de salida si no existe
            output_dir = options['output_dir']
            os.makedirs(output_dir, exist_ok=True)
            
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Exportar reportes
            reports = PowerBIReport.objects.all()
            reports_data = serializers.serialize('python', reports)
            
            # Exportar roles
            roles = Role.objects.all()
            roles_data = serializers.serialize('python', roles)
            
            # Preparar datos para exportación
            export_data = {
                'reports': reports_data,
                'roles': roles_data,
                'export_date': timestamp,
                'total_reports': len(reports),
                'total_roles': len(roles)
            }
            
            # Guardar archivo
            output_file = os.path.join(output_dir, f'reports_export_{timestamp}.json')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if options['format'] == 'pretty':
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(export_data, f, ensure_ascii=False)
            
            self.stdout.write(self.style.SUCCESS(
                f'\nExportación completada:\n'
                f'  - Archivo: {output_file}\n'
                f'  - Reportes exportados: {len(reports)}\n'
                f'  - Roles exportados: {len(roles)}'
            ))

        except Exception as e:
            logger.error(f"Error en exportación: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la exportación: {e}')
            ) 