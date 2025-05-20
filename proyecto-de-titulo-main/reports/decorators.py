"""
Decoradores para la aplicación de reportes.
Proporciona decoradores para:
- Control de acceso a reportes
- Verificación de roles
- Registro de actividad
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import UserRole
import logging

logger = logging.getLogger(__name__)

def role_required(role_name):
    """
    Decorador para verificar que el usuario tenga un rol específico.
    Redirige al dashboard si el usuario no tiene el rol requerido.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verificar si el usuario tiene el rol requerido
            has_role = UserRole.objects.filter(
                user=request.user,
                role__name=role_name
            ).exists()

            if not has_role:
                logger.warning(
                    f"Intento de acceso denegado: {request.user.username} "
                    f"intentó acceder a {view_func.__name__} "
                    f"sin el rol {role_name}"
                )
                messages.error(
                    request,
                    f"No tiene el rol {role_name} necesario para esta acción"
                )
                return redirect('reports:dashboard')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def log_report_access(view_func):
    """
    Decorador para registrar el acceso a reportes.
    Registra información sobre quién accede a qué reporte.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Obtener el ID del reporte de los argumentos
        report_id = kwargs.get('report_id')
        
        # Registrar el acceso
        logger.info(
            f"Acceso a reporte: {report_id} "
            f"por usuario: {request.user.username} "
            f"desde IP: {request.META.get('REMOTE_ADDR')}"
        )

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    """
    Decorador para verificar que el usuario sea administrador.
    Lanza PermissionDenied si el usuario no es administrador.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            logger.warning(
                f"Intento de acceso administrativo denegado: "
                f"{request.user.username}"
            )
            raise PermissionDenied("Se requieren privilegios de administrador")

        return view_func(request, *args, **kwargs)
    return _wrapped_view 