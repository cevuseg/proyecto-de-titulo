"""
Comando de Django para verificar permisos en Power BI Report Server.
Permite validar los permisos de usuarios y roles en PBIRS.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reports.models import Role, UserRole, PowerBIReport
from powerbi_reports.pbirs_client import PBIRSClient
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para verificar permisos en PBIRS.
    Valida los permisos de usuarios y roles en el servidor de reportes.
    """
    help = 'Verifica permisos de usuarios y roles en Power BI Report Server'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar usuarios o roles específicos a verificar.
        """
        parser.add_argument(
            '--user',
            type=str,
            help='Verificar permisos de un usuario específico'
        )
        parser.add_argument(
            '--role',
            type=str,
            help='Verificar permisos de un rol específico'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la verificación de permisos.
        Valida los permisos en PBIRS y muestra los resultados.
        """
        try:
            self.stdout.write('Iniciando verificación de permisos...')
            
            # Crear cliente de PBIRS
            pbirs_client = PBIRSClient()
            
            # Obtener todos los reportes
            reports = PowerBIReport.objects.all()
            
            if not reports:
                self.stdout.write(self.style.WARNING('No hay reportes para verificar'))
                return

            # Verificar permisos según los argumentos
            if options['user']:
                self._check_user_permissions(options['user'], reports, pbirs_client)
            elif options['role']:
                self._check_role_permissions(options['role'], reports, pbirs_client)
            else:
                self._check_all_permissions(reports, pbirs_client)

        except Exception as e:
            logger.error(f"Error en verificación de permisos: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la verificación: {e}')
            )

    def _check_user_permissions(self, username, reports, pbirs_client):
        """
        Verifica los permisos de un usuario específico.
        """
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'\nVerificando permisos para usuario: {username}')

            for report in reports:
                has_permission = pbirs_client.check_permissions(
                    report.report_id,
                    username
                )
                
                status = self.style.SUCCESS('✓') if has_permission else self.style.ERROR('✗')
                self.stdout.write(
                    f'{status} {report.name}: '
                    f'{"Tiene acceso" if has_permission else "Sin acceso"}'
                )

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuario {username} no encontrado')
            )

    def _check_role_permissions(self, role_name, reports, pbirs_client):
        """
        Verifica los permisos de un rol específico.
        """
        try:
            role = Role.objects.get(name=role_name)
            self.stdout.write(f'\nVerificando permisos para rol: {role_name}')

            # Obtener usuarios con este rol
            users = User.objects.filter(
                userrole__role=role
            ).distinct()

            for user in users:
                self.stdout.write(f'\nUsuario: {user.username}')
                for report in reports:
                    has_permission = pbirs_client.check_permissions(
                        report.report_id,
                        user.username
                    )
                    
                    status = self.style.SUCCESS('✓') if has_permission else self.style.ERROR('✗')
                    self.stdout.write(
                        f'{status} {report.name}: '
                        f'{"Tiene acceso" if has_permission else "Sin acceso"}'
                    )

        except Role.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Rol {role_name} no encontrado')
            )

    def _check_all_permissions(self, reports, pbirs_client):
        """
        Verifica los permisos de todos los usuarios y roles.
        """
        self.stdout.write('\nVerificando permisos para todos los usuarios...')

        for user in User.objects.all():
            self.stdout.write(f'\nUsuario: {user.username}')
            for report in reports:
                has_permission = pbirs_client.check_permissions(
                    report.report_id,
                    user.username
                )
                
                status = self.style.SUCCESS('✓') if has_permission else self.style.ERROR('✗')
                self.stdout.write(
                    f'{status} {report.name}: '
                    f'{"Tiene acceso" if has_permission else "Sin acceso"}'
                ) 