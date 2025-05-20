"""
Comando de Django para sincronizar reportes con Power BI Report Server.
Permite sincronizar reportes desde la línea de comandos.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from reports.models import PowerBIReport
from powerbi_reports.pbirs_client import PBIRSClient
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para sincronizar reportes con PBIRS.
    Obtiene la lista de reportes del servidor y actualiza la base de datos.
    """
    help = 'Sincroniza reportes desde Power BI Report Server'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar si se debe forzar la actualización.
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar la actualización de todos los reportes'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la sincronización de reportes.
        Obtiene reportes de PBIRS y actualiza la base de datos.
        """
        try:
            self.stdout.write('Iniciando sincronización de reportes...')
            
            # Crear cliente de PBIRS
            pbirs_client = PBIRSClient()
            
            # Obtener reportes del servidor
            reports = pbirs_client.get_reports()
            
            if not reports:
                self.stdout.write(self.style.WARNING('No se encontraron reportes'))
                return

            # Contadores para estadísticas
            created = 0
            updated = 0
            unchanged = 0

            # Procesar cada reporte
            for report_data in reports:
                report, created_flag = PowerBIReport.objects.update_or_create(
                    report_id=report_data['Id'],
                    defaults={
                        'name': report_data['Name'],
                        'description': report_data.get('Description', ''),
                        'workspace_id': report_data.get('Path', ''),
                        'path': report_data.get('Path', '')
                    }
                )

                if created_flag:
                    created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Creado: {report.name}')
                    )
                elif options['force']:
                    updated += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Actualizado: {report.name}')
                    )
                else:
                    unchanged += 1

            # Mostrar resumen
            self.stdout.write(self.style.SUCCESS(
                f'\nSincronización completada:\n'
                f'  - Reportes creados: {created}\n'
                f'  - Reportes actualizados: {updated}\n'
                f'  - Reportes sin cambios: {unchanged}'
            ))

        except Exception as e:
            logger.error(f"Error en sincronización: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la sincronización: {e}')
            ) 