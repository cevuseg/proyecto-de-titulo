"""
Utilidades para la aplicación de reportes.
Proporciona funciones auxiliares para:
- Manejo de permisos
- Formateo de datos
- Validación de configuraciones
"""

from django.conf import settings
from django.core.cache import cache
from .models import PowerBIReport, UserRole
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def get_user_reports(user):
    """
    Obtiene los reportes accesibles para un usuario.
    Utiliza caché para mejorar el rendimiento.
    """
    cache_key = f'user_reports_{user.id}'
    cached_reports = cache.get(cache_key)

    if cached_reports is not None:
        return cached_reports

    # Obtener roles del usuario
    user_roles = UserRole.objects.filter(user=user).select_related('role')
    roles = [ur.role for ur in user_roles]

    # Obtener reportes accesibles
    reports = PowerBIReport.objects.filter(roles__in=roles).distinct()

    # Guardar en caché por 5 minutos
    cache.set(cache_key, reports, 300)
    return reports

def format_report_data(report):
    """
    Formatea los datos de un reporte para su visualización.
    Incluye información adicional y metadatos.
    """
    return {
        'id': report.report_id,
        'name': report.name,
        'description': report.description,
        'workspace': report.workspace_id,
        'path': report.path,
        'roles': [role.name for role in report.roles.all()],
        'last_updated': report.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

def validate_pbirs_config():
    """
    Valida la configuración de PBIRS.
    Verifica que todas las configuraciones necesarias estén presentes.
    """
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
        logger.error(
            f"Configuración de PBIRS incompleta. "
            f"Faltan: {', '.join(missing_settings)}"
        )
        return False

    return True

def log_report_access(user, report, action='view'):
    """
    Registra el acceso a un reporte.
    Guarda información sobre quién, cuándo y qué acción realizó.
    """
    log_data = {
        'user': user.username,
        'report_id': report.report_id,
        'report_name': report.name,
        'action': action,
        'timestamp': datetime.now().isoformat(),
    }

    logger.info(
        f"Acceso a reporte: {json.dumps(log_data)}"
    )

def get_report_permissions(report_id, user):
    """
    Obtiene los permisos de un usuario sobre un reporte específico.
    Verifica roles y permisos en PBIRS.
    """
    # Verificar roles en la base de datos
    has_role = UserRole.objects.filter(
        user=user,
        role__reports__report_id=report_id
    ).exists()

    if not has_role:
        return False

    # Verificar permisos en PBIRS
    from powerbi_reports.pbirs_client import PBIRSClient
    pbirs_client = PBIRSClient()
    return pbirs_client.check_permissions(report_id, user.username) 