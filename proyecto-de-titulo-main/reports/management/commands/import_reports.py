"""
Comando de Django para importar reportes desde formato JSON.
Permite importar la configuración de reportes desde un respaldo.
"""

from django.core.management.base import BaseCommand
from django.core import serializers
from reports.models import PowerBIReport, Role
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para importar reportes desde JSON.
    Importa la configuración de reportes y roles.
    """
    help = 'Importa reportes y roles desde formato JSON'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar el archivo a importar y el comportamiento.
        """
        parser.add_argument(
            'input_file',
            type=str,
            help='Archivo JSON a importar'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar la importación sin confirmación'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Omitir reportes que ya existen'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la importación de reportes.
        Importa la configuración desde un archivo JSON.
        """
        try:
            self.stdout.write('Iniciando importación de reportes...')
            
            # Verificar archivo de entrada
            input_file = options['input_file']
            if not os.path.exists(input_file):
                self.stdout.write(
                    self.style.ERROR(f'Archivo no encontrado: {input_file}')
                )
                return
            
            # Leer archivo JSON
            with open(input_file, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Verificar estructura del archivo
            if not all(key in import_data for key in ['reports', 'roles']):
                self.stdout.write(
                    self.style.ERROR('Formato de archivo inválido')
                )
                return
            
            # Mostrar información de importación
            self.stdout.write(
                f'\nArchivo de importación:\n'
                f'  - Fecha de exportación: {import_data.get("export_date", "N/A")}\n'
                f'  - Reportes a importar: {len(import_data["reports"])}\n'
                f'  - Roles a importar: {len(import_data["roles"])}'
            )
            
            # Confirmar importación
            if not options['force']:
                confirm = input('\n¿Desea continuar con la importación? [y/N]: ')
                if confirm.lower() != 'y':
                    self.stdout.write('Operación cancelada')
                    return
            
            # Importar roles primero
            self.stdout.write('\nImportando roles...')
            for role_data in import_data['roles']:
                try:
                    role = next(serializers.deserialize('python', [role_data]))
                    if options['skip-existing'] and Role.objects.filter(
                        name=role.object.name
                    ).exists():
                        self.stdout.write(
                            self.style.WARNING(f'Omitido: {role.object.name}')
                        )
                        continue
                    role.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Importado: {role.object.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error al importar rol: {e}')
                    )
            
            # Importar reportes
            self.stdout.write('\nImportando reportes...')
            for report_data in import_data['reports']:
                try:
                    report = next(serializers.deserialize('python', [report_data]))
                    if options['skip-existing'] and PowerBIReport.objects.filter(
                        report_id=report.object.report_id
                    ).exists():
                        self.stdout.write(
                            self.style.WARNING(f'Omitido: {report.object.name}')
                        )
                        continue
                    report.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Importado: {report.object.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error al importar reporte: {e}')
                    )
            
            self.stdout.write(self.style.SUCCESS('\nImportación completada'))

        except Exception as e:
            logger.error(f"Error en importación: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la importación: {e}')
            ) 