"""
Comando de Django para validar la configuración del sistema.
Verifica la configuración de PBIRS y la base de datos.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from reports.models import PowerBIReport, Role, UserRole
from powerbi_reports.pbirs_client import PBIRSClient
import logging
import sys

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando para validar la configuración del sistema.
    Verifica la configuración y conexiones.
    """
    help = 'Valida la configuración del sistema de reportes'

    def add_arguments(self, parser):
        """
        Define los argumentos del comando.
        Permite especificar qué aspectos validar.
        """
        parser.add_argument(
            '--check-pbirs',
            action='store_true',
            help='Verificar conexión con PBIRS'
        )
        parser.add_argument(
            '--check-db',
            action='store_true',
            help='Verificar integridad de la base de datos'
        )
        parser.add_argument(
            '--check-permissions',
            action='store_true',
            help='Verificar permisos de usuarios'
        )

    def handle(self, *args, **options):
        """
        Ejecuta la validación de la configuración.
        Verifica los aspectos especificados.
        """
        try:
            self.stdout.write('Iniciando validación de configuración...')
            
            # Si no se especifican opciones, validar todo
            if not any(options.values()):
                options['check_pbirs'] = True
                options['check_db'] = True
                options['check_permissions'] = True
            
            # Validar configuración de PBIRS
            if options['check_pbirs']:
                self._validate_pbirs_config()
            
            # Validar base de datos
            if options['check_db']:
                self._validate_database()
            
            # Validar permisos
            if options['check_permissions']:
                self._validate_permissions()
            
            self.stdout.write(self.style.SUCCESS('\nValidación completada'))

        except Exception as e:
            logger.error(f"Error en validación: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error durante la validación: {e}')
            )
            sys.exit(1)

    def _validate_pbirs_config(self):
        """
        Valida la configuración de PBIRS.
        Verifica la conexión y los permisos necesarios.
        """
        self.stdout.write('\nValidando configuración de PBIRS...')
        
        # Verificar configuración
        required_settings = [
            'REPORT_SERVER_URL',
            'REPORT_MANAGER_URL',
            'API_URL',
            'CLIENT_ID',
            'CLIENT_SECRET',
            'TENANT_ID'
        ]
        
        pbirs_config = getattr(settings, 'PBIRS_CONFIG', {})
        missing_settings = [
            setting for setting in required_settings
            if setting not in pbirs_config
        ]
        
        if missing_settings:
            self.stdout.write(
                self.style.ERROR(
                    f'Configuración incompleta. Faltan: {", ".join(missing_settings)}'
                )
            )
            return False
        
        # Verificar conexión
        try:
            pbirs_client = PBIRSClient()
            reports = pbirs_client.get_reports()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Conexión exitosa. Reportes encontrados: {len(reports)}'
                )
            )
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error de conexión: {e}')
            )
            return False

    def _validate_database(self):
        """
        Valida la integridad de la base de datos.
        Verifica la consistencia de los datos.
        """
        self.stdout.write('\nValidando base de datos...')
        
        # Verificar reportes sin roles
        reports_without_roles = PowerBIReport.objects.filter(roles__isnull=True)
        if reports_without_roles.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Reportes sin roles asignados: {reports_without_roles.count()}'
                )
            )
        
        # Verificar roles sin usuarios
        roles_without_users = Role.objects.filter(userrole__isnull=True)
        if roles_without_users.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Roles sin usuarios asignados: {roles_without_users.count()}'
                )
            )
        
        # Verificar usuarios sin roles
        users_without_roles = UserRole.objects.none()
        for user in User.objects.all():
            if not UserRole.objects.filter(user=user).exists():
                users_without_roles = users_without_roles | UserRole.objects.filter(user=user)
        
        if users_without_roles.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Usuarios sin roles asignados: {users_without_roles.count()}'
                )
            )
        
        return True

    def _validate_permissions(self):
        """
        Valida los permisos de usuarios.
        Verifica que los permisos en PBIRS coincidan con la base de datos.
        """
        self.stdout.write('\nValidando permisos de usuarios...')
        
        try:
            pbirs_client = PBIRSClient()
            
            # Verificar permisos para cada usuario
            for user in User.objects.all():
                self.stdout.write(f'\nUsuario: {user.username}')
                
                # Obtener roles del usuario
                user_roles = UserRole.objects.filter(user=user).select_related('role')
                roles = [ur.role for ur in user_roles]
                
                # Obtener reportes accesibles
                accessible_reports = PowerBIReport.objects.filter(roles__in=roles).distinct()
                
                # Verificar permisos en PBIRS
                for report in accessible_reports:
                    has_permission = pbirs_client.check_permissions(
                        report.report_id,
                        user.username
                    )
                    
                    status = self.style.SUCCESS('✓') if has_permission else self.style.ERROR('✗')
                    self.stdout.write(
                        f'{status} {report.name}: '
                        f'{"Tiene acceso" if has_permission else "Sin acceso"}'
                    )
            
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al validar permisos: {e}')
            )
            return False 