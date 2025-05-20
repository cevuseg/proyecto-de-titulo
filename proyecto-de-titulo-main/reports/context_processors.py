"""
Procesadores de contexto para la aplicación de reportes.
Proporciona variables de contexto globales para las plantillas:
- Información del usuario actual
- Configuración de PBIRS
- Estadísticas de uso
"""

from django.conf import settings
from .models import PowerBIReport, UserRole

def user_context(request):
    """
    Procesador de contexto para información del usuario.
    Agrega información sobre roles y permisos del usuario actual.
    """
    if not request.user.is_authenticated:
        return {}

    # Obtener roles del usuario
    user_roles = UserRole.objects.filter(user=request.user).select_related('role')
    roles = [ur.role for ur in user_roles]
    role_names = [role.name for role in roles]

    return {
        'user_roles': roles,
        'role_names': role_names,
        'is_pbirs_admin': 'PBIRS_Admin' in role_names,
        'is_pbirs_viewer': 'PBIRS_Viewer' in role_names,
    }

def pbirs_config(request):
    """
    Procesador de contexto para configuración de PBIRS.
    Agrega variables de configuración necesarias para el cliente.
    """
    pbirs_config = getattr(settings, 'PBIRS_CONFIG', {})
    return {
        'pbirs_url': pbirs_config.get('REPORT_SERVER_URL', ''),
        'pbirs_manager_url': pbirs_config.get('REPORT_MANAGER_URL', ''),
        'pbirs_api_url': pbirs_config.get('API_URL', ''),
    }

def report_stats(request):
    """
    Procesador de contexto para estadísticas de reportes.
    Agrega información sobre el uso de reportes.
    """
    if not request.user.is_authenticated:
        return {}

    # Obtener roles del usuario
    user_roles = UserRole.objects.filter(user=request.user).select_related('role')
    roles = [ur.role for ur in user_roles]

    # Obtener reportes accesibles
    accessible_reports = PowerBIReport.objects.filter(roles__in=roles).distinct()

    return {
        'total_reports': accessible_reports.count(),
        'recent_reports': accessible_reports.order_by('-updated_at')[:5],
    } 