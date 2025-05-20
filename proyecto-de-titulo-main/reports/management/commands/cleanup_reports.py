"""
Comando de Django para limpiar reportes obsoletos.
Permite eliminar reportes que ya no existen en Power BI Report Server.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from reports.models import PowerBIReport
from powerbi_reports.pbirs_client import PBIRSClient
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para limpiar reportes obsoletos.
    Elimina reportes que ya no existen en PBIRS.
    """
    help = 'Limpia reportes que ya no existen en Power BI Report Server'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar si se debe realizar una limpieza forzada.
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar la eliminación sin confirmación'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la limpieza de reportes.
        Identifica y elimina reportes que ya no existen en PBIRS.
        """
        try:
            self.stdout.write('Iniciando limpieza de reportes...')
            
            # Crear cliente de PBIRS
            pbirs_client = PBIRSClient()
            
            # Obtener reportes del servidor
            pbirs_reports = pbirs_client.get_reports()
            pbirs_report_ids = {report['Id'] for report in pbirs_reports}
            
            # Obtener reportes de la base de datos
            db_reports = PowerBIReport.objects.all()
            
            # Identificar reportes obsoletos
            obsolete_reports = [
                report for report in db_reports
                if report.report_id not in pbirs_report_ids
            ]
            
            if not obsolete_reports:
                self.stdout.write(self.style.SUCCESS('No hay reportes obsoletos'))
                return

            # Mostrar reportes a eliminar
            self.stdout.write('\nReportes obsoletos encontrados:')
            for report in obsolete_reports:
                self.stdout.write(f'- {report.name} (ID: {report.report_id})')

            # Confirmar eliminación
            if not options['force']:
                confirm = input('\n¿Desea eliminar estos reportes? [y/N]: ')
                if confirm.lower() != 'y':
                    self.stdout.write('Operación cancelada')
                    return

            # Eliminar reportes
            for report in obsolete_reports:
                report_name = report.name
                report.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Eliminado: {report_name}')
                )

            self.stdout.write(self.style.SUCCESS(
                f'\nLimpieza completada: {len(obsolete_reports)} reportes eliminados'
            ))

        except Exception as e:
            logger.error(f"Error en limpieza de reportes: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la limpieza: {e}')
            ) 