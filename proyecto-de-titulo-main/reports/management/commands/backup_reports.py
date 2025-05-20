"""
Comando de Django para realizar respaldos del sistema.
Permite respaldar la configuración y datos de reportes.
"""

from django.core.management.base import BaseCommand
from django.core import serializers
from reports.models import PowerBIReport, Role, UserRole
from django.conf import settings
import json
import os
import shutil
from datetime import datetime
import logging
import zipfile

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para realizar respaldos.
    Crea archivos de respaldo con la configuración y datos.
    """
    help = 'Realiza respaldo del sistema de reportes'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar el directorio de salida y el tipo de respaldo.
        """
        parser.add_argument(
            '--output-dir',
            type=str,
            default='backups',
            help='Directorio donde guardar los respaldos'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['full', 'config', 'data'],
            default='full',
            help='Tipo de respaldo (full, config, data)'
        )

    def handle(self, *args, **options):
        """
        Ejecuta el respaldo del sistema.
        Crea archivos de respaldo según el tipo especificado.
        """
        try:
            self.stdout.write('Iniciando respaldo del sistema...')
            
            # Crear directorio de salida
            output_dir = options['output_dir']
            os.makedirs(output_dir, exist_ok=True)
            
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(output_dir, f'backup_{timestamp}')
            os.makedirs(backup_dir)
            
            # Realizar respaldo según el tipo
            if options['type'] in ['full', 'config']:
                self._backup_config(backup_dir)
            
            if options['type'] in ['full', 'data']:
                self._backup_data(backup_dir)
            
            # Crear archivo ZIP
            zip_file = f'{backup_dir}.zip'
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_dir)
                        zipf.write(file_path, arcname)
            
            # Eliminar directorio temporal
            shutil.rmtree(backup_dir)
            
            self.stdout.write(self.style.SUCCESS(
                f'\nRespaldo completado:\n'
                f'  - Archivo: {zip_file}\n'
                f'  - Tipo: {options["type"]}'
            ))

        except Exception as e:
            logger.error(f"Error en respaldo: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante el respaldo: {e}')
            )

    def _backup_config(self, backup_dir):
        """
        Realiza respaldo de la configuración.
        """
        self.stdout.write('Respaldando configuración...')
        
        # Respaldar configuración de PBIRS
        pbirs_config = getattr(settings, 'PBIRS_CONFIG', {})
        config_data = {
            'pbirs_config': pbirs_config,
            'django_settings': {
                'DEBUG': settings.DEBUG,
                'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
                'DATABASE': settings.DATABASES['default']['ENGINE'],
            }
        }
        
        with open(os.path.join(backup_dir, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)

    def _backup_data(self, backup_dir):
        """
        Realiza respaldo de los datos.
        """
        self.stdout.write('Respaldando datos...')
        
        # Respaldar reportes
        reports = PowerBIReport.objects.all()
        reports_data = serializers.serialize('python', reports)
        
        # Respaldar roles
        roles = Role.objects.all()
        roles_data = serializers.serialize('python', roles)
        
        # Respaldar asignaciones de roles
        user_roles = UserRole.objects.all()
        user_roles_data = serializers.serialize('python', user_roles)
        
        # Guardar datos
        data = {
            'reports': reports_data,
            'roles': roles_data,
            'user_roles': user_roles_data,
            'backup_date': datetime.now().isoformat(),
            'total_reports': len(reports),
            'total_roles': len(roles),
            'total_user_roles': len(user_roles)
        }
        
        with open(os.path.join(backup_dir, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2) 